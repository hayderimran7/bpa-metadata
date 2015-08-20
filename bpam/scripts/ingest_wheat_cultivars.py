# -*- coding: utf-8 -*-

from apps.common.models import DNASource, Sequencer
from apps.wheat_cultivars.models import Organism, CultivarProtocol, CultivarSample, CultivarRun, CultivarSequenceFile
from libs import ingest_utils
from libs import bpa_id_utils
from libs.logger_utils import get_logger
from libs.excel_wrapper import ExcelWrapper

from libs.fetch_data import Fetcher
from unipath import Path
from collections import namedtuple

logger = get_logger(__name__)

BPA_ID = "102.100.100"
PROJECT_ID = 'WHEAT_CULTIVAR'
PROJECT_DESCRIPTION = 'Wheat Cultivars'

# all metadata and checksums should be linked out here
METADATA_URL = 'https://downloads.bioplatforms.com/wheat_cultivars/tracking/'
DATA_DIR = Path(ingest_utils.METADATA_ROOT, 'wheat_cultivars')

def get_dna_source(description):
    """
    Get a DNA source if it exists, if it doesn't make it.
    """

    description = description.strip().capitalize()
    if description == '':
        logger.debug('Set blank description to unknown')
        description = 'Unknown'

    source, created = DNASource.objects.get_or_create(description=description)
    if created:
        source.note = 'Added by Wheat Cultivars Project'
        source.save()

    return source


def _get_bpa_id(entry):
    """
    Get or make BPA ID
    """

    bpa_id, report = bpa_id_utils.get_bpa_id(entry.bpa_id, PROJECT_ID, PROJECT_DESCRIPTION)
    if bpa_id is None:
        logger.warning('Could not add entry in {}, row {}, BPA ID Invalid: {}'.format(entry.file_name, entry.row, report))
        return None
    return bpa_id


def ingest_samples(samples):
    """
    Add all the cultivar samples
    """

    def add_sample(e):
        """
        Adds new sample or updates existing sample
        """

        bpa_id = _get_bpa_id(e)
        if bpa_id is None:
            return

        wheat_organism, _ = Organism.objects.get_or_create(genus='Triticum', species='Aestivum')
        cultivar_sample, created = CultivarSample.objects.get_or_create(bpa_id=bpa_id, organism=wheat_organism)

        cultivar_sample.organism = wheat_organism
        cultivar_sample.name = e.variety
        cultivar_sample.cultivar_code = e.cultivar_code
        cultivar_sample.extract_name = e.extract_name
        cultivar_sample.casava_version = e.casava_version
        cultivar_sample.debug_note = ingest_utils.INGEST_NOTE + ingest_utils.pretty_print_namedtuple(e)
        cultivar_sample.save()
        logger.info("Ingested Cultivars sample {0}".format(cultivar_sample.name))

    for sample in samples:
        add_sample(sample)


def get_cultivar_sample_data(file_name):
    """
    The data sets is relatively small, so make a in-memory copy to simplify some operations.
    """

    field_spec = [('bpa_id', ('Unique ID', 'Soil sample unique ID'), lambda s: s.replace('/', '.')),
                  ('variety', 'Variety', None),
                  ('cultivar_code', 'Comment[Sample code]', None),  # C
                  ('library', 'Parameter Value[library layout]', None),
                  ('library_construction', 'Parameter Value[library nominal fragment size]', ingest_utils.get_clean_number),
                  ('index', 'Parameter Value[index]', None),
                  ('extract_name', 'Extract Name', None),
                  ('cycle_count', 'Parameter Value[Cycle count]', ingest_utils.get_clean_number),
                  ('sequencer', 'Parameter Value[sequencing instrument]', None),
                  ('casava_version', 'Parameter Value[CASAVA version]', None),
                  ('run_number', 'Parameter Value[run number]', ingest_utils.get_clean_number),
                  ('flow_cell_id', 'Parameter Value[flow cell identifier]', None),
                  ('lane_number', 'Parameter Value[lane number]', ingest_utils.get_clean_number),
                  ('sequence_filename', 'Raw Data File', None),
                  ('corrected_sequence_filename', 'Comment[Corrected file name]', None),
                  ('sequence_filetype', 'Comment[file format]', None),
                  ('md5_checksum', 'Comment[MD5 checksum]', None),
                  ]

    wrapper = ExcelWrapper(
        field_spec,
        file_name,
        sheet_name='Sheet1',
        header_length=3,
        column_name_row_index=1)
    return wrapper.get_all()


def ingest_runs(sample_data):
    def get_protocol(entry):
        def get_library_type(libtype):
            """
            (('PE', 'Paired End'), ('SE', 'Single End'), ('MP', 'Mate Pair'))
            """
            new_str = libtype.lower()
            if new_str.find('paired') >= 0:
                return 'PE'
            if new_str.find('single') >= 0:
                return 'SE'
            if new_str.find('mate') >= 0:
                return 'MP'
            return 'UN'

        base_pairs = entry.library_construction
        library_type = get_library_type(entry.library)
        protocol, created = CultivarProtocol.objects.get_or_create(
            base_pairs=base_pairs,
            library_type=library_type,
            library_construction_protocol='Illumina Sequencing Protocol')
        return protocol

    def get_sequencer(name):
        if name == "":
            name = "Unknown"
        try:
            sequencer = Sequencer.objects.get(name=name)
        except Sequencer.DoesNotExist:
            sequencer = Sequencer(name=name)
            sequencer.save()
        return sequencer

    def get_sample(bpa_id):
        wheat_organism, _ = Organism.objects.get_or_create(genus='Triticum', species='Aestivum')
        sample, created = CultivarSample.objects.get_or_create(bpa_id__bpa_id=bpa_id, organism=wheat_organism)
        if created:
            logger.info("New sample with ID {0}".format(bpa_id))
        return sample

    def add_run(entry):
        """
        The run produced several files
        """
        flow_cell_id = entry.flow_cell_id
        if flow_cell_id is None:
            return

        flow_cell_id = flow_cell_id.strip()
        bpa_id = _get_bpa_id(e)
        run_number = entry.run_number
        sample = get_sample(bpa_id)

        cultivar_run, _ = CultivarRun.objects.get_or_create(
            flow_cell_id=flow_cell_id,
            run_number=run_number,
            sample=sample)

        # just update
        cultivar_run.flow_cell_id = flow_cell_id
        cultivar_run.run_number = run_number
        cultivar_run.index_number = ingest_utils.get_clean_number(entry.index)
        cultivar_run.sequencer = get_sequencer(entry.sequencer)
        cultivar_run.lane_number = ingest_utils.get_clean_number(entry.lane_number)
        cultivar_run.protocol = get_protocol(e)
        cultivar_run.save()

        # FIXME, I'm sure this is wrong
        cultivar_run.protocol.run = cultivar_run
        cultivar_run.protocol.save()

        return cultivar_run

    def add_file(entry, wc_run):
        """
        Add each sequence file produced by a run
        """

        # Use the corrected sequence filename, as for this project (Wheat Cultivars),
        # that's what the user wants to see
        file_name = entry.corrected_sequence_filename
        if file_name is None:
            return

        file_name = corrected_sequence_filename.strip()
        if file_name != "":
            f = CultivarSequenceFile()
            f.sample = CultivarSample.objects.get(bpa_id__bpa_id=entry.bpa_id)
            f.run = wc_run
            f.index_number = ingest_utils.get_clean_number(entry.index)
            f.lane_number = ingest_utils.get_clean_number(entry.lane_number)
            f.filename = file_name
            f.original_sequence_filename = entry.sequence_filename
            f.md5 = entry.md5_checksum
            f.note = ingest_utils.pretty_print_namedtuple(entry)
            f.save()

    for e in sample_data:
        _run = add_run(e)
        add_file(e, _run)


def truncate():
    from django.db import connection

    cursor = connection.cursor()
    cursor.execute('TRUNCATE TABLE "{0}" CASCADE'.format(CultivarSample._meta.db_table))
    cursor.execute('TRUNCATE TABLE "{0}" CASCADE'.format(CultivarRun._meta.db_table))
    cursor.execute('TRUNCATE TABLE "{0}" CASCADE'.format(CultivarProtocol._meta.db_table))
    cursor.execute('TRUNCATE TABLE "{0}" CASCADE'.format(CultivarSequenceFile._meta.db_table))


def ingest(file_name):
    sample_data = list(get_cultivar_sample_data(file_name))
    bpa_id_utils.ingest_bpa_ids(sample_data, 'WHEAT_CULTIVAR', 'Wheat Cultivars')
    ingest_samples(sample_data)
    ingest_runs(sample_data)


def do_metadata():
    def is_metadata(path):
        if path.isfile() and path.ext == '.xlsx':
            return True

    logger.info('Ingesting Wheat Cultivars metadata from {0}'.format(DATA_DIR))
    for metadata_file in DATA_DIR.walk(filter=is_metadata):
        logger.info('Processing Wheat Cultivars {0}'.format(metadata_file))
        ingest(metadata_file)


def parse_md5_file(md5_file):
    """
    Parse md5 file
    PAS_AD08TAACXX_GCCAAT_L002_R1.fastq.gz
    """

    Cultivar = namedtuple('Cultivar', 'desc bpa_id')
    cultivars = {
            'DRY': Cultivar('Drysdale', '102.100.100.13703'),
            'GLA': Cultivar('Gladius', '102.100.100.13704'),
            'RAC': Cultivar('RAC 875', '102.100.100.13705'),
            'EXC': Cultivar('Excalibur', '102.100.100.13706'),
            'KUK': Cultivar('Kukri', '102.100.100.13707'),
            'ACB': Cultivar('AC Barry', '102.100.100.13708'),
            'BAX': Cultivar('Baxter', '102.100.100.13709'),
            'CH7': Cultivar('Chara', '102.100.100.13710'),
            'VOL': Cultivar('Volcani DD1', '102.100.100.13711'),
            'WES': Cultivar('Westonia', '102.100.100.13712'),
            'PAS': Cultivar('Pastor', '102.100.100.13713'),
            'XIA': Cultivar('Xiaoyan 54', '102.100.100.13714'),
            'YIT': Cultivar('Yitpi', '102.100.100.13715'),
            'ALS': Cultivar('Alsen', '102.100.100.13716'),
            'WYA': Cultivar('Wyalcatchem', '102.100.100.13717'),
            'H45': Cultivar('H45', '102.100.100.13718'),
        }


    data = []

    with open(md5_file) as f:
        for line in f.read().splitlines():
            line = line.strip()
            if line == '':
                continue

            file_data = {}
            md5, filename = line.split()
            file_data['md5'] = md5

            filename_parts = filename.split('.')[0].split('_')
            key = filename_parts[0]
            cultivar = cultivars.get(key, None)
            if cultivar is None:
                logger.warning("Key {} from {} ignored".format(key, md5_file))
                continue

            # PAS_AD08TAACXX_GCCAAT_L002_R1.fastq.gz
            if len(filename_parts) == 5:
                key, flowcell, index, lane, run = filename_parts

                file_data['filename'] = filename
                file_data['md5'] = md5
                file_data['bpa_id'] = cultivar.bpa_id
                file_data['key'] = key
                file_data['flowcell'] = flowcell
                file_data['index'] = index
                file_data['lane'] = int(lane[1:])
                file_data['run'] = int(run[1:])
                file_data['description'] = cultivar.desc

            # older files does not have the index
            elif len(filename_parts) == 4:
                key, flowcell, lane, run = filename_parts

                file_data['filename'] = filename
                file_data['md5'] = md5
                file_data['bpa_id'] = cultivar.bpa_id
                file_data['key'] = key
                file_data['flowcell'] = flowcell
                file_data['index'] = "NoIndex"
                file_data['lane'] = int(lane[1:])
                file_data['run'] = int(run[1:])
                file_data['description'] = cultivar.desc
            else:
                logger.error('Ignoring line {} from {} with incomprehensible data'.format(filename, md5_file))
                continue

            data.append(file_data)

    return data


def add_md5(data):
    """
    Add md5 data
    """

    def get_bpa_id(bpa_idx):
        bpa_id, report = bpa_id_utils.get_bpa_id(bpa_idx, PROJECT_ID, PROJECT_ID, 'Created by Wheat Cultivar ingestor')
        if bpa_id is None:
            return None
        return bpa_id


    def get_run(flow_cell_id, run_number, sample):
        cultivar_run, _ = CultivarRun.objects.get_or_create(
            flow_cell_id=flow_cell_id,
            run_number=run_number,
            sample=sample)
        return cultivar_run

    organism, _ = Organism.objects.get_or_create(genus="Triticum", species="Aestivum")
    for file_data in data:

        bpa_idx = file_data["bpa_id"]
        bpa_id = get_bpa_id(bpa_idx)
        if bpa_id is None:
            continue

        flowcell = file_data["flowcell"]
        run_number = file_data["run"]
        lane = file_data["lane"]

        f = CultivarSequenceFile()
        sample, created = CultivarSample.objects.get_or_create(bpa_id=bpa_id, organism=organism)
        f.sample = sample
        f.lane_number = lane
        f.run = get_run(flowcell, run_number, sample)
        f.filename = file_data["filename"]
        f.md5 = file_data["md5"]
        f.save()


def do_md5():
    """
    Ingest the md5 files
    """

    def is_md5file(path):
        if path.isfile() and path.ext == '.md5':
            return True

    logger.info('Ingesting Wheat Cultivar md5 file information from {0}'.format(DATA_DIR))
    for md5_file in DATA_DIR.walk(filter=is_md5file):
        logger.info('Processing Wheat Cultivar md5 file {0}'.format(md5_file))
        data = parse_md5_file(md5_file)
        add_md5(data)


def run():
    truncate()

    fetcher = Fetcher(DATA_DIR, METADATA_URL)
    fetcher.clean()
    fetcher.fetch_metadata_from_folder()

    do_md5()
    do_metadata()

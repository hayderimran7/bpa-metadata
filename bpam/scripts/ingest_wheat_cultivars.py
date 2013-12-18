import sys
import pprint
from datetime import datetime
import logging

import xlrd
from unipath import Path

from apps.common.models import DNASource, BPAUniqueID, Sequencer
from apps.wheat_cultivars.models import Organism, CultivarProtocol, CultivarSample, CultivarRun, CultivarSequenceFile
from libs import ingest_utils

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('WheatCultivars')

DATA_DIR = Path(Path(__file__).ancestor(3), "data/wheat_cultivars/")
DEFAULT_SPREADSHEET_FILE = Path(DATA_DIR, 'Wheat_cultivars.xlsx')

BPA_ID = "102.100.100"
DESCRIPTION = 'Wheat Cultivars'


def get_dna_source(description):
    """
    Get a DNA source if it exists, if it doesn't make it.
    """

    description = description.strip().capitalize()
    if description == '':
        logger.debug('Set blank description to unknown')
        description = 'Unknown'

    try:
        source = DNASource.objects.get(description=description)
    except DNASource.DoesNotExist:
        source = DNASource(description=description)
        source.note = 'Added by Cultivars Project'
        source.save()

    return source


def ingest_samples(samples):
    """
    Add all the cultivar samples
    """
    wheat_organism = Organism(genus='Triticum', species='Aestivum')
    wheat_organism.save()

    def add_sample(e):
        """
        Adds new sample or updates existing sample
        """

        bpa_id = e['bpa_id']

        if not ingest_utils.is_bpa_id(bpa_id):
            logger.warning('BPA ID {0} does not look like a real ID, ignoring'.format(bpa_id))
            return

        try:
            # Test if sample already exists
            cultivar_sample = CultivarSample.objects.get(bpa_id__bpa_id=bpa_id)
        except CultivarSample.DoesNotExist:
            cultivar_sample = CultivarSample()
            cultivar_sample.bpa_id = BPAUniqueID.objects.get(bpa_id=bpa_id)

        cultivar_sample.organism = wheat_organism
        cultivar_sample.name = e['name']
        cultivar_sample.dna_extraction_protocol = e['dna_extraction_protocol']
        cultivar_sample.cultivar_code = e['cultivar_code']
        cultivar_sample.extract_name = e['extract_name']
        cultivar_sample.casava_version = e['casava_version']
        cultivar_sample.protocol_reference = e['protocol_reference']
        cultivar_sample.note = e['note']
        cultivar_sample.debug_note = ingest_utils.INGEST_NOTE + pprint.pformat(e)

        cultivar_sample.save()
        logger.info("Ingested Cultivars sample {0}".format(cultivar_sample.name))

    for sample in samples:
        add_sample(sample)


def get_cultivar_sample_data(spreadsheet_file):
    """
    The data sets is relatively small, so make a in-memory copy to simplify some operations.
    """

    fieldnames = ['bpa_id',
                  'name',
                  'cultivar_code', # C
                  'dna_extraction_protocol',
                  'extract_name',
                  'library_construction_protocol',
                  'library_construction',
                  'library',
                  'index_sequence',
                  'extract_name',
                  'protocol_reference',
                  'index_number', # cycle count CHECK
                  'sequencer',
                  'casava_version',
                  'run_number',
                  'flow_cell_id',
                  'lane_number',
                  'sequence_filename',
                  'corrected_sequence_filename',
                  'sequence_filetype',
                  'md5_checksum',
                  'note'
    ]

    wb = xlrd.open_workbook(spreadsheet_file)
    sheet = wb.sheet_by_name('a_genome_seq_assay_BPA-Wheat-Cu')
    samples = []
    for row_idx in range(sheet.nrows)[2:]:  # the first two lines are headers
        vals = sheet.row_values(row_idx)

        if not ingest_utils.is_bpa_id(vals[0]):
            logger.warning('BPA ID {0} does not look like a real ID, ignoring'.format(vals[0]))
            continue

        # for date types try to convert to python dates
        types = sheet.row_types(row_idx)
        for i, t in enumerate(types):
            if t == xlrd.XL_CELL_DATE:
                vals[i] = datetime(*xlrd.xldate_as_tuple(vals[i], wb.datemode))

        samples.append(dict(zip(fieldnames, vals)))

    return samples


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

        base_pairs = ingest_utils.get_clean_number(entry['library_construction'])
        library_type = get_library_type(entry['library'])
        library_construction_protocol = entry['library_construction_protocol'].replace(',', '').capitalize()

        try:
            protocol = CultivarProtocol.objects.get(base_pairs=base_pairs,
                                                    library_type=library_type,
                                                    library_construction_protocol=library_construction_protocol)
        except CultivarProtocol.DoesNotExist:
            protocol = CultivarProtocol(base_pairs=base_pairs,
                                        library_type=library_type,
                                        library_construction_protocol=library_construction_protocol)
            protocol.save()
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
        try:
            sample = CultivarSample.objects.get(bpa_id__bpa_id=bpa_id)
            logger.debug("Found sample {0}".format(sample))
            return sample
        except CultivarSample.DoesNotExist:
            logger.error("No sample with ID {0}, quiting now".format(bpa_id))
            sys.exit(1)

    def get_run_number(entry):
        run_number = ingest_utils.get_clean_number(entry['run_number'])
        return run_number

    def add_run(entry):
        """
        The run produced several files
        """
        flow_cell_id = entry['flow_cell_id'].strip()
        bpa_id = entry['bpa_id'].strip()
        run_number = get_run_number(entry)

        try:
            cultivar_run = CultivarRun.objects.get(flow_cell_id=flow_cell_id,
                                                   run_number=run_number,
                                                   sample__bpa_id__bpa_id=bpa_id)
        except CultivarRun.DoesNotExist:
            cultivar_run = CultivarRun()
        cultivar_run.flow_cell_id = flow_cell_id
        cultivar_run.run_number = run_number
        cultivar_run.sample = get_sample(bpa_id)
        cultivar_run.index_number = ingest_utils.get_clean_number(entry['index_number'])
        cultivar_run.sequencer = get_sequencer(entry['sequencer'])
        cultivar_run.lane_number = ingest_utils.get_clean_number(entry['lane_number'])
        cultivar_run.protocol = get_protocol(e)
        cultivar_run.save()

        # FIXME, I'm sure this is wrong
        cultivar_run.protocol.run = cultivar_run
        cultivar_run.protocol.save()

        return cultivar_run

    def add_file(entry, cultivar_run):
        """
        Add each sequence file produced by a run
        """

        # Use the corrected sequence filename, as for this project (Wheat Cultivars),
        # thats what the user wants to see
        file_name = entry['corrected_sequence_filename'].strip()
        if file_name != "":
            f = CultivarSequenceFile()
            f.sample = CultivarSample.objects.get(bpa_id__bpa_id=entry['bpa_id'])
            f.run = cultivar_run
            f.index_number = ingest_utils.get_clean_number(entry['index_number'])
            f.lane_number = ingest_utils.get_clean_number(entry['lane_number'])
            f.filename = file_name
            f.original_sequence_filename = entry['sequence_filename']
            f.md5 = entry['md5_checksum']
            f.note = pprint.pformat(entry)
            f.save()

    for e in sample_data:
        sequence_run = add_run(e)
        add_file(e, sequence_run)


def ingest(spreadsheet_file):
    sample_data = get_cultivar_sample_data(spreadsheet_file)
    ingest_utils.ingest_bpa_ids(sample_data, 'Wheat Cultivars')
    ingest_samples(sample_data)
    ingest_runs(sample_data)


def run(spreadsheet_file=DEFAULT_SPREADSHEET_FILE):
    """
    Pass parameters like below:
    vpython-bpam manage.py runscript ingest_gbr --script-args Wheat_cultivars.xlsx
    """

    ingest(spreadsheet_file)

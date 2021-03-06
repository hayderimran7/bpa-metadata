# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from apps.wheat_cultivars.models import Organism, Protocol, CultivarSample, CultivarSequenceFile
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
METADATA_URL = 'https://downloads-qcif.bioplatforms.com/bpa/wheat_cultivars/tracking/'
DATA_DIR = Path(ingest_utils.METADATA_ROOT, 'wheat_cultivars')

Run = namedtuple('Run', 'run_number casava_version lib_cons_proto lib_range sequencer')


def get_bpa_id(entry):
    """
    Get or make BPA ID
    """

    bpa_id, report = bpa_id_utils.get_bpa_id(entry.bpa_id, PROJECT_ID, PROJECT_DESCRIPTION)
    if bpa_id is None:
        logger.warning('Could not add entry BPA ID Invalid: {}'.format(report))
        return None
    return bpa_id


def get_run_lookup():
    """
    Run data is uniquely defined by
    - bpa_id
    - flowcell
    - library type
    - library size

    Values recorded per key are:
    - run_number
    - CASAVA version
    - library construction protocol
    - sequencer
    - range
    """

    def is_metadata(path):
        if path.isfile() and path.ext == '.xlsx':
            return True

    logger.info('Ingesting Wheat Cultivars run metadata from {0}'.format(DATA_DIR))
    run_data = {}

    for metadata_file in DATA_DIR.walk(filter=is_metadata):
        logger.info('Processing Wheat Cultivars {0}'.format(metadata_file))
        run_data = list(get_run_data(metadata_file))

    run_lookup = {}

    for run in run_data:
        key = run.bpa_id + run.flowcell + run.library + run.library_construction
        runt = Run(run.run_number, run.casava_version, run.library_construction_protocol, run.library_range,
                   run.sequencer)
        run_lookup[key] = runt
    return run_lookup


def ingest_samples(samples):
    """
    Add all the cultivar samples
    """

    wheat_organism, _ = Organism.objects.get_or_create(genus='Triticum', species='Aestivum')

    def add_sample(e):
        """
        Adds cultivar sample from spreadsheet
        """

        bpa_id = get_bpa_id(e)
        if bpa_id is None:
            return

        cultivar_sample, created = CultivarSample.objects.get_or_create(bpa_id=bpa_id, organism=wheat_organism)

        cultivar_sample.name = e.variety  # DDD
        cultivar_sample.variety = e.variety
        cultivar_sample.cultivar_code = e.code
        cultivar_sample.source_name = e.source_name
        cultivar_sample.characteristics = e.characteristics
        cultivar_sample.organism = wheat_organism

        cultivar_sample.organism_part = e.organism_part
        cultivar_sample.pedigree = e.pedigree
        cultivar_sample.dev_stage = e.dev_stage
        cultivar_sample.yield_properties = e.yield_properties
        cultivar_sample.morphology = e.morphology
        cultivar_sample.maturity = e.maturity

        cultivar_sample.pathogen_tolerance = e.pathogen_tolerance
        cultivar_sample.drought_tolerance = e.drought_tolerance
        cultivar_sample.soil_tolerance = e.soil_tolerance

        cultivar_sample.classification = e.classification
        cultivar_sample.url = e.url

        cultivar_sample.debug_note = ingest_utils.INGEST_NOTE + ingest_utils.pretty_print_namedtuple(e)

        cultivar_sample.save()
        logger.info("Ingested Cultivars sample {0}".format(cultivar_sample.name))

    for sample in samples:
        add_sample(sample)


def do_metadata():
    def is_metadata(path):
        if path.isfile() and path.ext == '.xlsx':
            return True

    logger.info('Ingesting Wheat Cultivars metadata from {0}'.format(DATA_DIR))
    for metadata_file in DATA_DIR.walk(filter=is_metadata):
        logger.info('Processing Wheat Cultivars {0}'.format(metadata_file))
        sample_data = list(get_cultivar_sample_characteristics(metadata_file))
        bpa_id_utils.ingest_bpa_ids(sample_data, 'WHEAT_CULTIVAR', 'Wheat Cultivars')
        ingest_samples(sample_data)


def parse_md5_file(md5_file):
    """
    Parse md5 file
    PAS_AD08TAACXX_GCCAAT_L002_R1.fastq.gz
    """

    class MD5ParsedLine(object):
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

        def __init__(self, line):
            self._line = line

            self.cultivar_key = None
            self.cultivar = None
            self.bpa_id = None
            self.lib_type = None
            self.lib_size = None
            self.flowcell = None
            self.barcode = None

            self.md5 = None
            self.filename = None

            self._lane = None
            self._read = None

            self._ok = False

            self.__parse_line()

        def is_ok(self):
            return self._ok

        @property
        def lane(self):
            return self._lane

        @lane.setter
        def lane(self, val):
            self._lane = int(val[1:])

        @property
        def read(self):
            return self._read

        @read.setter
        def read(self, val):
            self._read = int(val[1:])

        def __parse_line(self):
            """ unpack the md5 line """
            self.md5, self.filename = self._line.split()

            filename_parts = self.filename.split('.')[0].split('_')
            self.cultivar_key = filename_parts[0]

            # there are some files with an unknown cultivar code
            self.cultivar = self.cultivars.get(self.cultivar_key, None)
            if self.cultivar is None:
                self._ok = False
                return

            self.bpa_id = self.cultivar.bpa_id

            # WYA_PE_300bp_AD0ALYACXX_ATCACG_L003_R2.fastq.gz
            # [Cultivar_key]_[Library_Type]_[Library_Size]_[FLowcel]_[Barcode]_L[Lane_number]_R[Read_Number].
            if len(filename_parts) == 7:
                _key, self.lib_type, self.lib_size, self.flowcell, self.barcode, self.lane, self.read = filename_parts
                self._ok = True
            else:
                self._ok = False  # be explicit

    data = []

    with open(md5_file) as f:
        for line in f.read().splitlines():
            line = line.strip()
            if line == '':
                continue

            parsed_line = MD5ParsedLine(line)
            if parsed_line.is_ok():
                data.append(parsed_line)

    return data


def add_md5(md5_lines, run_data):
    """
    Add md5 data
    """

    organism, _ = Organism.objects.get_or_create(genus="Triticum", species="Aestivum")

    for md5_line in md5_lines:
        bpa_idx = md5_line.bpa_id
        bpa_id, report = bpa_id_utils.get_bpa_id(bpa_idx, PROJECT_ID, PROJECT_DESCRIPTION)
        if bpa_id is None:
            continue

        key = md5_line.bpa_id + md5_line.flowcell + md5_line.lib_type + md5_line.lib_size
        run = run_data.get(
            key, Run(run_number=-1, casava_version="-",
                     lib_cons_proto="-",
                     lib_range="-", sequencer="-"))
        protocol = Protocol()
        protocol.library_type = md5_line.lib_type
        protocol.set_base_pairs(md5_line.lib_size)
        protocol.library_construction_protocol = run.lib_cons_proto
        protocol.sequencer = run.sequencer
        protocol.save()

        f = CultivarSequenceFile()
        sample, created = CultivarSample.objects.get_or_create(bpa_id=bpa_id, organism=organism)
        f.sample = sample
        f.protocol = protocol
        f.flowcell = md5_line.flowcell
        f.barcode = md5_line.barcode
        f.read_number = md5_line.read
        f.lane_number = md5_line.lane
        f.run_number = run.run_number
        f.casava_version = run.casava_version

        f.filename = md5_line.filename
        f.md5 = md5_line.md5
        f.save()


def get_run_data(file_name):
    """
    The run metadata for this set
    """

    field_spec = [('bpa_id', 'Soil sample unique ID', lambda s: s.replace('/', '.')),
                  ('variety', 'Variety', None),
                  ('cultivar_code', 'Code', None),
                  ('library', 'Library code', None),
                  ('library_construction', 'Library Construction - average insert size', None),
                  ('library_range', 'Range', None),
                  ('library_construction_protocol', 'Library construction protocol', None),
                  ('sequencer', 'Sequencer', None),
                  ('run_number', 'Run number', ingest_utils.get_clean_number),
                  ('flowcell', 'Flow Cell ID', None),
                  ('index', 'Index', None),
                  ('casava_version', 'CASAVA version', None), ]

    wrapper = ExcelWrapper(field_spec, file_name, sheet_name='Metadata', header_length=1)
    return wrapper.get_all()


def get_cultivar_sample_characteristics(file_name):
    """
    This is the data from the Characteristics Sheet
    """

    field_spec = [
        ("source_name", "BPA ID", None),
        ("code", "CODE", None),
        ("bpa_id", "BPA ID", lambda s: s.replace("/", ".")),
        ("characteristics", "Characteristics", None),
        ("organism", "Organism", None),
        ("variety", "Variety", None),
        ("organism_part", "Organism part", None),
        ("pedigree", "Pedigree", None),
        ("dev_stage", "Developmental stage", None),
        ("yield_properties", "Yield properties", None),
        ("morphology", "Morphology", None),
        ("maturity", "Maturity", None),
        ("pathogen_tolerance", "Pathogen tolerance", None),
        ("drought_tolerance", "Drought tolerance", None),
        ("soil_tolerance", "Soil tolerance", None),
        ("classification", "International classification", None),
        ("url", "Link", None),
    ]

    wrapper = ExcelWrapper(field_spec, file_name, sheet_name="Characteristics", header_length=1)
    return wrapper.get_all()


def do_md5():
    """
    Ingest the md5 files
    """

    run_data = get_run_lookup()

    def is_md5file(path):
        if path.isfile() and path.ext == '.md5':
            return True

    logger.info('Ingesting Wheat Cultivar md5 file information from {0}'.format(DATA_DIR))
    for md5_file in DATA_DIR.walk(filter=is_md5file):
        logger.info('Processing Wheat Cultivar md5 file {0}'.format(md5_file))
        data = parse_md5_file(md5_file)
        add_md5(data, run_data)


def truncate():
    from django.db import connection

    cursor = connection.cursor()
    cursor.execute('TRUNCATE TABLE "{0}" CASCADE'.format(CultivarSample._meta.db_table))
    cursor.execute('TRUNCATE TABLE "{0}" CASCADE'.format(Protocol._meta.db_table))
    cursor.execute('TRUNCATE TABLE "{0}" CASCADE'.format(CultivarSequenceFile._meta.db_table))


class Command(BaseCommand):
    help = 'Ingest Wheat Cultivars'

    def handle(self, *args, **options):
        truncate()

        fetcher = Fetcher(DATA_DIR, METADATA_URL)
        fetcher.clean()
        fetcher.fetch_metadata_from_folder()

        do_metadata()
        do_md5()

from unipath import Path

from libs.excel_wrapper import ExcelWrapper
from libs import bpa_id_utils
from libs import logger_utils
from apps.common.models import Facility
from apps.base_amplicon.models import AmpliconSample


logger = logger_utils.get_logger(__name__)

DATA_DIR = Path(Path(__file__).ancestor(3), "data/base/amplicons")
DEFAULT_SPREADSHEET_FILE = Path(DATA_DIR, 'amplicon_test')

BPA_ID = "102.100.100"
BASE_DESCRIPTION = 'BASE'


def get_bpa_id(e):
    """
    Get or make BPA ID
    """

    bpa_id = bpa_id_utils.get_bpa_id(e.bpa_id, 'BASE', 'BASE')
    if not bpa_id:
        logger.warning('Ignoring {0}, not a good BPA ID'.format(e.bpa_id))
        return None
    return bpa_id


def get_data(file_name):
    """
    The data sets is relatively small, so make a in-memory copy to simplify some operations.
    """

    field_spec = [('bpa_id', 'Soil sample unique ID', lambda s: s.replace('/', '.')),
                  ('sample_extraction_id', 'Sample extraction ID', None),
                  ('genome_sequencing_facility', 'Sequencing facility', None),
                  ('target', 'Target', lambda s: s.upper()),
                  ('index', 'Index', None),
                  ('pcr_1_to_10', '1:10 PCR, P=pass, F=fail', None),
                  ('pcr_1_to_100', '1:100 PCR, P=pass, F=fail', None),
                  ('pcr_neat', 'neat PCR, P=pass, F=fail', None),
                  ('dilution', 'Dilution used', None),
                  ('run_number', 'Sequencing run number', None),
                  ('flow_cell_id', 'Flowcell', None),
                  ('reads', '# of reads', None),
                  ('name', 'Sample name on sample sheet', None),
                  ('analysis_software_version', 'AnalysisSoftwareVersion', None),
                  ('comments', 'Comments', None),
    ]

    wrapper = ExcelWrapper(field_spec,
                           file_name,
                           sheet_name='Sheet1',
                           header_length=4,
                           column_name_row_index=1)

    return wrapper.get_all()


def get_facility(entry):
    """
    Get teh facility
    """
    facility_str = entry.genome_sequencing_facility
    if facility_str == '':
        return None
    try:
        return Facility.objects.get(name__iexact=facility_str)
    except Facility.DoesNotExist:
        logger.warning('Facility "{0}" on line {1} not known'.format(facility_str, entry.row))
        return None


def add_samples(data):
    """
    Add sequence files
    """
    for entry in data:
        bpa_id = get_bpa_id(entry)
        if bpa_id is None:
            logger.warning('Could not add entry '.format(entry))
            continue

        sample, created = AmpliconSample.objects.get_or_create(bpa_id=bpa_id)

        sample.sample_extraction_id = entry.sample_extraction_id
        sample.name = entry.name

        sample.genome_sequencing_facility = get_facility(entry)
        sample.index = entry.index
        sample.target = entry.target
        sample.pcr_1_to_10 = entry.pcr_1_to_10
        sample.pcr_1_to_100 = entry.pcr_1_to_100
        sample.pcr_neat = entry.pcr_neat
        sample.dilution = entry.dilution

        sample.analysis_software_version = entry.analysis_software_version
        sample.reads = entry.reads

        sample.note = entry.comments

        sample.save()


def run(file_name=DEFAULT_SPREADSHEET_FILE):
    """
    Pass parameters like below:
    vpython-bpam manage.py runscript ingest_base_454 --script-args Melanoma_study_metadata.xlsx
    """

    samples = list(get_data(file_name))
    add_samples(samples)



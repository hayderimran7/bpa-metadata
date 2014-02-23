from unipath import Path

from libs.excel_wrapper import ExcelWrapper
from libs import bpa_id_utils
from libs import ingest_utils
from libs import logger_utils
from apps.base.models.metagenomics import MetagenomicsSample, MetagenomicsSequenceFile


logger = logger_utils.get_logger('BASE Metagenomics')

DATA_DIR = Path(Path(__file__).ancestor(3), "data/base/")
DEFAULT_SPREADSHEET_FILE = Path(DATA_DIR, 'metagenomics')

BPA_ID = "102.100.100"
BASE_DESCRIPTION = 'BASE'


def get_sample(e):
    """
    Get the Sample by bpa_id
    """

    bpa_id = bpa_id_utils.get_bpa_id(e.bpa_id, BASE_DESCRIPTION, note='BASE Metagenomics Sample')
    if bpa_id is None:
        return None

    try:
        sample = MetagenomicsSample.objects.get(bpa_id__bpa_id=bpa_id)
    except MetagenomicsSample.DoesNotExist:
        logger.debug('Adding Metagenomics Sample ' + bpa_id.bpa_id)
        sample = MetagenomicsSample(bpa_id=bpa_id)

    # always update
    sample.name = e.sample_id
    sample.dna_extraction_protocol = e.library_protocol
    sample.requested_sequence_coverage = e.library_construction
    sample.collection_date = e.date_received
    sample.debug_note = ingest_utils.pretty_print_namedtuple(e)
    sample.save()

    return sample


def get_data(file_name):
    """
    The data sets is relatively small, so make a in-memory copy to simplify some operations.
    """

    def set_flag(flag):
        """
        Inconsistent spreadsheet data, can be either a boolean or y or n string
        """
        if isinstance(flag, bool):
            return flag
        if not isinstance(flag, basestring):
            return False
        if flag.lower() == 'y':
            return True
        return False

    def set_id(_bpa_id):
        if isinstance(_bpa_id, basestring):
            return _bpa_id.strip().replace('/', '.')
        else:
            logger.warning('Expected a valid BPA_ID got {0}'.format(_bpa_id))
            return ''

    field_spec = [('bpa_id', 'BPA ID', set_id),
                  ('sample_id', 'Sample ID', None),
                  ('genome_sequencing_facility', 'Genome Sequencing Facility', None),
                  ('date_received', 'Date Received by sequencing facility', ingest_utils.get_date),
                  ('comments', 'Comments by sequencing facility', None),
                  ('date_sequenced', 'Date sequenced', ingest_utils.get_date),
                  ('library', 'Library', None),
                  ('library_construction', 'Library Construction (insert size bp)', ingest_utils.get_clean_number),
                  ('library_protocol', 'Library construction protocol', None),
                  ('index', 'Index', None),
                  ('sequencer', 'Sequencer', None),
                  ('run', 'Run number', None),
                  ('flow_cell_id', 'Run #:Flow Cell ID', None),
                  ('lane_number', 'Lane number', None),
                  ('file_name', 'FILE NAMES - supplied by sequencing facility', None),
                  ('md5sum', 'MD5 Checksum', None),
                  ('date_data_sent', 'Date data sent/transferred', ingest_utils.get_date),
    ]

    wrapper = ExcelWrapper(field_spec,
                           file_name,
                           sheet_name='BASE Metagenomics',
                           header_length=1,
                           column_name_row_index=0)

    return wrapper.get_all()


def add_sequence_files(data):
    """
    Add sequence files
    """
    for file_row in data:
        sample = get_sample(file_row)
        if sample is None:
            logger.warning('Could not add sample {0}'.format(sample))

        sequence_file = MetagenomicsSequenceFile()
        sequence_file.sample = sample
        sequence_file.filename = file_row.file_name
        sequence_file.md5 = file_row.md5sum
        sequence_file.index_number = file_row.index
        sequence_file.lane_number = file_row.lane_number
        sequence_file.date_received_from_sequencing_facility = file_row.date_received
        sequence_file.note = file_row.comments

        sequence_file.save()


def run(file_name=DEFAULT_SPREADSHEET_FILE):
    """
    Pass parameters like below:
    vpython-bpam manage.py runscript ingest_base_454 --script-args Melanoma_study_metadata.xlsx
    """

    data = list(get_data(file_name))
    add_sequence_files(data)



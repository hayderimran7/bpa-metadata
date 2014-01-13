import logging
import pprint
import sys
from unipath import Path

from libs.excel_wrapper import ExcelWrapper
from libs import bpa_id_utils
from libs import ingest_utils

from apps.BASE.models import SoilMetagenomicsSample

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('BASE Metagenomics')

DATA_DIR = Path(Path(__file__).ancestor(3), "data/base/")
DEFAULT_SPREADSHEET_FILE = Path(DATA_DIR, 'metagenomics')

BPA_ID = "102.100.100"
BASE_DESCRIPTION = 'BASE'


def get_bpa_id(t):
    if bpa_id_utils.is_good_bpa_id(t.bpa_id):
        return bpa_id_utils.get_bpa_id(t.bpa_id, BASE_DESCRIPTION, note='BASE Metagenomics Sample')
    else:
        return None


def get_sample(t):
    """
    Get the Sample by bpa_id
    """

    bpa_id = get_bpa_id(t)
    if bpa_id is None:
        return None

    try:
        sample = SoilMetagenomicsSample.objects.get(bpa_id=bpa_id)
    except SoilMetagenomicsSample.DoesNotExist:
        logger.debug('Adding Metagenomics Sample ' + bpa_id.bpa_id)
        sample = SoilMetagenomicsSample(bpa_id=bpa_id)
        sample.name = t.sample_id
        sample.dna_extraction_protocol = t.library_protocol
        sample.requested_sequence_coverage = t.library_construction
        sample.collection_date = t.date_received
    return sample


def ingest(file_name):
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

    wrapper = ExcelWrapper(field_spec, file_name, sheet_name='BASE Metagenomics', header_length=1,
                           column_name_row_index=0)
    for t in wrapper.get_all():
        # ID
        bpa_id = get_bpa_id(t)
        if bpa_id is None:
            logger.warning('BPA ID {0} does not look like a proper BPA ID ignoring'.format(t.bpa_id))
            continue

        sample = get_sample(bpa_id)

        sample.save()

        try:
            sample.save()
        except Exception, e:
            pprint.pprint(e)
            pprint.pprint(t)
            sys.exit(1)


def run(file_name=DEFAULT_SPREADSHEET_FILE):
    """
    Pass parameters like below:
    vpython-bpam manage.py runscript ingest_base_454 --script-args Melanoma_study_metadata.xlsx
    """

    ingest(file_name)



# -*- coding: utf-8 -*-

import sys
from contracts import contract
from unipath import Path
from libs.fetch_data import Fetcher, get_password
from libs.excel_wrapper import ExcelWrapper
from libs.logger_utils import get_logger
from libs import bpa_id_utils
from libs import user_helper
from libs import ingest_utils
from libs import management_command
from apps.base_454.models import Sample454

logger = get_logger(__name__)

METADATA_PATH = 'base/metadata/'
BASE_454_FILE = 'BASE_454.xlsx'
DATA_DIR = Path(ingest_utils.METADATA_ROOT, METADATA_PATH)

BPA_ID = "102.100.100"
PROJECT_DESCRIPTION = 'BASE'
PROJECT_ID = 'BASE'


def _get_bpa_id(entry):
    """
    Get or make BPA ID
    """

    bpa_id, report = bpa_id_utils.get_bpa_id(entry.bpa_id, PROJECT_ID, PROJECT_DESCRIPTION)
    if bpa_id is None:
        logger.warning('Could not add entry in BPA ID Invalid: {}'.format(report))
        return None
    return bpa_id


@contract
def get_sample_454(bpa_id):
    """ Get the Sample given a BPAUniqueID object
     :param bpa_id: BPA Unique ID object
     :type bpa_id: *
    """

    sample, created = Sample454.objects.get_or_create(bpa_id=bpa_id)
    if created:
        logger.info('Adding 454 Sample {0}'.format(bpa_id.bpa_id))
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

    def set_result(val):
        """
        The result must be either P, F, R or NP
        """

        # non strings
        if val is None:
            return 'U'
        if not isinstance(val, basestring):
            return 'U'

        # at least we are dealing with a string now
        val = val.strip().upper()
        if val == '':
            return 'U'

        if val == 'REPEAT':
            return 'R'

        if val not in ('P', 'F', 'R', 'NP'):
            logger.warning("Val must be either P, F, R or NP not '{0}'".format(val))
            return 'U'

        return val

    def set_purified(p):
        return p.lower().find('purified') != -1

    field_spec = [('bpa_id', 'Unique ID', set_id),
                  ('sample_id', 'Sample ID', None),
                  ('aurora_purified', 'Aurora purified', set_purified),
                  ('dna_storage_nunc_plate', 'DNA Storage Nunc Plate', None),
                  ('dna_storage_nunc_tube', 'DNA Storage Nunc Tube', None),
                  ('dna_storage_nunc_well_location', 'DNA Storage Well Location', None),
                  ('agrf_batch_number', 'AGRF Batch number', None),
                  ('submitter_name', 'Submitter Name', None),
                  ('date_received', 'Date received', ingest_utils.get_date),
                  # Adelaide extraction
                  ('adelaide_extraction_sample_weight', 'Extraction Sample Weight (mg)', None),  # mg
                  ('adelaide_fluorimetry', 'Fluorimetry ng/uL gDNA', ingest_utils.get_clean_float),  # ng/uL gDNA'
                  ('adelaide_pcr_inhibition',
                   'PCR Inhibition (neat plus spike) 16S (V3-V8) p=pass, f=fail, NP = not performed', set_result),
                  ('adelaide_pcr1', 'PCR1 (neat) 16S (V3-V8) p=pass, f-fail  NP = not performed', set_result),
                  ('adelaide_pcr2', 'PCR2 (1:100) 16S (V3-V8) p=pass, f=fail   NP = not performed', set_result),
                  ('adelaide_date_shipped_to_agrf_454', 'DNA shipped to AGRF (454)', ingest_utils.get_date),
                  ('adelaide_date_shipped_to_agrf_miseq', 'DNA shipped to AGRF (MiSeq)', ingest_utils.get_date),
                  ('adelaide_date_shipped_to_ramacciotitti', 'DNA shipped to Ramaciotti', ingest_utils.get_date),
                  # Brisbane 454
                  ('brisbane_16s_mid', '16S MID', ingest_utils.get_clean_float),
                  ('brisbane_its_mid', 'ITS MID', ingest_utils.get_clean_float),
                  ('brisbane_16s_pcr1', '16S (V1-V3) PCR1 (neat) p=pass, f=fail', set_result),
                  ('brisbane_16s_pcr2', '16S (V1-V3) PCR2 (1:10) p=pass, f=fail', set_result),
                  ('brisbane_16s_pcr3', '16S (V1-V3) PCR3 (fusion-primer) p=pass, f=fail', set_result),
                  ('brisbane_its_pcr1_neat', 'ITS PCR1 (neat) p=pass, f=fail', set_result),
                  ('brisbane_its_pcr2_1_10', 'ITS PCR1 (1:10) p=pass, f=fail', set_result),
                  ('brisbane_its_pcr3_fusion', 'ITS PCR3 (fusion-primer) p=pass, f=fail', set_result),
                  ('brisbane_fluorimetry_16s', 'Fluorimetry ng/uL 16S', ingest_utils.get_clean_float),  # ng/uL 16S
                  ('brisbane_fluorimetry_its', 'Fluorimetry ng/uL ITS', ingest_utils.get_clean_float),  # ng/uL 16S
                  ('brisbane_16s_qpcr', '16S qPCR', ingest_utils.get_clean_float),
                  ('brisbane_its_qpcr', 'ITS qPCR', ingest_utils.get_clean_float),
                  ('brisbane_i6s_pooled', '16S pooled y=yes, n=no', set_flag),
                  ('brisbane_its_pooled', 'ITS pooled y=yes, n=no', set_flag),
                  ('brisbane_16s_reads', '16S >3000 reads - Trim Back 150bp', ingest_utils.get_clean_number),
                  ('brisbane_its_reads', 'ITS >3000 reads - Trim Back 150bp Run1', ingest_utils.get_clean_number),
                  ('note', 'Sample comments', None), ]

    wrapper = ExcelWrapper(field_spec, file_name, sheet_name='Sheet1', header_length=2, column_name_row_index=1)
    for t in wrapper.get_all():
        # ID
        bpa_id = _get_bpa_id(t)
        if bpa_id is None:
            logger.warning('BPA ID {0} does not look like a proper BPA ID ignoring'.format(t.bpa_id))
            continue

        sample = get_sample_454(bpa_id)
        sample.sample_id = t.sample_id
        sample.aurora_purified = t.aurora_purified
        sample.dna_storage_nunc_plate = t.dna_storage_nunc_plate
        sample.dna_storage_nunc_tube = t.dna_storage_nunc_tube
        sample.dna_storage_nunc_well_location = t.dna_storage_nunc_well_location
        sample.agrf_batch_number = t.agrf_batch_number
        sample.submitter = user_helper.get_user(t.submitter_name, '', ('AGRF', 'BASE'))
        sample.date_received = t.date_received
        # adelaide
        sample.adelaide_extraction_sample_weight = t.adelaide_extraction_sample_weight
        sample.adelaide_fluorimetry = t.adelaide_fluorimetry
        sample.adelaide_pcr_inhibition = t.adelaide_pcr_inhibition
        sample.adelaide_pcr1 = t.adelaide_pcr1
        sample.adelaide_pcr2 = t.adelaide_pcr2
        sample.adelaide_date_shipped_to_agrf_454 = t.adelaide_date_shipped_to_agrf_454
        sample.adelaide_date_shipped_to_agrf_miseq = t.adelaide_date_shipped_to_agrf_miseq
        sample.adelaide_date_shipped_to_ramacciotitti = t.adelaide_date_shipped_to_ramacciotitti
        # brisbane
        sample.brisbane_16s_mid = t.brisbane_16s_mid
        sample.brisbane_its_mid = t.brisbane_its_mid
        sample.brisbane_16s_pcr1 = t.brisbane_16s_pcr1
        sample.brisbane_16s_pcr2 = t.brisbane_16s_pcr2
        sample.brisbane_16s_pcr3 = t.brisbane_16s_pcr3
        sample.brisbane_its_pcr1_neat = t.brisbane_its_pcr1_neat
        sample.brisbane_its_pcr2_1_10 = t.brisbane_its_pcr2_1_10
        sample.brisbane_its_pcr3_fusion = t.brisbane_its_pcr3_fusion
        sample.brisbane_fluorimetry_16s = t.brisbane_fluorimetry_16s
        sample.brisbane_fluorimetry_its = t.brisbane_fluorimetry_its
        sample.brisbane_16s_qpcr = t.brisbane_16s_qpcr
        sample.brisbane_its_qpcr = t.brisbane_its_qpcr
        sample.brisbane_i6s_pooled = t.brisbane_i6s_pooled
        sample.brisbane_16s_reads = t.brisbane_i6s_pooled
        sample.brisbane_its_reads = t.brisbane_its_reads
        sample.note = t.note
        sample.debug_note = ingest_utils.pretty_print_namedtuple(t)

        try:
            sample.save()
        except Exception as e:
            logger.error(e)
            sys.exit(1)


def truncate():
    from django.db import connection

    cursor = connection.cursor()
    cursor.execute('TRUNCATE TABLE "{0}" CASCADE'.format(Sample454._meta.db_table))


def do_metadata():
    def is_metadata(path):
        if path.isfile() and path.ext == '.xlsx':
            return True

    logger.info('Ingesting BASE Contextual Data from {0}'.format(DATA_DIR))
    for metadata_file in DATA_DIR.walk(filter=is_metadata):
        logger.info('Processing BASE Contextual Data file {0}'.format(metadata_file))
        ingest(metadata_file)


class Command(management_command.BPACommand):
    help = 'Ingest BASE 454 Data'

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument('--delete',
                            action='store_true',
                            dest='delete',
                            default=False,
                            help='Delete all BASE 454 data', )

    def handle(self, *args, **options):
        if options['delete']:
            logger.info("Deleting all 454 data")
            truncate()

        fetcher = Fetcher(DATA_DIR, self.get_base_url(options) + METADATA_PATH, auth=('base', get_password('base')))
        fetcher.fetch(BASE_454_FILE)
        truncate()
        do_metadata()

# -*- coding: utf-8 -*-

from unipath import Path
from libs.fetch_data import Fetcher
from libs.excel_wrapper import ExcelWrapper
from libs import bpa_id_utils
from libs import ingest_utils
from libs import logger_utils

from apps.common.models import Facility, Sequencer
from apps.base_metagenomics.models import MetagenomicsSample, MetagenomicsSequenceFile, MetagenomicsRun


logger = logger_utils.get_logger(__name__)

METADATA_URL = 'https://downloads.bioplatforms.com/base/tracking/metagenomics/'
DATA_DIR = Path(ingest_utils.METADATA_ROOT, 'base/metagenomics_metadata/')

BPA_ID = "102.100.100"
BASE_DESCRIPTION = 'BASE'


def _get_bpa_id(entry):
    """
    Get or make BPA ID
    """

    bpa_id, report = bpa_id_utils.get_bpa_id(entry.bpa_id, 'BASE', 'BASE', note="BASE Metagenomics Sample")
    if bpa_id is None:
        logger.warning('Could not add entry in {}, row {}, BPA ID Invalid: {}'.format(entry.file_name, entry.row, report))
        return None
    return bpa_id


def get_data(file_name):
    """
    The data sets is relatively small, so make a in-memory copy to simplify some operations.
    """

    def get_library_type(library):
        """
        (('PE', 'Paired End'), ('SE', 'Single End'), ('MP', 'Mate Pair'))
        """
        new_str = library.lower()
        if new_str.find('pair') >= 0:
            return 'PE'
        if new_str.find('single') >= 0:
            return 'SE'
        if new_str.find('mate') >= 0:
            return 'MP'
        return 'UN'

    def set_id(_bpa_id):
        if isinstance(_bpa_id, basestring):
            return _bpa_id.strip().replace('/', '.')
        else:
            logger.warning('Expected a valid BPA_ID got {0}'.format(_bpa_id))
            return ''

    field_spec = [('bpa_id', 'BPA ID', set_id),
                  ('sample_id', 'Sample extraction ID', None),
                  ('genome_sequencing_facility', 'Genome Sequencing Facility', None),
                  ('date_received', 'Date Received by sequencing facility', ingest_utils.get_date),
                  ('comments', 'Comments by sequencing facility', None),
                  ('date_sequenced', 'Date sequenced', ingest_utils.get_date),
                  ('library', 'Library', get_library_type),
                  ('library_construction', 'Library Construction (insert size bp)', ingest_utils.get_clean_number),
                  ('library_protocol', 'Library construction protocol', None),
                  ('index', 'Index', ingest_utils.get_clean_number),
                  ('sequencer', 'Sequencer', None),
                  ('run', 'Run number', ingest_utils.get_clean_number),
                  ('flow_cell_id', 'Run #:Flow Cell ID', None),
                  ('lane_number', 'Lane number', ingest_utils.get_clean_number),
                  ('sequence_file_name', 'FILE NAMES - supplied by sequencing facility', None),
                  ('md5sum', 'MD5 Checksum', None),
                  ('date_data_sent', 'Date data sent/transferred', ingest_utils.get_date),
                  ]

    wrapper = ExcelWrapper(field_spec,
                           file_name,
                           sheet_name='BASE Metagenomics',
                           header_length=1,
                           column_name_row_index=0)

    return wrapper.get_all()


def get_sample(entry):
    """
    Get the Sample by bpa_id
    """
    bpa_id = _get_bpa_id(entry)
    if bpa_id is None:
        return None

    sample, created = MetagenomicsSample.objects.get_or_create(bpa_id=bpa_id)
    if created:
        sample.name = entry.sample_id
        sample.dna_extraction_protocol = entry.library_protocol
        sample.requested_sequence_coverage = entry.library_construction
        sample.collection_date = entry.date_received
        sample.debug_note = ingest_utils.pretty_print_namedtuple(entry)
        sample.save()
        logger.debug('Adding Metagenomics Sample ' + bpa_id.bpa_id)

    return sample


def get_run(entry):
    def get_sequencer(name):
        if name == '':
            name = 'Unknown'

        sequencer, _ = Sequencer.objects.get_or_create(name=name)
        return sequencer

    def get_facility(name):
        if name == '':
            name = 'Unknown'

        facility, _ = Facility.objects.get_or_create(name=name)
        return facility

    met_run, created = MetagenomicsRun.objects.get_or_create(sample=get_sample(entry))
    if created:
        logger.info('New metagenomics run created')

        met_run.flow_cell_id = entry.flow_cell_id.strip()
        met_run.run_number = entry.run
        met_run.index_number = entry.index
        met_run.sequencer = get_sequencer(entry.sequencer.strip())
        met_run.lane_number = entry.lane_number
        met_run.genome_sequencing_facility = get_facility(entry.genome_sequencing_facility)
        met_run.save()

    return met_run


def add_sequence_files(data):
    """
    Add sequence files
    """
    for file_row in data:
        sample = get_sample(file_row)
        if sample is None:
            logger.warning('Could not add sample {0}'.format(sample))
            continue

        sequence_file = MetagenomicsSequenceFile()
        sequence_file.sample = sample
        sequence_file.filename = file_row.sequence_file_name
        sequence_file.md5 = file_row.md5sum
        sequence_file.index_number = file_row.index
        sequence_file.lane_number = file_row.lane_number
        sequence_file.date_received_from_sequencing_facility = file_row.date_received
        sequence_file.note = file_row.comments
        sequence_file.run = get_run(file_row)

        sequence_file.save()


def do_metadata():
    def is_metadata(path):
        if path.isfile() and path.ext == '.xlsx':
            return True

    logger.info('Ingesting BASE Metagenomics metadata from {0}'.format(DATA_DIR))
    for metadata_file in DATA_DIR.walk(filter=is_metadata):
        logger.info('Processing BASE Metagenomics Metadata file {0}'.format(metadata_file))
        samples = list(get_data(metadata_file))
        add_sequence_files(samples)


def run():
    # get_all_metadata_from_server()
    fetcher = Fetcher(DATA_DIR, METADATA_URL, auth=('base', 'b4s3'))
    fetcher.fetch_metadata_from_folder()

    do_metadata()

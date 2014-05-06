# -*- coding: utf-8 -*-

from unipath import Path

from libs.excel_wrapper import ExcelWrapper
from libs import ingest_utils
from libs import bpa_id_utils
from libs import logger_utils

from apps.base_amplicon.models import AmpliconSequencingMetadata
from apps.common.models import Facility

logger = logger_utils.get_logger(__name__)

# all the Excel sheets and md5sums should be in here
DATA_DIR = Path(Path('~').expand_user(), 'var/amplicon_metadata/')

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
                  ('sequencing_facility', 'Sequencing facility', None),
                  ('target', 'Target', lambda s: s.upper().strip()),
                  ('index', 'Index', None),
                  ('pcr_1_to_10', '1:10 PCR, P=pass, F=fail', None),
                  ('pcr_1_to_100', '1:100 PCR, P=pass, F=fail', None),
                  ('pcr_neat', 'neat PCR, P=pass, F=fail', None),
                  ('dilution', 'Dilution used', None),
                  ('sequencing_run_number', 'Sequencing run number', None),
                  ('flow_cell_id', 'Flowcell', None),
                  ('reads', '# of reads', ingest_utils.get_int),
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


def add_samples(data):
    """
    Add sequence files
    """
    for entry in data:
        bpa_id = get_bpa_id(entry)
        if bpa_id is None:
            logger.warning('Could not add entry on row {0}'.format(entry.row))
            continue

        metadata, created = AmpliconSequencingMetadata.objects.get_or_create(bpa_id=bpa_id)

        metadata.sample_extraction_id = entry.sample_extraction_id
        metadata.name = entry.name

        metadata.sequencing_facility = Facility.objects.add(entry.sequencing_facility)
        metadata.index = entry.index
        metadata.target = entry.target
        metadata.pcr_1_to_10 = entry.pcr_1_to_10
        metadata.pcr_1_to_100 = entry.pcr_1_to_100
        metadata.pcr_neat = entry.pcr_neat
        # metadata.dilution = entry.dilution FIXME
        metadata.sequencing_run_number = entry.sequencing_run_number
        metadata.flow_cell_id = entry.flow_cell_id
        metadata.analysis_software_version = entry.analysis_software_version
        metadata.reads = entry.reads
        metadata.comments = entry.comments
        metadata.debug_note = ingest_utils.pretty_print_namedtuple(entry)

        metadata.save()


def is_metadata(path):
    if path.isfile() and path.ext == '.xlsx':
        return True


def run():
    # find all the spreadsheets in the data directory and ingest them
    logger.info('Ingesting BASE Amplicon metadata from {0}'.format(DATA_DIR))
    for metadata_file in DATA_DIR.walk(filter=is_metadata):
        logger.info('Processing BASE Amplicon Metadata file {0}'.format(metadata_file))
        samples = list(get_data(metadata_file))
        add_samples(samples)



# -*- coding: utf-8 -*-

from unipath import Path
from libs import bpa_id_utils
from libs import ingest_utils
from libs import management_command
from libs.excel_wrapper import ExcelWrapper
from libs.fetch_data import Fetcher, get_password

from ...models import SepsisSample, SampleTrack
from apps.common.models import Facility

from libs.logger_utils import get_logger
logger = get_logger(__name__)

BPA_ID = "102.100.100"
PROJECT_ID = "Sepsis"
PROJECT_DESCRIPTION = "Sepsis"

SEPSIS_ID_FILE = "sepsis_tracking.xlsx"
METADATA_PATH = "sepsis/projectdata"
DATA_DIR = Path(ingest_utils.METADATA_ROOT, METADATA_PATH)

def has_data(val):
    return True if val else False

def set_track(bpa_id, entry):
    """ Note tracking data """

    track, _ = SampleTrack.objects.get_or_create(bpa_id=bpa_id)
    track.given_to = entry.given_to
    track.allocation_date = entry.allocation_date
    track.sample_submission_date = entry.sample_submission_date
    track.replicate = entry.replicate
    track.work_order = entry.work_order
    track.omics = entry.omics
    track.analytical_platform = entry.analytical_platform
    track.facility, _ = Facility.objects.get_or_create(name=entry.facility)
    track.data_generated = entry.data_generated
    track.archive_ingestion_date = entry.archive_ingestion_date
    track.save()


def add_sepsis_id_data(data):
    """ pack the sepsis ID's into the DB """

    for entry in data:

        # do not process unallocated ID's
        given_to = entry.given_to.strip()
        if given_to is "":
            continue

        bpa_id, report = bpa_id_utils.get_bpa_id(entry.bpa_id, PROJECT_ID, PROJECT_DESCRIPTION, add_prefix=True)
        if not bpa_id:
            logger.info("Non BPA encountered when I expected one {}".format(report))
            continue

        # TODO verify what is intended in the source doc
        track, _ = SampleTrack.objects.get_or_create(bpa_id=bpa_id)
        track.given_to = entry.given_to
        track.allocation_date = entry.allocation_date
        track.sample_submission_date = entry.sample_submission_date
        track.replicate = entry.replicate
        track.work_order = entry.work_order
        track.omics = entry.omics
        track.analytical_platform = entry.analytical_platform
        track.facility, _ = Facility.objects.get_or_create(name=entry.facility)
        track.save()



def add_pacbio_tracking(data):
    """ pack the sepsis PacBio tracking data into the DB """

    for entry in data:

        bpa_id, report = bpa_id_utils.get_bpa_id(entry.bpa_id, PROJECT_ID, PROJECT_DESCRIPTION, add_prefix=True)
        if not bpa_id:
            logger.info("Non BPA encountered when I expected one {}".format(report))
            continue

        set_track(bpa_id, entry)


def add_miseq_tracking(data):
    """ pack the sepsis miseq tracking data into the DB """

    for entry in data:

        bpa_id, report = bpa_id_utils.get_bpa_id(entry.bpa_id, PROJECT_ID, PROJECT_DESCRIPTION, add_prefix=True)
        if not bpa_id:
            logger.info("Non BPA encountered when I expected one {}".format(report))
            continue

        set_track(bpa_id, entry)


def ingest_ids():
    def is_metadata(path):
        if path.isfile() and path.ext == ".xlsx":
            return True

    logger.info("Ingesting Sepsis BPA ID metadata from {0}".format(DATA_DIR))
    for metadata_file in DATA_DIR.walk(filter=is_metadata):
        logger.info("Processing Sepsis BPA ID file {0}".format(metadata_file))
        # allocated ID's
        sepsis_ids = list(get_ids(metadata_file))
        add_sepsis_id_data(sepsis_ids)

        # PacBio
        pacbio = list(get_pacbio(metadata_file))
        add_pacbio_tracking(pacbio)

        # MiSeq
        miseq = list(get_miseq(metadata_file))
        add_miseq_tracking(miseq)


def get_miseq(file_name):
    """ Parse fields from the metadata spreadsheet """

    # BPA ID
    # Date allocated
    # Taxon_OR_organism
    # Strain_OR_isolate
    # Serovar
    # Work order #
    # Replicate
    # Omics
    # Analytical platform
    # Facility
    # Sample Submission Date
    # Contextual Data Submission Date
    # Data generated
    # Archive ID
    # Archive Ingestion Date

    def strip_id(bpa_id):
        if bpa_id and bpa_id is not "":
            return bpa_id.split('/')[1]
        return None


    field_spec = [
        ("sample_number", "NUMBER", None),
        ("bpa_id", "BPA ID", strip_id),
        ("given_to", "Given to", None),
        ("allocation_date", "Date allocated", ingest_utils.get_date),
        ("taxon_or_organism", "Taxon_OR_organism", None),
        ("strain_or_isolate", "Strain_OR_isolate", None),
        ("serovar", "Serovar", None),
        ("work_order", "Work order #", None),
        ("replicate", "Replicate", ingest_utils.get_int),
        ("omics", "Omics", None),
        ("analytical_platform", "Analytical platform", None),
        ("facility", "Facility", None),
        ("sample_submission_date", "Sample Submission Date", ingest_utils.get_date),
        ("data_generated", "Data generated", has_data),
        ("archive_id", "Archive ID", None),
        ("archive_ingestion_date", "Archive Ingestion Date", ingest_utils.get_date),
    ]

    wrapper = ExcelWrapper(field_spec,
                           file_name,
                           sheet_name="MiSeq",
                           header_length=1,
                           column_name_row_index=0,
                           formatting_info=True)

    return wrapper.get_all()


def get_pacbio(file_name):
    """ Parse fields from the metadata spreadsheet """

    # NUMBER
    # BPA ID
    # Given to
    # Date allocated
    # Taxon_OR_organism
    # Strain_OR_isolate
    # Serovar
    # Work order #
    # Replicate
    # Omics
    # Analytical platform
    # Facility
    # Sample Submission Date
    # Contextual Data Submission Date
    # Data generated
    # Archive ID
    # Archive Ingestion Date

    def strip_id(bpa_id):
        if bpa_id and bpa_id is not "":
            return bpa_id.split('/')[1]
        return None

    field_spec = [
        ("sample_number", "NUMBER", None),
        ("bpa_id", "BPA ID", strip_id),
        ("given_to", "Given to", None),
        ("allocation_date", "Date allocated", ingest_utils.get_date),
        ("taxon_or_organism", "Taxon_OR_organism", None),
        ("strain_or_isolate", "Strain_OR_isolate", None),
        ("serovar", "Serovar", None),
        ("work_order", "Work order #", None),
        ("replicate", "Replicate", ingest_utils.get_int),
        ("omics", "Omics", None),
        ("analytical_platform", "Analytical platform", None),
        ("facility", "Facility", None),
        ("sample_submission_date", "Sample Submission Date", ingest_utils.get_date),
        ("data_generated", "Data generated", has_data),
        ("archive_id", "Archive ID", None),
        ("archive_ingestion_date", "Archive Ingestion Date", ingest_utils.get_date),
    ]

    wrapper = ExcelWrapper(field_spec,
                           file_name,
                           sheet_name="PacBio",
                           header_length=1,
                           column_name_row_index=0,
                           formatting_info=True)

    return wrapper.get_all()


def get_ids(file_name):
    """ Parse fields from the metadata spreadsheet """

    # NUMBER
    # BPA ID
    # Given to
    # Date allocated
    # Taxon_OR_organism
    # Strain_OR_isolate
    # Serovar
    # Work order #
    # Replicate
    # Omics
    # Analytical platform
    # Facility
    # Sample Submission Date
    # Contextual Data Submission Date
    # Data generated
    # Archive ID
    # Archive Ingestion Date

    def strip_id(bpa_id):
        if bpa_id and bpa_id is not "":
            return bpa_id.split('/')[1]
        return None

    field_spec = [
        ("sample_number", "NUMBER", None),
        ("bpa_id", "BPA ID", strip_id),
        ("given_to", "Given to", None),
        ("allocation_date", "Date allocated", ingest_utils.get_date),
        ("taxon_or_organism", "Taxon_OR_organism", None),
        ("strain_or_isolate", "Strain_OR_isolate", None),
        ("serovar", "Serovar", None),
        ("work_order", "Work order #", None),
        ("replicate", "Replicate", ingest_utils.get_int),
        ("omics", "Omics", None),
        ("analytical_platform", "Analytical platform", None),
        ("facility", "Facility", None),
        ("sample_submission_date", "Sample Submission Date", ingest_utils.get_date),
        ("data_generated", "Data generated", has_data),
        ("archive_id", "Archive ID", None),
        ("archive_ingestion_date", "Archive Ingestion Date", ingest_utils.get_date),
    ]

    wrapper = ExcelWrapper(field_spec,
                           file_name,
                           sheet_name="Unique_IDs",
                           header_length=1,
                           column_name_row_index=0,
                           formatting_info=True)

    return wrapper.get_all()


class Command(management_command.BPACommand):
    help = 'Ingest Sepsis Project tracking data'

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument('--delete',
                            action='store_true',
                            dest='delete',
                            default=False,
                            help='Delete all tracking data', )

    def handle(self, *args, **options):

        if options['delete']:
            logger.info("Deleting all Sample Tracking Information")
            SampleTrack.objects.all().delete()

        fetcher = Fetcher(DATA_DIR, self.get_base_url(options) + METADATA_PATH, auth=("sepsis", get_password('sepsis')))
        fetcher.clean()
        fetcher.fetch(SEPSIS_ID_FILE)
        ingest_ids()

# -*- coding: utf-8 -*-

from django.db.utils import DataError
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from unipath import Path
from apps.common.models import Facility
from libs import bpa_id_utils
from libs import ingest_utils
from libs.excel_wrapper import ExcelWrapper
from libs.fetch_data import Fetcher, get_password

from ...models import SepsisSample, SampleTrack

from libs.logger_utils import get_logger
logger = get_logger(__name__)

BPA_ID = "102.100.100"
PROJECT_ID = "Sepsis"
PROJECT_DESCRIPTION = "Sepsis"

# TODO get mirror urls from DB
METADATA_URL = "https://downloads-mu.bioplatforms.com/bpa/sepsis/projectdata/"
SEPSIS_ID_FILE= "sepsis_id.xlsx"
DATA_DIR = Path(ingest_utils.METADATA_ROOT, "sepsis/metadata/projectdata")

def add_sepsis_id_data(data):
    """ pack the sepsis ID's into the DB """

    for entry in data:
        bpa_id, report = bpa_id_utils.get_bpa_id(entry.bpa_id, PROJECT_ID, PROJECT_DESCRIPTION, add_prefix=True)
        if not bpa_id:
            logger.info("Non BPA encountered when I expected one {}".format(report))
            continue

        sample, _ = SepsisSample.objects.get_or_create(bpa_id=bpa_id)
        # just fill in everything available from this spreadsheet
        if sample:
            sample.taxon_or_organism = entry.taxon_or_organism
            sample.strain_or_isolate = entry.strain_or_isolate
            sample.serovar = entry.serovar
            sample.contact_researcher = entry.given_to
            sample.save()

        #if method:
        #    files = GenomicsMiseqFile.objects.filter(sample__bpa_id=bpa_id)
        #    for f in files:
        #        f.method = method
        #        f.save()

def ingest_ids():
    def is_metadata(path):
        if path.isfile() and path.ext == ".xlsx":
            return True

    logger.info("Ingesting Sepsis BPA ID metadata from {0}".format(DATA_DIR))
    for metadata_file in DATA_DIR.walk(filter=is_metadata):
        logger.info("Processing Sepsis BPA ID file {0}".format(metadata_file))
        sepsis_ids = list(get_ids(metadata_file))
        add_sepsis_id_data(sepsis_ids)


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
        ("allocation_date", "Date allocated", None),
        ("taxon_or_organism", "Taxon_OR_organism", None),
        ("strain_or_isolate", "Strain_OR_isolate", None),
        ("serovar", "Serovar", None),
        ("work_order", "Work order #", None),
        ("replicate", "Replicate", None),
        ("omics", "Omics", None),
        ("analytical_platform", "Analytical platform", None),
        ("facility", "Facility", None),
        ("sample_submission_date", "Sample Submission Date", None),
        ("data_generated", "Data generated", None),
        ("archive_id", "Archive ID", None),
        ("archive_ingestion_date", "Archive Ingestion Date", None),
    ]

    wrapper = ExcelWrapper(field_spec,
                           file_name,
                           sheet_name="Sepsis_Unique_IDs_23-12-2015",
                           header_length=1,
                           column_name_row_index=0,
                           formatting_info=True,
                           pick_first_sheet=True)

    return wrapper.get_all()


class Command(BaseCommand):
    help = 'Ingest Sepsis Project metadata'

    def handle(self, *args, **options):
        password = get_password('sepsis')
        # fetch the new data formats
        fetcher = Fetcher(DATA_DIR, METADATA_URL, auth=("sepsis", password))
        fetcher.clean()
        fetcher.fetch(SEPSIS_ID_FILE) # TODO pass file arg 
        ingest_ids()

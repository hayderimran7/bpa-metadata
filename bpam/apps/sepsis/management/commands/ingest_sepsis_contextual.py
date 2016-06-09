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

from ...models import SepsisSample, GrowthMethod, Host

from libs.logger_utils import get_logger
logger = get_logger(__name__)

BPA_ID = "102.100.100"
PROJECT_ID = "Sepsis"
PROJECT_DESCRIPTION = "Sepsis"

# TODO get mirror urls from DB
METADATA_URL = "https://downloads-mu.bioplatforms.com/bpa/sepsis/projectdata/"
SEPSIS_ID_FILE = "sepsis_contextual.xlsx"
DATA_DIR = Path(ingest_utils.METADATA_ROOT, "sepsis/metadata/projectdata")


def add_data(data):
    """ pack data into the DB """

    for entry in data:
        bpa_id, report = bpa_id_utils.get_bpa_id(entry.bpa_id,
                                                 PROJECT_ID,
                                                 PROJECT_DESCRIPTION,
                                                 add_prefix=True)
        if not bpa_id:
            logger.info(
                "Non BPA encountered when I expected one {}, skipping".format(
                    report))
            continue

        sample, _ = SepsisSample.objects.get_or_create(bpa_id=bpa_id)
        # just fill in everything available from this spreadsheet
        if sample:
            sample.taxon_or_organism = entry.taxon_or_organism
            sample.strain_or_isolate = entry.strain_or_isolate
            sample.serovar = entry.serovar
            sample.key_virulence_genes = entry.key_virulence_genes
            sample.gram_stain = entry.gram_stain
            sample.isolation_source = entry.isolation_source
            sample.publication_reference = entry.publication_reference
            sample.contact_researcher = entry.contact_researcher
            sample.culture_collection_date = entry.culture_collection_date

            growth, _ = GrowthMethod.objects.get_or_create(
                growth_condition_time=entry.growth_condition_time,
                growth_condition_temperature=entry.growth_condition_temperature,
                growth_condition_media=entry.growth_condition_media, )
            sample.growth = growth

            host, _ = Host.objects.get_or_create(
                description=entry.host_description,
                location=entry.host_location,
                sex=entry.host_sex,
                age=entry.host_age,
                dob=entry.host_dob,
                disease_outcome=entry.disease_outcome,
                strain_or_isolate=entry.strain_or_isolate, )
            sample.host = host

            sample.save()


def ingest_data():
    def is_metadata(path):
        if path.isfile() and path.ext == ".xlsx":
            return True

    logger.info("Ingesting Sepsis BPA COntextual metadata from {0}".format(
        DATA_DIR))
    for metadata_file in DATA_DIR.walk(filter=is_metadata):
        logger.info("Processing Sepsis BPA Contextual file {0}".format(
            metadata_file))
        data = list(get_data(metadata_file))
        add_data(data)


def get_data(file_name):
    """ Parse fields from the metadata spreadsheet """

    # BPA_sample_ID
    # Gram_staining_(positive_or_negative)
    # Taxon_OR_organism
    # Strain_OR_isolate
    # Serovar
    # Key_virulence_genes
    # Strain_description
    # Isolation_source
    # Publication_reference
    # Contact_researcher
    # Growth_condition_time
    # Growth_condition_temperature
    # Growth_condition_media
    # Experimental_replicate
    # Analytical_facility
    # Analytical_platform
    # Experimental_sample_preparation_method
    # Culture_collection_ID (alternative name[s])
    # Culture_collection_date (DD/MM/YY)
    # Host_location (state, country)
    # Host_age
    # Host_DOB (DD/MM/YY)
    # Host_sex (F/M)
    # Host_disease_outcome
    # Host_description

    def strip_id(bpa_id):
        if bpa_id and bpa_id is not "":
            return bpa_id.split('/')[1]
        return None

    def get_gram_stain(val):
        if val and val is not "":
            val = val.lower()
            if val.find("positive") != -1:
                return "POS"
            if val.find("negative") != -1:
                return "NEG"

        return None

    field_spec = [
        ("bpa_id", "BPA_sample_ID", strip_id),
        ("gram_stain", "Gram_staining_(positive_or_negative)", get_gram_stain),
        ("taxon_or_organism", "Taxon_OR_organism", None),
        ("strain_or_isolate", "Strain_OR_isolate", None),
        ("serovar", "Serovar", None),
        ("key_virulence_genes", "Key_virulence_genes", None),
        ("strain_description", "Strain_description", None),
        ("publication_reference", "Publication_reference", None),
        ("contact_researcher", "Contact_researcher", None),
        ("growth_condition_time", "Growth_condition_time", None),
        ("growth_condition_temperature", "Growth_condition_temperature", None),
        ("growth_condition_media", "Growth_condition_media", None),
        ("experimental_replicate", "Experimental_replicate", None),
        ("analytical_facility", "Analytical_facility", None),
        ("analytical_platform", "Analytical_platform", None),
        ("experimental_sample_preparation_method",
         "Experimental_sample_preparation_method", None),
        ("culture_collection_id",
         "Culture_collection_ID (alternative name[s])", None),
        ("culture_collection_date", "Culture_collection_date (DD/MM/YY)",
         ingest_utils.get_date),
        ("host_location", "Host_location (state, country)", None),
        ("host_age", "Host_age", None),
        ("host_dob", "Host_DOB (DD/MM/YY)", ingest_utils.get_date),
        ("host_sex", "Host_sex (F/M)", None),
        ("host_disease_outcome", "Host_disease_outcome", None),
        ("isolation_source", "Isolation_source", None),
        ("host_description", "Host_description", None),
    ]

    wrapper = ExcelWrapper(field_spec,
                           file_name,
                           sheet_name="Sheet1",
                           header_length=5,
                           column_name_row_index=4,
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
        fetcher.fetch(SEPSIS_ID_FILE)  # TODO pass file arg
        ingest_data()

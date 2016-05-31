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

from ...models import GenomicsFile, SepsisSample
from .. import md5parser

from libs.logger_utils import get_logger
logger = get_logger(__name__)

BPA_ID = "102.100.100"
PROJECT_ID = "Sepsis"
PROJECT_DESCRIPTION = "Sepsis"

# TODO get mirror urls from DB
METADATA_URL = "https://downloads-mu.bioplatforms.com/bpa/sepsis/genomics/miseq/"
DATA_DIR = Path(ingest_utils.METADATA_ROOT, "sepsis/metadata/genomics/miseq")


def _get_index(entry):
    """
    Archial amplicons have more than one index, take all available indexi and bunch them into
    a single string. So be it.
    """
    indexi = []
    for i in (entry.index1, entry.index2):
        if i is not None:
            i = i.strip()
            if i is not "":
                indexi.append(i)
    return ", ".join(indexi)


def add_samples(data):
    """
    Add sequence files
    """
    for entry in data:
        bpa_id, report = bpa_id_utils.get_bpa_id(entry.bpa_id, PROJECT_ID, PROJECT_DESCRIPTION)
        if not bpa_id:
            continue

        metadata, created = AmpliconSequencingMetadata.objects.get_or_create(bpa_id=bpa_id, target=entry.target)

        metadata.sample_extraction_id = entry.sample_extraction_id
        metadata.name = entry.name

        # This may be set by older formats here, or later from md5


        if entry.sequencing_facility is not None:
            metadata.sequencing_facility = Facility.objects.add(entry.sequencing_facility)

        metadata.index = _get_index(entry)
        metadata.pcr_1_to_10 = entry.pcr_1_to_10
        metadata.pcr_1_to_100 = entry.pcr_1_to_100
        metadata.pcr_neat = entry.pcr_neat
        metadata.dilution = entry.dilution.upper()
        metadata.sequencing_run_number = entry.sequencing_run_number
        metadata.flow_cell_id = entry.flow_cell_id
        metadata.analysis_software_version = entry.analysis_software_version
        metadata.reads = entry.reads
        metadata.comments = entry.comments
        metadata.debug_note = ingest_utils.pretty_print_namedtuple(entry)

        try:
            metadata.save()
        except DataError as e:
            logger.error(e)
            logger.error(entry)
            exit()


def do_metadata():
    def is_metadata(path):
        if path.isfile() and path.ext == ".xlsx":
            return True

    logger.info("Ingesting GBR Amplicon metadata from {0}".format(DATA_DIR))
    for metadata_file in DATA_DIR.walk(filter=is_metadata):
        logger.info("Processing GBR Amplicon Metadata file {0}".format(metadata_file))
        samples = list(get_metadata(metadata_file))
        add_samples(samples)


def get_metadata(file_name):
    """
    Parse fields from the metadata spreadsheet
    """

    field_spec = [
        ("bpa_id", "Sample unique ID", lambda s: s.replace("/", ".")),
        ("sample_extraction_id", "Sample extraction ID", ingest_utils.get_int),
        ("sequencing_facility", "Sequencing facility", None),
        ("target", "Target", lambda s: s.upper().strip()),
        ("i7_index", "I7_Index_ID", None),
        ("index1", "index", None),
        ("index2", "index2", None),
        ("pcr_1_to_10", "1:10 PCR, P=pass, F=fail", fix_pcr),
        ("pcr_1_to_100", "1:100 PCR, P=pass, F=fail", fix_pcr),
        ("pcr_neat", "neat PCR, P=pass, F=fail", fix_pcr),
        ("dilution", "Dilution used", fix_dilution),
        ("sequencing_run_number", "Sequencing run number", None),
        ("flow_cell_id", "Flowcell", None),
        ("reads", "# of reads", ingest_utils.get_int),
        ("name", "Sample name on sample sheet", None),
        ("analysis_software_version", "AnalysisSoftwareVersion", None),
        ("comments", "Comments", None),
    ]

    wrapper = ExcelWrapper(field_spec,
                           file_name,
                           sheet_name="Sheet1",
                           header_length=4,
                           column_name_row_index=1,
                           formatting_info=True,
                           pick_first_sheet=True)

    return wrapper.get_all()

def add_md5(md5_lines):
    """ Add md5 data """

    for md5_line in md5_lines:
        bpa_idx = md5_line.md5data.get('id')
        bpa_id, report = bpa_id_utils.get_bpa_id(bpa_idx, PROJECT_ID, PROJECT_DESCRIPTION, add_prefix=True)

        if bpa_id is None:
            continue

        sample, _ = SepsisSample.objects.get_or_create(bpa_id=bpa_id)

        f, _ = GenomicsFile.objects.get_or_create(
            sample=sample,
            #read_number=md5_line.md5data.get('read'),
            #lane=md5_line.md5data.get('lane'),
            filename=md5_line.filename,
            md5=md5_line.md5)


def ingest_md5():
    """ Ingest the md5 files """
    def is_md5file(path):
        if path.isfile() and path.ext == ".md5":
            return True

    logger.info("Ingesting Sepsis md5 file information from {0}".format(DATA_DIR))
    for md5_file in DATA_DIR.walk(filter=is_md5file):
        logger.info("Processing Sepsis Genomic md5 file {0}".format(md5_file))
        data = md5parser.parse_md5_file(md5parser.miseq_filename_pattern, md5_file)
        print(data)
        add_md5(data)

class Command(BaseCommand):
    help = 'Ingest Sepsis Genomics miseq metadata'

    def handle(self, *args, **options):
        password = get_password('sepsis')
        # fetch the new data formats
        fetcher = Fetcher(DATA_DIR, METADATA_URL, auth=("sepsis", password))
        fetcher.clean()
        fetcher.fetch_metadata_from_folder()

        ingest_md5()

# -*- coding: utf-8 -*-

from unipath import Path
from libs import bpa_id_utils
from libs import ingest_utils
from libs import management_command
from libs.excel_wrapper import ExcelWrapper
from libs.fetch_data import Fetcher, get_password

from ...models import PacBioGenomicsMethod, GenomicsPacBioFile, SepsisSample
from .. import md5parser

from libs.logger_utils import get_logger
logger = get_logger(__name__)

BPA_ID = "102.100.100"
PROJECT_ID = "Sepsis"
PROJECT_DESCRIPTION = "Sepsis"

METADATA_PATH = "sepsis/genomics/pacbio/"
DATA_DIR = Path(ingest_utils.METADATA_ROOT, METADATA_PATH)


def add_method_data(data):
    """ Add method data to files """

    for entry in data:
        bpa_id, report = bpa_id_utils.get_bpa_id(entry.bpa_id, PROJECT_ID, PROJECT_DESCRIPTION, add_prefix=True)
        if not bpa_id:
            logger.info("Non BPA encountered when I expected one {}".format(report))
            continue

        args = entry._asdict()
        # get rid of keys that confuses get_or_create
        args.pop('bpa_id', None)
        args.pop('file_name', None)
        args.pop('row', None)
        method, _ = PacBioGenomicsMethod.objects.get_or_create(**args)
        if method:
            files = GenomicsPacBioFile.objects.filter(sample__bpa_id=bpa_id)
            for f in files:
                f.method = method
                f.save()


def do_metadata():
    def is_metadata(path):
        if path.isfile() and path.ext == ".xlsx":
            return True

    logger.info("Ingesting Sepsis Genomics PacBio metadata from {0}".format(DATA_DIR))
    for metadata_file in DATA_DIR.walk(filter=is_metadata):
        logger.info("Processing Sepsis Genomics metadata file {0}".format(metadata_file))
        methods = list(get_metadata(metadata_file))
        add_method_data(methods)


def get_metadata(file_name):
    """ Parse fields from the metadata spreadsheet """

    def get_bpa_id(val):
        if not val or val is "":
            return None
        return val.replace("102.100.100/", "")

    field_spec = [
        ("bpa_id", "Bacterial sample unique ID", get_bpa_id),
        ("insert_size_range", "Insert size range", None),
        ("library_construction_protocol", "Library construction protocol", None),
        ("sequencer", "Sequencer", None),
        ("sequencer_run_id", "Run ID", None),
        ("smrt_cell_id", "SMRT Cell ID", None),
        ("cell_position", ("Cell Postion", "Cell Position"), None),
        ("rs_version", "RS Version", None),
    ]

    wrapper = ExcelWrapper(field_spec,
                           file_name,
                           sheet_name="Sheet1",
                           header_length=2,
                           column_name_row_index=1,
                           formatting_info=True,
                           pick_first_sheet=True)

    return wrapper.get_all()


def add_md5(md5_lines):
    """ Unpack md5 data to database """

    for md5_line in md5_lines:
        # add bpa id
        bpa_idx = md5_line.md5data.get('id')
        bpa_id, report = bpa_id_utils.get_bpa_id(bpa_idx, PROJECT_ID, PROJECT_DESCRIPTION, add_prefix=True)

        if bpa_id is None:
            continue

        # add samples
        sample, _ = SepsisSample.objects.get_or_create(bpa_id=bpa_id)

        # add files
        f, _ = GenomicsPacBioFile.objects.get_or_create(note="Ingested using management command",
                                                        sample=sample,
                                                        vendor=md5_line.md5data.get('vendor'),
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
        data = md5parser.parse_md5_file(md5parser.pacbio_filename_pattern, md5_file)
        add_md5(data)


class Command(management_command.BPACommand):
    help = 'Ingest Sepsis Genomics PacBio metadata'

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument('--delete',
                            action='store_true',
                            dest='delete',
                            default=False,
                            help='Delete all contextual data', )

    def handle(self, *args, **options):

        if options['delete']:
            logger.info("Deleting all PacBio Files")
            GenomicsPacBioFile.objects.all().delete()

        # fetch the new data formats
        fetcher = Fetcher(DATA_DIR, self.get_base_url(options) + METADATA_PATH, auth=("sepsis", get_password('sepsis')))
        fetcher.clean()
        fetcher.fetch_metadata_from_folder()
        ingest_md5()
        do_metadata()

# -*- coding: utf-8 -*-
"""
Ingests Marine Microbe Metagenomic metadata from archive into database.
"""

from unipath import Path

from libs import ingest_utils
from libs import management_command
from libs.excel_wrapper import ExcelWrapper
from libs.fetch_data import Fetcher
from apps.common.models import Facility

from ...models import Metagenomic
from ...models import MMSample
from ...models import MetagenomicSequenceFile

METADATA_PATH = "marine_microbes/metadata"
DATA_DIR = Path(ingest_utils.METADATA_ROOT, METADATA_PATH)


class Command(management_command.BPACommand):
    help = 'Ingest Marine Microbes Metagenomics'

    def _get_data(self, file_name):
        """ The data sets is relatively small, so make a in-memory copy to simplify some operations. """

        field_spec = [
            ("sample_extraction_id", "Sample extraction ID", None),
            ("sequencing_facility", "Sequencing facility", None),
        ]

        wrapper = ExcelWrapper(field_spec,
                               file_name,
                               sheet_name="Sheet1",
                               header_length=4,
                               column_name_row_index=1,
                               formatting_info=True,
                               pick_first_sheet=True)

        return wrapper.get_all()

    def _get_facility_name_from_filename(self, filename):
        """ If facility is not noted in spreadsheet, get it from the filename """

        if filename is None:
            self.log_warn("Filename not set")
            return "UNKNOWN"

        parts = filename.split('_')
        if len(parts) >= 2:
            return parts[2]  # the vendor should be at [2] Marine Microbes_metagenomics_AGRF_H32M7BCXX_metadata.xlsx
        else:
            self.log_warn("Filename {} mallformed".format(filename))
            return "UNKNOWN"

    def _get_facility(self, entry):
        name = entry.sequencing_facility
        if name is None:
            name = self._get_facility_name_from_filename(entry.file_name)

        name = name.strip()
        if name == "":
            name = "UNKNOWN"
        facility, _ = Facility.objects.get_or_create(name=name)
        return facility

    def _add_samples(self, data):
        """ Add sequence files """

        for entry in data:
            amplicon, _ = Metagenomic.objects.get_or_create(extraction_id=entry.sample_extraction_id,
                                                            facility=self._get_facility(entry),
                                                            metadata_filename=entry.file_name)

    def _ingest_metadata(self):
        def is_metadata(path):
            if path.isfile() and path.ext == ".xlsx":
                return True

        self.log_info("Ingesting Marine Microbes Metagenomic metadata from {0}".format(DATA_DIR))
        for metadata_file in DATA_DIR.walk(filter=is_metadata):
            self.log_info("Processing Marine Microbes  Metadata file {0}".format(metadata_file))
            samples = list(self._get_data(metadata_file))
            self._add_samples(samples)

    def truncate(self):
        from django.db import connection

        cursor = connection.cursor()
        cursor.execute("TRUNCATE TABLE {} CASCADE".format(MetagenomicSequenceFile._meta.db_table))

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument('--delete',
                            action='store_true',
                            dest='delete',
                            default=False,
                            help='Delete all data', )

    def handle(self, *args, **options):

        if options['delete']:
            self.log_info("Truncating MM Metagenomic Files data")
            self.truncate()

        fetcher = Fetcher(DATA_DIR, self.get_base_url(options) + METADATA_PATH)
        fetcher.clean()
        fetcher.fetch_metadata_from_folder()

        # find all the spreadsheets in the data directory and ingest them
        self._ingest_metadata()

        # find all the md5 files in the data directory and make metagenomic sequence file objects
        self._ingest_md5()

# -*- coding: utf-8 -*-

"""
Ingests Marine Microbes Amplicon metadata from server into database.
"""

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from ...models import Amplicon

from django.db.utils import DataError
from unipath import Path
import logging
import os

from bpatrack.libs.excel_wrapper import ExcelWrapper
from bpatrack.libs.fetch_data import Fetcher

from bpatrack.common.models import Facility
from bpatrack.base.models import Amplicon

METADATA_ROOT = os.path.join(os.path.expanduser('~'), 'bpametadata')

METADATA_URL = "https://downloads.bioplatforms.com/marine_microbes/tracking/amplicons/"
DATA_DIR = Path(METADATA_ROOT, "marine_microbes/amplicon_metadata/")

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Ingest Marine Microbe Amplicons'

    def _get_data(self, file_name):
        """ The data sets is relatively small, so make a in-memory copy to simplify some operations. """

        field_spec = [
                ("sample_extraction_id", "Sample extraction ID", None),
                ("sequencing_facility", "Sequencing facility", None),
                ("target", "Target", lambda s: s.upper().strip()),
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

    def _get_facility_name_from_filename(self, filename):
        """ If facility is not noted in spreadsheed, get it from the filename """

        if filename is None:
            logger.warn("Filename not set")
            return "UNKNOWN"

        parts = filename.split('_')
        if len(parts) >= 2:
            return parts[2] # the vendor should be at [2] BASE_ITS_UNSW_AGEFG_metadata.xlsx
        else:
            logger.warn("Filename mallformed")
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
            amplicon, _ = Amplicon.objects.get_or_create(
                    extraction_id=entry.sample_extraction_id,
                    facility=self._get_facility(entry),
                    target=entry.target,
                    metadata_filename=entry.file_name,
                    comments=entry.comments
                    )

    def _do_metadata(self):
        def is_metadata(path):
            if path.isfile() and path.ext == ".xlsx":
                return True

        self.stdout.write(self.style.SUCCESS("Ingesting Marine Microbe Amplicon metadata from {0}".format(DATA_DIR)))
        for metadata_file in DATA_DIR.walk(filter=is_metadata):
            self.stdout.write(self.style.SUCCESS("Processing Marine Microbe Amplicon Metadata file {0}".format(metadata_file)))
            samples = list(self._get_data(metadata_file))
            self._add_samples(samples)


    def handle(self, *args, **options):
        fetcher = Fetcher(DATA_DIR, METADATA_URL)
        fetcher.clean()
        fetcher.fetch_metadata_from_folder()

        # find all the spreadsheets in the data directory and ingest them
        self._do_metadata()

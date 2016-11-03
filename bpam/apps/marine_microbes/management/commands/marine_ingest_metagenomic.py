# -*- coding: utf-8 -*-
"""
Ingests Marine Microbe Metagenomic metadata from archive into database.
"""

from __future__ import print_function

import os
import re
from unipath import Path

from libs import ingest_utils
from libs import management_command
from libs import bpa_id_utils
from libs.excel_wrapper import ExcelWrapper
from libs.fetch_data import Fetcher, get_password
from libs.parse_md5 import parse_md5_file
from apps.common.models import Facility

from ...models import MMSample
from ...models import MetagenomicSequenceFile

METADATA_PATH = "marine_microbes/metagenomics"
DATA_DIR = Path(ingest_utils.METADATA_ROOT, METADATA_PATH)

# 21649_1_PE_680bp_MM_AGRF_H3VJJBCXX_TAGGCATG_L001_R1.fastq.gz
FILENAME_PATTERN = """
    (?P<id>\d{4,6})_
    (?P<extraction>\d)_
    (?P<library>PE|MP)_
    (?P<size>\d*bp)_
    MM_
    (?P<vendor>AGRF|UNSW)_
    (?P<flowcell>\w{9})_
    (?P<index>[G|A|T|C|-]*)_
    (?P<lane>L\d{3})_
    (?P<read>R[1|2])\.fastq\.gz
"""
filename_pattern = re.compile(FILENAME_PATTERN, re.VERBOSE)


class Command(management_command.BPACommand):
    help = 'Ingest Marine Microbes Metagenomics'

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.problem_xlsx = []
        self.ok_xlsx = []

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

        if wrapper.missing_headers:
            self.problem_xlsx.append((os.path.basename(file_name), wrapper.header + [], [t[1] for t in field_spec], wrapper.missing_headers + []))
        else:
            self.ok_xlsx.append(os.path.basename(file_name))
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

    def _add_metadata(self, data):
        """ Add metadata so samples from metadata spreadsheets """

        for entry in data:
            bpa_id, report = bpa_id_utils.get_bpa_id(entry.sample_extraction_id, "marine_microbes", "Marine Microbes", add_prefix=True)

            if bpa_id is None:
                self.log_warn(report)
                continue

            sample, _ = MMSample.objects.get_or_create(bpa_id=bpa_id)
            # TODO add metadata

    def _ingest_metadata(self):
        def is_metadata(path):
            if path.isfile() and path.ext == ".xlsx":
                return True

        self.log_info("Ingesting Marine Microbes Metagenomic metadata from {0}".format(DATA_DIR))
        for metadata_file in DATA_DIR.walk(filter=is_metadata):
            self.log_info("Processing Marine Microbes  Metadata file {0}".format(metadata_file))
            metadata = list(self._get_data(metadata_file))
            self._add_metadata(metadata)

    def add_md5(self, md5_lines):
        """ Unpack md5 data to database """

        for md5_line in md5_lines:
            # add bpa id
            bpa_idx = md5_line.md5data.get('id')
            bpa_id, report = bpa_id_utils.get_bpa_id(bpa_idx, "marine_microbes", "Marine Microbes", add_prefix=True)

            if bpa_id is None:
                self.log_warn(report)
                continue

            # add samples
            sample, _ = MMSample.objects.get_or_create(bpa_id=bpa_id)
            lane = int(md5_line.md5data.get('lane')[1:])

            # add files
            MetagenomicSequenceFile.objects.get_or_create(note="Ingested using management command",
                                                          sample=sample,
                                                          extraction=md5_line.md5data.get('extraction'),
                                                          library=md5_line.md5data.get('library'),
                                                          vendor=md5_line.md5data.get('vendor'),
                                                          size=md5_line.md5data.get('size'),
                                                          flow_cell=md5_line.md5data.get('flowcell'),
                                                          index=md5_line.md5data.get('index'),
                                                          lane_number=lane,
                                                          read=md5_line.md5data.get('read'),
                                                          filename=md5_line.filename,
                                                          md5=md5_line.md5)

    def _ingest_md5(self):
        """ Ingest the md5 files """

        def is_md5file(path):
            if path.isfile() and path.ext == ".md5":
                return True

        self.log_info("Ingesting Marine Microbes md5 file information from {0}".format(DATA_DIR))
        for md5_file in DATA_DIR.walk(filter=is_md5file):
            self.log_info("Processing Marine Microbes md5 file {0}".format(md5_file))
            data = parse_md5_file(filename_pattern, md5_file)
            self.add_md5(data)

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

        fetcher = Fetcher(DATA_DIR, self.get_base_url(options) + METADATA_PATH, auth=("marine", get_password('marine')))
        fetcher.clean()
        fetcher.fetch_metadata_from_folder()
        filename_url = fetcher.filename_url

        # find all the spreadsheets in the data directory and ingest them
        self._ingest_metadata()

        # find all the md5 files in the data directory and make metagenomic sequence file objects
        self._ingest_md5()

        # report on problems found during XLSX import
        print("Spreadsheets read without any issue:")
        for filename in self.ok_xlsx:
            print(filename_url[filename])
            print()

        print("Spreadsheet issues:")
        for filename, present_header, required_header, missing_headers in sorted(self.problem_xlsx, key=lambda t: filename_url[t[0]]):
            print("%s:" % filename_url[filename])
            print("    missing headers: %s" % ' ,'.join(repr(t) for t in missing_headers))
            print("     header present: %s" % ' ,'.join(repr(t) for t in present_header))
            print("    header required: %s" % ' ,'.join(repr(t) for t in required_header))
            print()

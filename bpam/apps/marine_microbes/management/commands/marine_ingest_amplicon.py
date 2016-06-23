# -*- coding: utf-8 -*-
"""
Ingests Marine Microbe Metagenomic amplicon metadata from archive into database.
"""

import re
from unipath import Path

from libs import ingest_utils
from libs import management_command
from libs import bpa_id_utils
from libs.excel_wrapper import ExcelWrapper
from libs.fetch_data import Fetcher
from libs.parse_md5 import parse_md5_file

from ...models import MMSample
from ...models import AmpliconSequenceFile

# 21878_1_A16S_UNSW_GGACTCCT-TATCCTCT_AP3JE_S17_L001_R1.fastq.gz
FILENAME_PATTERN = """
    (?P<id>\d{4,6})_
    (?P<extraction>\d)_
    (?P<amplicon>16S|18S|ITS|A16S)_
    (?P<vendor>AGRF|UNSW)_
    (?P<index>[G|A|T|C|-]*)_
    (?P<flowcell>\w{5})_
    (?P<runsamplenum>\S\d*)_
    (?P<lane>L\d{3})_
    (?P<read>[R|I][1|2])\.fastq\.gz
"""
filename_pattern = re.compile(FILENAME_PATTERN, re.VERBOSE)


class Command(management_command.BPACommand):
    help = 'Ingest Marine Microbes Amplicon'

    def fix_dilution(self, val):
        """
        Some source xcell files ship with the dilution column type as time.
        xlrd advertises support for format strings but not implemented.
        So stuff it.
        """
        if isinstance(val, float):
            return u"1:10"  # yea, that"s how we roll...
        return val

    def fix_pcr(self, pcr):
        """ Check pcr value """

        val = pcr.encode('utf-8').strip()
        if val not in ("P", "F", ""):
            self.log_error("PCR value [{}] is neither F, P or " ", setting to X".format(val))
            val = "X"
        return val

    def _get_data(self, file_name):
        """ The data sets is relatively small, so make a in-memory copy to simplify some operations. """

        field_spec = [
            ("bpa_id", "MM sample unique ID", lambda s: s.replace("/", ".")),
            ("pcr_1_to_10", "1:10 PCR, P=pass, F=fail", self.fix_pcr),
            ("pcr_1_to_100", "1:100 PCR, P=pass, F=fail", self.fix_pcr),
            ("pcr_neat", "neat PCR, P=pass, F=fail", self.fix_pcr),
            ("dilution", "Dilution used", self.fix_dilution),
            ("amplicon", "Target", None),
            ("number_of_reads", "# of reads", None),
            ("analysis_software_version", "AnalysisSoftwareVersion", None),
        ]

        wrapper = ExcelWrapper(field_spec,
                               file_name,
                               sheet_name="Sheet1",
                               header_length=3,
                               column_name_row_index=1,
                               formatting_info=True,
                               pick_first_sheet=True)

        return wrapper.get_all()

    def _add_samples(self, data):
        """ Add amplicon sequence files """

        for entry in data:
            bpa_id, report = bpa_id_utils.get_bpa_id(entry.bpa_id, "marine_microbes", "Marine Microbes")

            if bpa_id is None:
                self.log_warn("Metadata file {} row {} warning {}".format(entry.file_name, entry.row, report))
                continue

            # create MM sample for the entry found in the xcell metadata spreadsheet
            sample, _ = MMSample.objects.get_or_create(bpa_id=bpa_id)
            for amplicon_file in AmpliconSequenceFile.objects.filter(sample=sample, amplicon=entry.amplicon):
                amplicon_file.dilution = entry.dilution
                amplicon_file.pcr_1_to_10 = entry.pcr_1_to_10
                amplicon_file.pcr_1_to_100 = entry.pcr_1_to_100
                amplicon_file.pcr_neat = entry.pcr_neat
                amplicon_file.analysis_software_version = entry.analysis_software_version
                amplicon_file.number_of_reads = entry.number_of_reads
                amplicon_file.save()

    def _ingest_metadata(self, data_dir):
        def is_metadata(path):
            if path.isfile() and path.ext == ".xlsx":
                return True

        self.log_info("Ingesting Marine Microbes Metagenomic metadata from {0}".format(data_dir))
        for metadata_file in data_dir.walk(filter=is_metadata):
            self.log_info("Processing Marine Microbes  Metadata file {0}".format(metadata_file))
            samples = list(self._get_data(metadata_file))
            self._add_samples(samples)

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
            AmpliconSequenceFile.objects.get_or_create(note="Ingested using management command",
                                                       sample=sample,
                                                       extraction=md5_line.md5data.get('extraction'),
                                                       amplicon=md5_line.md5data.get('amplicon'),
                                                       vendor=md5_line.md5data.get('vendor'),
                                                       flow_cell=md5_line.md5data.get('flowcell'),
                                                       index=md5_line.md5data.get('index'),
                                                       lane_number=lane,
                                                       read=md5_line.md5data.get('read'),
                                                       filename=md5_line.filename,
                                                       md5=md5_line.md5)

    def _ingest_md5(self, data_dir):
        """ Ingest the md5 files """

        def is_md5file(path):
            if path.isfile() and path.ext == ".md5":
                return True

        self.log_info("Ingesting Marine Microbes md5 file information from {0}".format(data_dir))
        for md5_file in data_dir.walk(filter=is_md5file):
            self.log_info("Processing Marine Microbes md5 file {0}".format(md5_file))
            data = parse_md5_file(filename_pattern, md5_file)
            self.add_md5(data)

    def truncate(self):
        from django.db import connection

        cursor = connection.cursor()
        cursor.execute("TRUNCATE TABLE {} CASCADE".format(AmpliconSequenceFile._meta.db_table))
        # cursor.execute("TRUNCATE TABLE {} CASCADE".format(MMSample._meta.db_table))

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument('--delete',
                            action='store_true',
                            dest='delete',
                            default=False,
                            help='Delete all data', )

    def handle(self, *args, **options):

        if options['delete']:
            self.log_info("Truncating MM Amplicon Files data")
            self.truncate()

        for amplicon in ("a16s", "16s", "18s", "its"):
            self.log_info("Ingesting amplicon {}".format(amplicon))
            metadata_path = "marine_microbes/amplicons/{}".format(amplicon)
            data_dir = Path(ingest_utils.METADATA_ROOT, metadata_path)
            fetcher = Fetcher(data_dir, self.get_base_url(options) + metadata_path)
            fetcher.clean()
            fetcher.fetch_metadata_from_folder()

            # find all the md5 files in the data directory and make MM samples
            # as well as the amplicon sequence file's associated with them
            self._ingest_md5(data_dir)

            # find all the spreadsheets in the data directory and update the
            # amplicon files with the extra metadata
            self._ingest_metadata(data_dir)

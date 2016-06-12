# -*- coding: utf-8 -*-

from apps.common.models import Facility
from apps.gbr.models import GBRSample
from apps.gbr_amplicon.models import AmpliconSequenceFile, AmpliconSequencingMetadata
from django.db.utils import DataError
from libs import bpa_id_utils
from libs import ingest_utils
from libs import management_command
from libs.excel_wrapper import ExcelWrapper
from libs.fetch_data import Fetcher, get_password
from libs.logger_utils import get_logger
from unipath import Path

logger = get_logger(__name__)

BPA_ID = "102.100.100"
PROJECT_ID = "GBR"
PROJECT_DESCRIPTION = "Great Barrier Reef"

METADATA_PATH = "gbr/metadata/amplicons/"
DATA_DIR = Path(ingest_utils.METADATA_ROOT, METADATA_PATH)


def fix_dilution(val):
    """
    Some source xcell files ship with the dilution column type as time.
    xlrd advertises support for format strings but not implemented.
    So stuff it.
    """
    if isinstance(val, float):
        return u"1:10"  # yea, that's how we roll...
    return val


def fix_pcr(pcr):
    """
    Check pcr value
    """
    val = pcr.strip()
    if val not in ("P", "F", ""):
        logger.error("PCR value [{0}] is neither F, P or " ", setting to X".format(pcr.encode("utf8")))
        val = "X"
    return val


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


class MD5ParsedLine(object):
    def __init__(self, line):
        self._line = line
        self._ok = False
        self.__parse_line()

    def is_ok(self):
        return self._ok

    @property
    def lane(self):
        return self._lane

    @lane.setter
    def lane(self, val):
        self._lane = int(val[1:])

    @property
    def read(self):
        return self._read

    @read.setter
    def read(self, val):
        self._read = int(val[1:])

    def __parse_line(self):
        """ unpack the md5 line """
        self.md5, self.filename = self._line.split()

        filename_parts = self.filename.split(".")[0].split("_")
        if len(filename_parts) == 12:
            # 14658_GBR_UNSW_16S_R341-806_AB50N_CTCTCTAC_CTATTAAG_S54_L001_I1_001.fastq.gz
            self.bpa_id, _, self.vendor, self.amplicon, self.amplicon_range, self.flowcell, index1, index2, self.i5index, self.lane, self.read, _ = filename_parts
            self.index = index1 + "-" + index2
            self._ok = True
        else:
            self._ok = False


def parse_md5_file(md5_file):
    """
    Parse md5 file
    """

    data = []

    with open(md5_file) as f:
        for line in f.read().splitlines():
            line = line.strip()
            if line == "":
                continue

            parsed_line = MD5ParsedLine(line)
            if parsed_line.is_ok():
                data.append(parsed_line)

    return data


def get_sequencing_metadata(bpa_id, md5_line):
    """
    Populates the amplicon sequencing metadata object from the import md5 line
    """

    metadata, _ = AmpliconSequencingMetadata.objects.get_or_create(bpa_id=bpa_id, target=md5_line.amplicon)
    metadata.sequencing_facility = Facility.objects.add(md5_line.vendor)
    metadata.index = md5_line.index
    metadata.flow_cell_id = md5_line.flowcell
    metadata.save()

    return metadata


def add_md5(md5_lines):
    """
    Add md5 data
    """

    for md5_line in md5_lines:
        bpa_idx = md5_line.bpa_id
        bpa_id, report = bpa_id_utils.get_bpa_id(bpa_idx, PROJECT_ID, PROJECT_DESCRIPTION, add_prefix=True)

        if bpa_id is None:
            continue

        sample, _ = GBRSample.objects.get_or_create(bpa_id=bpa_id)
        metadata = get_sequencing_metadata(bpa_id, md5_line)

        f, _ = AmpliconSequenceFile.objects.get_or_create(sample=sample,
                                                          metadata=metadata,
                                                          read_number=md5_line.read,
                                                          lane_number=md5_line.lane,
                                                          filename=md5_line.filename,
                                                          md5=md5_line.md5)


def ingest_md5():
    """
    Ingest the md5 files
    """

    def is_md5file(path):
        if path.isfile() and path.ext == ".md5":
            return True

    logger.info("Ingesting GBR md5 file information from {0}".format(DATA_DIR))
    for md5_file in DATA_DIR.walk(filter=is_md5file):
        logger.info("Processing GBR md5 file {0}".format(md5_file))
        data = parse_md5_file(md5_file)
        add_md5(data)


def truncate():
    """ Truncate Amplicon DB tables """
    from django.db import connection

    cursor = connection.cursor()
    cursor.execute("TRUNCATE TABLE {} CASCADE".format(AmpliconSequencingMetadata._meta.db_table))
    cursor.execute("TRUNCATE TABLE {} CASCADE".format(AmpliconSequenceFile._meta.db_table))


class Command(management_command.BPACommand):
    help = 'Ingest Great Barrier Reef Amplicons'

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument('--delete',
                            action='store_true',
                            dest='delete',
                            default=False,
                            help='Delete all contextual data', )

    def handle(self, *args, **options):
        if options['delete']:
            logger.info("Truncating GBR Amplicon data")
            truncate()

        fetcher = Fetcher(DATA_DIR, self.get_base_url(options) + METADATA_PATH, auth=("bpa", get_password('gbr')))
        fetcher.clean()
        fetcher.fetch_metadata_from_folder()

        do_metadata()
        ingest_md5()

# -*- coding: utf-8 -*-

import sys

from apps.common.models import DNASource, Facility, Sequencer
from apps.gbr.models import CollectionSite, Organism, CollectionEvent, GBRSample
from apps.gbr_amplicon.models import AmpliconSequenceFile, AmpliconSequencingMetadata
from libs import ingest_utils, user_helper
from libs import bpa_id_utils
from libs.logger_utils import get_logger
from libs.excel_wrapper import ExcelWrapper, ColumnNotFoundException
from libs.fetch_data import Fetcher
from unipath import Path
from collections import namedtuple

logger = get_logger(__name__)

BPA_ID = "102.100.100"
PROJECT_ID = "GBR"
PROJECT_DESCRIPTION = "Great Barrier Reef"

METADATA_URL = 'https://downloads.bioplatforms.com/gbr/metadata/amplicons/'
DATA_DIR = Path(ingest_utils.METADATA_ROOT, 'gbr/metadata/amplicons/')

class MD5ParsedLine(object):
    def __init__(self, line):
        self._line = line

        self.bpa_id = None
        self.vendor = None
        self.lib_type = None
        self.lib_size = None
        self.flowcell = None
        self.barcode = None

        self.md5 = None
        self.filename = None

        self._lane = None
        self._read = None

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

        filename_parts = self.filename.split('.')[0].split('_')
        if len(filename_parts) == 11:
            # ['14658', 'GBR', 'UNSW', '16Sa', 'AB50N', 'TAAGGCGA', 'TCGACTAG', 'S1', 'L001', 'I1', '001']
            self.bpa_id, _, self.vendor, self.amplicon, self.flowcell, index1, index2, self.i5index, self.lane, self.read, _ = filename_parts
            self.index = index1 + '-' + index2
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
            if line == '':
                continue

            parsed_line = MD5ParsedLine(line)
            if parsed_line.is_ok():
                data.append(parsed_line)

    return data


def get_sequencing_metadata(bpa_id, md5_line):
    """
    Populates the amplicon sequencing metadata object from the import md5 line
    """

    metadata, _ = AmpliconSequencingMetadata.objects.get_or_create(bpa_id=bpa_id)
    metadata.sample_extraction_id = ""
    metadata.sequencing_facility = Facility.objects.add(md5_line.vendor)
    metadata.target = md5_line.amplicon[:-1]
    metadata.index = md5_line.index
    metadata.flow_cell_id = md5_line.flowcell
    metadata.name = md5_line.filename
    metadata.pcr_1_to_10 = None
    metadata.pcr_1_to_100 = None
    metadata.pcr_neat = None
    metadata.dilution = None
    metadata.sequencing_run_number = None
    metadata.reads = None
    metadata.analysis_software_version = None
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

        f, _ = AmpliconSequenceFile.objects.get_or_create(sample=sample, metadata=metadata)
        f.sample = sample
        f.metadata = metadata
        f.flowcell = md5_line.flowcell
        f.barcode = md5_line.barcode
        f.read_number = md5_line.read
        f.lane_number = md5_line.lane

        f.filename = md5_line.filename
        f.md5 = md5_line.md5


        f.save()

def ingest_md5():
    """
    Ingest the md5 files
    """

    def is_md5file(path):
        if path.isfile() and path.ext == '.md5':
            return True

    logger.info('Ingesting GBR md5 file information from {0}'.format(DATA_DIR))
    for md5_file in DATA_DIR.walk(filter=is_md5file):
        logger.info('Processing GBR md5 file {0}'.format(md5_file))
        data = parse_md5_file(md5_file)
        add_md5(data)

def truncate():
    """
    Truncate Amplicon DB tables
    """
    from django.db import connection

    cursor = connection.cursor()
    cursor.execute('TRUNCATE TABLE "{0}" CASCADE'.format(AmpliconSequencingMetadata._meta.db_table))
    cursor.execute('TRUNCATE TABLE "{0}" CASCADE'.format(AmpliconSequenceFile._meta.db_table))


def run():
    # fetch the new data formats
    fetcher = Fetcher(DATA_DIR, METADATA_URL, auth=('bpa', 'gbr33f'))
    fetcher.clean()
    fetcher.fetch_metadata_from_folder()
    truncate()
    ingest_md5()

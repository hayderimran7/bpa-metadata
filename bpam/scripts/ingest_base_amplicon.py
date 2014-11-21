# -*- coding: utf-8 -*-

"""
Ingests BASE Amplicon metadata from server into database.
"""

import os
from django.db.utils import DataError
from unipath import Path
import requests
from bs4 import BeautifulSoup
from libs.excel_wrapper import ExcelWrapper
from libs import ingest_utils
from libs import bpa_id_utils
from libs import logger_utils
from apps.common.models import Facility
from apps.base_amplicon.models import AmpliconSequencingMetadata, AmpliconSequenceFile, AmpliconRun
from apps.base.models import BASESample


logger = logger_utils.get_logger(__name__)

METADATA_URL = 'https://downloads.bioplatforms.com/base/tracking/amplicons/'
DATA_DIR = Path(ingest_utils.METADATA_ROOT, 'base/amplicon_metadata/')

BPA_ID = "102.100.100."
BASE_DESCRIPTION = 'BASE'


def get_bpa_id(e):
    """
    Get or make BPA ID
    """

    bpa_id = bpa_id_utils.get_bpa_id(e.bpa_id, 'BASE', 'BASE')
    if not bpa_id:
        logger.warning('Ignoring {0}, not a good BPA ID'.format(e.bpa_id))
        return None
    return bpa_id


def fix_dilution(val):
    """
    Some source xcell files ship with the dilution column type as time.
    xlrd advertises support for format strings but not implemented.
    So stuff it.
    """
    if isinstance(val, float):
        return u'1:10'  # yea, that's how we roll...
    return val


def fix_pcr(pcr):
    """
    'todo' is neither P, nor F, it will be F
    """
    val = pcr.strip()
    if val not in ['P', 'F', '']:
        logger.error('PCR value [{0}] is neither F nor P'.format(pcr))
        val = 'X'
    return val


def get_data(file_name):
    """
    The data sets is relatively small, so make a in-memory copy to simplify some operations.
    """

    field_spec = [('bpa_id', 'Soil sample unique ID', lambda s: s.replace('/', '.')),
                  ('sample_extraction_id', 'Sample extraction ID', None),
                  ('sequencing_facility', 'Sequencing facility', None),
                  ('target', 'Target', lambda s: s.upper().strip()),
                  ('index', 'Index', None),
                  ('pcr_1_to_10', '1:10 PCR, P=pass, F=fail', fix_pcr),
                  ('pcr_1_to_100', '1:100 PCR, P=pass, F=fail', fix_pcr),
                  ('pcr_neat', 'neat PCR, P=pass, F=fail', fix_pcr),
                  ('dilution', 'Dilution used', fix_dilution),
                  ('sequencing_run_number', 'Sequencing run number', None),
                  ('flow_cell_id', 'Flowcell', None),
                  ('reads', ('# of RAW reads', '# of reads'), ingest_utils.get_int),
                  ('name', 'Sample name on sample sheet', None),
                  ('analysis_software_version', 'AnalysisSoftwareVersion', None),
                  ('comments', 'Comments', None),
    ]

    wrapper = ExcelWrapper(field_spec,
                           file_name,
                           sheet_name='Sheet1',
                           header_length=4,
                           column_name_row_index=1,
                           formatting_info=True,
                           pick_first_sheet=True)

    return wrapper.get_all()


def add_samples(data):
    """
    Add sequence files
    """
    for entry in data:
        bpa_id = get_bpa_id(entry)
        if bpa_id is None:
            logger.warning('Could not add entry on row {0}'.format(entry.row))
            continue

        metadata, created = AmpliconSequencingMetadata.objects.get_or_create(bpa_id=bpa_id, target=entry.target)

        metadata.sample_extraction_id = entry.sample_extraction_id
        metadata.name = entry.name

        metadata.sequencing_facility = Facility.objects.add(entry.sequencing_facility)
        metadata.index = entry.index
        metadata.pcr_1_to_10 = entry.pcr_1_to_10
        metadata.pcr_1_to_100 = entry.pcr_1_to_100
        metadata.pcr_neat = entry.pcr_neat
        metadata.dilution = entry.dilution
        metadata.sequencing_run_number = entry.sequencing_run_number
        metadata.flow_cell_id = entry.flow_cell_id
        metadata.analysis_software_version = entry.analysis_software_version
        metadata.reads = entry.reads
        metadata.comments = entry.comments
        metadata.debug_note = ingest_utils.pretty_print_namedtuple(entry)

        try:
            metadata.save()
        except DataError, e:
            logger.error(e)
            logger.error(entry)
            exit()



def is_metadata(path):
    if path.isfile() and path.ext == '.xlsx':
        return True


def is_md5file(path):
    if path.isfile() and path.ext == '.md5' or path.ext == '.txt':
        return True


def do_metadata():
    logger.info('Ingesting BASE Amplicon metadata from {0}'.format(DATA_DIR))
    for metadata_file in DATA_DIR.walk(filter=is_metadata):
        logger.info('Processing BASE Amplicon Metadata file {0}'.format(metadata_file))
        samples = list(get_data(metadata_file))
        add_samples(samples)


def parse_md5_file(md5_file):
    """
    Parse md5 file
    cea407dac3f3e7b9afd21b1c096619b7  9486_1_16S_AGRF_ACGTGTACCCAA_A810W_S43_L001_R2_001.fastq.gz
    """
    targets = ('16S', '18S', 'ITS', 'A16S')

    def get_bpa_id_from_filename(parts):
        for target in targets:
            index = parts.index(target) if target in parts else -1
            if index != -1:
                bpa_id = '_'.join(filename_parts[:index])
                rest = filename_parts[index:]
                return bpa_id, rest

        return None, None

    data = []

    with open(md5_file) as f:
        for line in f.read().splitlines():
            line = line.strip()
            if line == '':
                continue

            file_data = {}
            md5, filename = line.split()
            file_data['md5'] = md5

            filename = filename.replace('-', '_')
            filename_parts = filename.split('_')

            extraction_id, rest = get_bpa_id_from_filename(filename_parts)
            if extraction_id == None:
                continue

            if len(rest) != 8:
                logger.error('Ignoring line {0} from {1} with missing data'.format(filename, md5_file))
                continue

            target, vendor, index, well, sequence, lane, run_num, run_id = rest

            file_data['filename'] = filename
            file_data['extraction_id'] = extraction_id
            file_data['target'] = target
            file_data['vendor'] = vendor
            file_data['index'] = index
            file_data['well'] = well
            file_data['sequence'] = sequence
            file_data['lane'] = lane
            file_data['run'] = run_num
            file_data['run_id'] = run_id
            data.append(file_data)

    return data


def add_md5(data):
    """
    Add md5 data
    """

    def get_base_sample(bpa_idx):
        try:
            idx = BPA_ID + bpa_idx.split('_')[0]
        except ValueError:
            return None

        bpa_id = bpa_id_utils.get_bpa_id(idx, 'BASE', 'BASE', 'Created by BASE Amplicon ingestor')
        sample, _ = BASESample.objects.get_or_create(bpa_id=bpa_id)
        return sample

    def get_run(file_data):
        sample = get_base_sample(extraction_id)
        if sample:
            arun, _ = AmpliconRun.objects.get_or_create(sample=sample)
            arun.sequencing_facility = Facility.objects.get(name=file_data['vendor'])
            arun.flow_cell_id = file_data['well']
            arun.save()
            return arun
        return None

    for file_data in data:
        extraction_id = file_data['extraction_id']
        target = file_data['target']
        try:
            metadata = AmpliconSequencingMetadata.objects.get(target=target,
                                                              sample_extraction_id=extraction_id)
        except AmpliconSequencingMetadata.DoesNotExist:
            logger.warning('No Amplicon Metadata for {0} {1}'.format(extraction_id, target))
            continue

        amplicon_run = get_run(file_data)
        sfile = AmpliconSequenceFile(metadata=metadata, run=amplicon_run, sample=amplicon_run.sample)
        sfile.filename = file_data['filename']
        sfile.analysed = True
        sfile.md5 = file_data['md5']
        sfile.save()


def do_md5():
    """
    Ingest the md5 files
    """
    logger.info('Ingesting BASE Amplicon md5 file information from {0}'.format(DATA_DIR))
    for md5_file in DATA_DIR.walk(filter=is_md5file):
        logger.info('Processing BASE Amplicon md5 file {0}'.format(md5_file))
        data = parse_md5_file(md5_file)
        add_md5(data)


def truncate():
    from django.db import connection

    cursor = connection.cursor()
    cursor.execute('TRUNCATE TABLE "{0}" CASCADE'.format(AmpliconSequencingMetadata._meta.db_table))
    cursor.execute('TRUNCATE TABLE "{0}" CASCADE'.format(AmpliconRun._meta.db_table))
    cursor.execute('TRUNCATE TABLE "{0}" CASCADE'.format(AmpliconSequenceFile._meta.db_table))


def get_all_metadata_from_server():
    """ downloads metadata from archive """

    def download(name):
        """ fetch file from server """
        logger.info('Fetching {0} from {1}'.format(name, METADATA_URL))
        r = requests.get(METADATA_URL + '/' + name, stream=True, auth=('base', 'b4s3'))
        with open(DATA_DIR + '/' + name, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    f.flush()

    if not os.path.exists(DATA_DIR):
        from distutils.dir_util import mkpath
        # os.makedirs(DATA_DIR)
        mkpath(DATA_DIR)

    response = requests.get(METADATA_URL, stream=True, auth=('base', 'b4s3'))
    for link in BeautifulSoup(response.content).find_all('a'):
        fname = link.get('href')
        if fname.endswith('.xlsx') or fname.endswith('.txt'):
            download(fname)


def run():
    get_all_metadata_from_server()
    truncate()
    # find all the spreadsheets in the data directory and ingest them
    do_metadata()
    do_md5()

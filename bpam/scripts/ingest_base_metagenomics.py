# -*- coding: utf-8 -*-

# The md5 files are taken as canonical sources of metadata.
# Most relevant metadata has migrated into the sequence filenames and
# are parsed from there. The xlsx spreadsheet is used as a supplementary data
# source.

# The md5 files is the source of base.MetagenomicsSequenceFile data
# The metadata spreadsheet represents one extraction per line.

import os

from unipath import Path
from libs.fetch_data import Fetcher
from libs.excel_wrapper import ExcelWrapper
from libs import bpa_id_utils
from libs import ingest_utils
from libs import logger_utils

from apps.common.models import Facility, Sequencer
from apps.base_metagenomics.models import (
    MetagenomicsSample,
    MetagenomicsSequenceFile,
    MetagenomicsRun
)


logger = logger_utils.get_logger(__name__)

METADATA_URL = 'https://downloads.bioplatforms.com/base/tracking/metagenomics/'
DATA_DIR = Path(ingest_utils.METADATA_ROOT, 'base/metagenomics_metadata/')

BPA_ID = "102.100.100."
BASE_DESCRIPTION = 'BASE'


def _get_bpa_id(entry):
    """
    Get or make BPA ID
    """

    bpa_id, report = bpa_id_utils.get_bpa_id(entry.bpa_id, 'BASE', 'BASE', note="BASE Metagenomics Sample")
    if bpa_id is None:
        logger.warning('Could not add entry in {}, row {}, BPA ID Invalid: {}'.format(entry.file_name, entry.row, report))
        return None
    return bpa_id


def get_data(file_name):
    """
    The data sets is relatively small, so make a in-memory copy to simplify some operations.
    """

    def get_library_type(library):
        """
        (('PE', 'Paired End'), ('SE', 'Single End'), ('MP', 'Mate Pair'))
        """
        new_str = library.lower()
        if new_str.find('pair') >= 0:
            return 'PE'
        if new_str.find('single') >= 0:
            return 'SE'
        if new_str.find('mate') >= 0:
            return 'MP'
        return 'UN'

    def set_id(_bpa_id):
        if isinstance(_bpa_id, basestring):
            return _bpa_id.strip().replace('/', '.')
        else:
            logger.warning('Expected a valid BPA_ID got {0}'.format(_bpa_id))
            return ''

    field_spec = [('bpa_id', 'Soil sample unique ID', set_id),
                  ('sample_id', 'Sample extraction ID', None),
                  ('sequencing_facility', 'Sequencing facility', None),
                  ('taget', 'Target', None),
                  ('index', 'Index', ingest_utils.get_clean_number),
                  ('library', 'Library', get_library_type),
                  ('library_code', 'Library code', None),  # No, I don't know why
                  ('library_construction', 'Library Construction - average insert size', ingest_utils.get_clean_number),
                  ('insert_size_range', 'Insert size range', None),
                  ('library_protocol', 'Library construction protocol', None),
                  ('sequencer', 'Sequencer', None),
                  ('run', 'Run number', ingest_utils.get_clean_number),
                  ('flow_cell_id', 'Run #:Flow Cell ID', None),
                  ('lane_number', 'Lane number', None),
                  ('casava_version', 'CASAVA version', None),
                  ]

    wrapper = ExcelWrapper(field_spec,
                           file_name,
                           sheet_name='Sheet1',
                           header_length=3,
                           column_name_row_index=1)

    return wrapper.get_all()


def get_sample(entry):
    """
    Get the Sample by bpa_id
    """
    bpa_id = _get_bpa_id(entry)
    if bpa_id is None:
        return None

    sample, created = MetagenomicsSample.objects.get_or_create(bpa_id=bpa_id)
    if created:
        sample.name = entry.sample_id
        sample.dna_extraction_protocol = entry.library_protocol
        sample.requested_sequence_coverage = entry.library_construction
        sample.debug_note = ingest_utils.pretty_print_namedtuple(entry)
        sample.save()
        logger.debug('Adding Metagenomics Sample ' + bpa_id.bpa_id)

    return sample


def get_run(entry):
    def get_sequencer(name):
        if name == '':
            name = 'Unknown'

        sequencer, _ = Sequencer.objects.get_or_create(name=name)
        return sequencer

    def get_facility(name):
        if name == '':
            name = 'Unknown'

        facility, _ = Facility.objects.get_or_create(name=name)
        return facility

    met_run, created = MetagenomicsRun.objects.get_or_create(sample=get_sample(entry))
    if created:
        logger.info('New metagenomics run created')

        met_run.flow_cell_id = entry.flow_cell_id.strip()
        met_run.run_number = entry.run
        met_run.index_number = entry.index
        met_run.sequencer = get_sequencer(entry.sequencer.strip())
        met_run.lane_number = entry.lane_number
        met_run.genome_sequencing_facility = get_facility(entry.sequencing_facility)
        met_run.save()

    return met_run


def add_samples(data):
    """
    Add samples from metadata file
    """
    for entry in data:
        sample = get_sample(entry)
        if sample is None:
            logger.warning('Could not add sample {0}'.format(sample))
            continue


def do_metadata():
    def is_metadata(path):
        if path.isfile() and path.ext == '.xlsx':
            return True

    logger.info('Ingesting BASE Metagenomics metadata from {0}'.format(DATA_DIR))
    for metadata_file in DATA_DIR.walk(filter=is_metadata):
        logger.info('Processing BASE Metagenomics Metadata file {0}'.format(metadata_file))
        samples = list(get_data(metadata_file))
        add_samples(samples)



def truncate():
    """
    Truncate Amplicon DB tables
    """
    from django.db import connection

    cursor = connection.cursor()
    cursor.execute('TRUNCATE TABLE "{0}" CASCADE'.format(MetagenomicsSample._meta.db_table))
    cursor.execute('TRUNCATE TABLE "{0}" CASCADE'.format(MetagenomicsRun._meta.db_table))
    cursor.execute('TRUNCATE TABLE "{0}" CASCADE'.format(MetagenomicsSequenceFile._meta.db_table))


class MD5handler(object):
    @static
    def add_md5(entries):
        """ Add md5 data
        Args:
            entries (list): List of md5 dicts parsed from md5 file
        """

        def get_metagenomics_sample(idx):
            bpa_id, report = bpa_id_utils.get_bpa_id(idx, 'BASE', 'BASE', 'Created by BASE Metagenomics ingestor')
            if bpa_id is None:
                return None
            sample, _ = MetagenomicsSample.objects.get_or_create(bpa_id=bpa_id)
            return sample

        def get_run(entry):
            sample = get_metagenomics_sample(entry['bpa_id'])
            if sample:
                _metagenomics_run, _ = MetagenomicsRun.objects.get_or_create(sample=sample)
                _metagenomics_run.sequencing_facility, _ = Facility.objects.get_or_create(name=entry['facility'])
                _metagenomics_run.flow_cell_id = entry['flowcell']
                _metagenomics_run.run_number = entry['run']
                _metagenomics_run.save()
                return _metagenomics_run
            return None

        for entry in entries:
            _run = get_run(entry)
            sfile = MetagenomicsSequenceFile(run=_run, sample=_run.sample)
            sfile.filename = entry['filename']
            sfile.index_number = entry['index']
            sfile.lane_number = entry['lane']
            sfile.analysed = True
            sfile.md5 = entry['md5']
            sfile.note = "BASE Metagenomics sequence file {}".format(entry['filename'])
            sfile.save()


    def parse_md5(md5_file):
        """ Parse given md5 file

        d33c76935c343df30572a2f719510eec  Sample_7910_1_PE_550bp_BASE_UNSW_H2TFJBCXX/7910_1_PE_550bp_BASE_UNSW_H2TFJBCXX_GAATTCGT-TATAGCCT_L001_R1_001.fastq.gz

        Args:
            md5_file (string): md5 text file
        Returns:
            list: List of dicts containing parsed values from md5 filenames.
        """

        data = []

        with open(md5_file) as f:
            for line in f.read().splitlines():
                line = line.strip()
                if line == '':
                    continue

                md5_entry = {}
                md5, filepath = line.split()
                md5_entry['md5'] = md5

                filename = os.path.basename(filepath)
                no_extentions_filename = filename.split('.')[0]
                parts = no_extentions_filename.split('_')

                if len(parts) == 11:
                    # UniqueID_extraction_library_insert-size_BASE_facility code_FlowID_Index_Lane_F1/R1
                    bpa_id, extraction_id, library, insert_size, _, facility, flowcell, index, lane, read, run = parts

                    md5_entry['filename'] = filename
                    md5_entry['bpa_id'] = BPA_ID + bpa_id
                    md5_entry['extraction_id'] = extraction_id
                    md5_entry['target'] = "metagenomics"
                    md5_entry['facility'] = facility
                    md5_entry['library'] = library
                    md5_entry['insert_size'] = insert_size
                    md5_entry['flowcell'] = insert_size
                    md5_entry['index'] = index
                    md5_entry['lane'] = lane
                    md5_entry['read'] = read
                    md5_entry['run'] = run
                else:
                    logger.error('Ignoring line {} from {} with missing data'.format(filename, md5_file))
                    continue

                data.append(md5_entry)

        return data

    def do_md5():
        """
        Ingest the md5 files
        """

        def is_md5file(path):
            if path.isfile() and path.ext == '.md5' or path.ext == '.txt':
                return True

        logger.info('Ingesting BASE Metagenomics md5 file information from {0}'.format(DATA_DIR))

        for md5_file in DATA_DIR.walk(filter=is_md5file):
            logger.info('Processing BASE Metagenomics md5 file {0}'.format(md5_file))
            md5_entries = parse_md5(md5_file)
            add_md5(md5_entries)


def run():
    # get all current metadata, this includes md5 and xlsx metadata files
    fetcher = Fetcher(DATA_DIR, METADATA_URL, auth=('base', 'b4s3'))
    fetcher.clean()
    fetcher.fetch_metadata_from_folder()

    truncate()

    do_md5()
    do_metadata()

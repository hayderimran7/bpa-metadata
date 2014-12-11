# -*- coding: utf-8 -*-

import zipfile
import csv
import time

from unipath import Path
from libs import logger_utils
from libs import bpa_id_utils
from libs import ingest_utils
from libs.fetch_data import Fetcher
from apps.base_otu.models import *
from apps.base.models import BASESample
from libs.excel_wrapper import ExcelWrapper
from django.conf import settings


settings.DEBUG = False

BPA_PREFIX = '102.100.100.'

logger = logger_utils.get_logger(__name__)

METADATA_URL = 'https://downloads.bioplatforms.com/base/amplicons/otu/all'
DATA_DIR = Path(ingest_utils.METADATA_ROOT, 'base/otu/')


def strip_count(val):
    return val.split('__')[-1].split('(')[0]


def ingest_taxonomy(file_name):
    kingdoms = map(lambda e: e[0], OperationalTaxonomicUnit.KINGDOMS)

    def is_valid_kingdom(kingdom):
        """ Only valid kingdom entries are allowed"""
        if kingdom in kingdoms:
            return True
        else:
            return False

    logger.info('Ingesting OTUs')
    logger.info('Now ingesting {0}'.format(file_name))

    field_spec = [('otu_id', 'OTUID', None),
                  ('kingdom', 'kingdom', strip_count),
                  ('phylum', 'phylum', strip_count),
                  ('otu_class', 'class', strip_count),
                  ('order', 'order', strip_count),
                  ('family', 'family', strip_count),
                  ('genus', 'genus', strip_count),
                  ('species', 'species', strip_count),
    ]

    wrapper = ExcelWrapper(field_spec,
                           file_name,
                           sheet_name='',
                           header_length=1,
                           column_name_row_index=0,
                           pick_first_sheet=True)

    otu_list = []
    for e in wrapper.get_all():
        if not is_valid_kingdom(e.kingdom):
            logger.error('{0} is not a valid kingdom, ignoring'.format(e.kingdom))
            continue

        otu_list.append(
            OperationalTaxonomicUnit(
                name=e.otu_id,
                kingdom=e.kingdom,
                phylum=e.phylum,
                otu_class=e.otu_class,
                order=e.order,
                family=e.family,
                genus=e.genus,
                species=e.species)
        )

    logger.info('Bulk creating {0} OTUs'.format(len(otu_list)))
    OperationalTaxonomicUnit.objects.bulk_create(otu_list)


class BASESampleCache(object):
    """
    Cache samples, try to reduce DB hits
    """

    cache = {}

    def get(self, bpa_idx):
        if bpa_idx in self.cache:
            return self.cache[bpa_idx]
        else:
            logger.info('Caching BPA ID {0}'.format(bpa_idx))
            bpa_id = bpa_id_utils.get_bpa_id(bpa_idx, 'BASE', 'BASE', note='BASE OTU Ingest')
            sample, created = BASESample.objects.get_or_create(bpa_id=bpa_id)
            self.cache[bpa_idx] = sample
            return sample


class OTUCache(object):
    """
    Caches OTU's locally to reduce DB hits
    """

    cache = {}

    def get(self, otu_name):
        if otu_name in self.cache:
            return self.cache[otu_name]
        else:
            try:
                otu = OperationalTaxonomicUnit.objects.get(name=otu_name)
                self.cache[otu_name] = otu
                return otu
            except OperationalTaxonomicUnit.DoesNotExist, e:
                logger.error('OTU {0} Does not exist'.format(otu_name))
                return None


class BPAIDLookup(object):
    """
    maybe save some cycles by doing the splitting once
    """
    cache = {}

    def get(self, key):
        if key in self.cache:
            return self.cache[key]
        else:
            val = self.get_bpa_id_from_key(key)
            self.cache[key] = val
            return val

    def get_bpa_id_from_key(self, sample_key):
        """
        Split out BPAID, some of the OTU matrixes have BPID_BLA, get rid of _BLA
        """
        split_index = sample_key.find('_')
        if split_index != -1:
            return BPA_PREFIX + sample_key[0:split_index]  # ignore the rest
        else:
            return BPA_PREFIX + sample_key


class ProgressReporter(object):
    def __init__(self, file_name):
        self.file_name = file_name
        self.total_len = self.file_len(file_name)
        self.count = 0

        self.then = time.time()

    def file_len(self, fname):
        i = -1
        with open(fname) as f:
            for i, l in enumerate(f):
                pass
        return i

    def count_row(self):
        self.count += 1
        if self.count % 100 == 0:
            now = time.time()
            logger.info('Ingested {0}/{1} rows, taking {2}s'.format(self.count, self.total_len, now - self.then))
            self.then = now


def ingest_otu_matrix(file_name):
    """
    populate the link table
    """

    csv_files = []  # all cv files found in zip
    if zipfile.is_zipfile(file_name):
        logger.info('Unzipping {0}'.format(file_name))
        with zipfile.ZipFile(file_name, 'r') as z:
            csv_files = z.namelist()
            z.extractall(DATA_DIR)
    else:
        logger.warning('{0} is not a zip file'.format(file_name))

    for csvf in csv_files:
        csv_file = Path(DATA_DIR, csvf)
        reporter = ProgressReporter(csv_file)
        logger.info('Now ingesting {0} with {1} lines'.format(csv_file, reporter.total_len))
        _ingest_csv_file(csv_file, reporter)


def _ingest_csv_file(csv_file, reporter):
    """
    Ingest the given csv file
    """
    base_sample_cache = BASESampleCache()
    otu_cache = OTUCache()
    bpa_id_lookup = BPAIDLookup()

    def _get_otu_id(row):
        """
        inconsistent UTUID, OTUId
        """
        for _ID in ('OTUID', 'OTUId'):
            if _ID in row:
                otu = otu_cache.get(row[_ID])
                row.pop(_ID)  # get rid of ID column here so I don't have to filter it out below
                return otu, row

        # should never get here
        logger.error('Could not get OTUID')
        exit(0)

    def populate_sample_cache():
        """
        populate the BASE Sample Cache
        """
        logger.info('Caching {0} BASE Samples'.format(len(reader.fieldnames) - 1))
        for sample_name in reader.fieldnames[1:]:
            base_sample_cache.get(bpa_id_lookup.get(sample_name))

    with open(csv_file, "rb") as mapfile:
        reader = csv.DictReader(mapfile)

        populate_sample_cache()

        for row in reader:
            sample_otu_list = []
            otu, row = _get_otu_id(row)
            if otu is None:
                logger.error('No valid OTU found, ignoring')

            # step through all the sample keys and create the sample to OTU links
            for sample_key, count in row.items():
                count = int(count)
                if count == 0:
                    continue

                bpa_idx = bpa_id_lookup.get(sample_key)
                if bpa_idx:
                    sample = base_sample_cache.get(bpa_idx)
                    sample_otu_list.append(SampleOTU(sample=sample, otu=otu, count=count))

            SampleOTU.objects.bulk_create(sample_otu_list)
            reporter.count_row()


def truncate():
    from django.db import connection

    cursor = connection.cursor()
    cursor.execute('TRUNCATE TABLE "{0}" CASCADE'.format(OperationalTaxonomicUnit._meta.db_table))


def do_taxonomies():
    def is_taxonomy(path):
        if path.isfile() and path.ext == '.xlsx':
            return True

    logger.info('Ingesting BASE OTUs from {0}'.format(DATA_DIR))
    for taxonomy_file in DATA_DIR.walk(filter=is_taxonomy):
        logger.info('Processing BASE OTU Metadata file {0}'.format(taxonomy_file))
        ingest_taxonomy(taxonomy_file)


def do_otu_matrix():
    def is_otu_matrix(path):
        if path.isfile() and path.ext == '.zip':
            return True

    logger.info('Ingesting BASE OTU Matrixs from {0}'.format(DATA_DIR))
    for matrix_file in DATA_DIR.walk(filter=is_otu_matrix):
        logger.info('Processing BASE OTU Matrix file {0}'.format(matrix_file))
        ingest_otu_matrix(matrix_file)


def run():
    fetcher = Fetcher(DATA_DIR, METADATA_URL, auth=('base', 'b4s3'))
    fetcher.fetch_metadata_from_folder()
    truncate()

    do_taxonomies()
    do_otu_matrix()







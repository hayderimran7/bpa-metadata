# -*- coding: utf-8 -*-

import zipfile
from unipath import Path
import requests
import csv
import time
import os

from libs import logger_utils
from libs import bpa_id_utils
from libs import ingest_utils

from apps.base_otu.models import *
from apps.base.models import BASESample
from libs.excel_wrapper import ExcelWrapper

from django.conf import settings

settings.DEBUG = False

BPA_PREFIX = '102.100.100.'

logger = logger_utils.get_logger(__name__)

# DATA_DIR = Path(Path(__file__).ancestor(3), "data/base/")
# TAXONOMY_FILE = Path(DATA_DIR, '16s_otu.xlst')
# MAP_TAXONOMY_TO_SAMPLE_FILE = Path(DATA_DIR, '16s_otu_sample_map.zip')

DATA_DIR = os.path.join(ingest_utils.METADATA_ROOT, "data/base/")
TAXONOMY_FILE = os.path.join(ingest_utils.METADATA_ROOT, 'base/16s_otu.xlst')
MAP_TAXONOMY_TO_SAMPLE_FILE = os.path.join(ingest_utils.METADATA_ROOT, 'base/16s_otu_sample_map')

# for testing
# DEV_MAP_FILE = Path(DATA_DIR, 'small_otu.xlst')
DEV_MAP_FILE = os.path.join(ingest_utils.METADATA_ROOT, 'base/small_otu.xlst')

TAXONOMY_URL = 'https://downloads.bioplatforms.com/base/amplicons/otu/16s/BASE_16S_OTU.xlst'
MAP_16S_OTU_URL = 'https://downloads.bioplatforms.com/base/amplicons/otu/16s/BASE_16S_97OTUS_OTUXSAMPLE.zip'

# TODO use ingest utils
def download_url(url, local_name=None):
    """
    Fetches data file from webserver
    """
    logger.info('Downloading {0}'.format(url))
    if local_name is None:
        local_name = url.split('/')[-1]

    r = requests.get(url, stream=True, auth=('base', 'b4s3'))
    with open(local_name, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()

    return local_name


def ensure_data_file_is_available(url, file_name):
    """
    get the data file of the webserver if not locally available
    """
    _file = Path(file_name)
    logger.info('Is {0} in {1} ?'.format(file_name, DATA_DIR))
    #if not Path.isfile(_file):
    download_url(url, _file) # always download
    logger.info('Yes, it is now')


def strip_count(val):
    return val.split('__')[-1].split('(')[0]


def ingest_otu(file_name):
    logger.info('Ingesting OTUs')
    logger.info('Now ingesting {0}'.format(file_name))

    field_spec = [('otu_id', 'OTUID', None),
                  ('phylum', 'phylum', strip_count),
                  ('otu_class', 'class', strip_count),
                  ('order', 'ordetr', strip_count),
                  ('family', 'family', strip_count),
                  ('genus', 'genus', strip_count), ]

    wrapper = ExcelWrapper(field_spec,
                           file_name,
                           sheet_name='BASE_16S_97OTUS_NOSINGLES_label',
                           header_length=1,
                           column_name_row_index=0)

    otu_list = []
    for e in wrapper.get_all():
        otu_list.append(
            OperationalTaxonomicUnit(
                name=e.otu_id,
                kingdom='Bacteria',
                phylum=e.phylum,
                otu_class=e.otu_class,
                order=e.order,
                family=e.family,
                genus=e.genus)
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
            otu = OperationalTaxonomicUnit.objects.get(name=otu_name)
            self.cache[otu_name] = otu
            return otu


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
        Split out BPAID
        """
        split_index = sample_key.find('_')
        if split_index != -1:
            return BPA_PREFIX + sample_key[0:split_index]  # ignore the rest
        else:
            return None


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


def ingest_sample_to_otu(file_name):
    """
    populate the link table
    """
    base_sample_cache = BASESampleCache()
    otu_cache = OTUCache()
    bpa_id_lookup = BPAIDLookup()

    csv_files = []  # all cv files found in zip
    if zipfile.is_zipfile(file_name):
        logger.info('Unzipping {0}'.format(file_name))
        with zipfile.ZipFile(file_name, 'r') as z:
            csv_files = z.namelist()
            z.extractall(DATA_DIR)

    for csvf in csv_files:
        csv_file = Path(DATA_DIR, csvf)
        reporter = ProgressReporter(csv_file)
        logger.info('Now ingesting {0} with {1} lines'.format(csv_file, reporter.total_len))

        with open(csv_file, "rb") as mapfile:
            reader = csv.DictReader(mapfile)

            # populate the BASE Sample Cache
            logger.info('Caching {0} BASE Samples'.format(len(reader.fieldnames) - 1))
            for sample_name in reader.fieldnames[1:]:
                base_sample_cache.get(bpa_id_lookup.get(sample_name))

            for row in reader:
                sample_otu_list = []
                otu = otu_cache.get(row['OTUId'])
                row.pop('OTUId')  # get rid of ID column here so I don't have to filter it out below
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


def ingest():
    # OTU
    ensure_data_file_is_available(TAXONOMY_URL, TAXONOMY_FILE)
    ingest_otu(TAXONOMY_FILE)

    # OTU->Sample
    ensure_data_file_is_available(MAP_16S_OTU_URL, MAP_TAXONOMY_TO_SAMPLE_FILE)
    ingest_sample_to_otu(MAP_TAXONOMY_TO_SAMPLE_FILE)


def run():
    truncate()
    ingest()







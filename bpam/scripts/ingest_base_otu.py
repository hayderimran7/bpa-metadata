# -*- coding: utf-8 -*-

import zipfile
from unipath import Path
import requests
import xlrd
import csv

from libs import logger_utils
from libs import ingest_utils
from libs import bpa_id_utils

from apps.base_otu.models import *
from apps.base.models import BASESample
from libs.excel_wrapper import ExcelWrapper

BPA_PREFIX = '102.100.100.'

logger = logger_utils.get_logger(__name__)

DATA_DIR = Path(Path(__file__).ancestor(3), "data/base/")
TAXONOMY_FILE = Path(DATA_DIR, '16s_otu.xlst')
MAP_TAXONOMY_TO_SAMPLE_FILE = Path(DATA_DIR, '16s_otu_sample_map.zip')

# for testing
DEV_MAP_FILE = Path(DATA_DIR, 'small_otu.xlst')

TAXONOMY_URL = 'https://downloads.bioplatforms.com/base/metadata/BASE_16S_97OTUS_MAY5.xlsx'
MAP_16S_OTU_URL = 'https://downloads.bioplatforms.com/base/metadata/BASE_16S_97OTUS_OTUXSAMPLE_MAY5.zip'


def download_url(url, local_name=None):
    """
    Fetches data file from webserver
    """
    logger.info('Downloading {0}'.format(url))
    if local_name is None:
        local_name = url.split('/')[-1]

    r = requests.get(url, stream=True)
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
    logger.info('Is {0} in {1} ?'.format(file_name, DATA_DIR))
    if not Path.isfile(file_name):
        download_url(url, file_name)
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

    for e in wrapper.get_all():
        otu, created = OperationalTaxonomicUnit.objects.get_or_create(
            name=e.otu_id,
            kingdom='Bacteria',
            phylum=e.phylum,
            otu_class=e.otu_class,
            order=e.order,
            family=e.family,
            genus=e.genus)
        otu.save()


class BASESampleCache(object):
    """
    Cache samples, try to reduce DB hits
    """

    cache = {}

    def get(self, bpa_idx):
        if self.cache.has_key(bpa_idx):
            return self.cache[bpa_idx]

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
        if self.cache.has_key(otu_name):
            return self.cache[otu_name]
        else:
            otu = OperationalTaxonomicUnit.objects.get(name=otu_name)
            self.cache[otu_name] = otu
            return otu


def get_bpa_id_from_key(sample_key):
    if 

def ingest_sample_to_otu(file_name):
    """
    populate the link table
    """
    base_sample_cache = BASESampleCache()
    otu_cache = OTUCache()

    csv_files = []  # all cv files found in zip
    if zipfile.is_zipfile(file_name):
        logger.info('Unzipping {0}'.format(file_name))
        with zipfile.ZipFile(file_name, 'r') as z:
            csv_files = z.namelist()
            z.extractall(DATA_DIR)

    for csvf in csv_files:
        csv_file = Path(DATA_DIR, csvf)
        logger.info('Now ingesting {0}'.format(csv_file))

        with open(csv_file, "rb") as mapfile:
            reader = csv.DictReader(mapfile)

            # populate the BASE Sample Cache
            for sample_name in reader.fieldnames[1:]:
                base_sample_cache.get(BPA_PREFIX + sample_name.split('_')[0])

            for row in reader:
                otu = otu_cache.get(row['OTUId'])
                # step through all the sample keys and update the links
                for sample_key, count in row.items():
                    bpa_idx = get_bpa_id_from_key(sample_key)
                    sample =



# deprecated
def xcell_otu_sample_map_ingest(file_name):
    workbook = xlrd.open_workbook(file_name)
    sheet = workbook.sheet_by_index(0)  # the first sheet looks ok...

    otu_total = sheet.nrows - 1
    sample_total = sheet.ncols - 1
    curr_otu = 0  # skip header

    base_sample_cache = BASESampleCache()
    otu_cache = OTUCache()

    while curr_otu < otu_total:
        curr_otu += 1
        curr_sample = 0  # first col is otu id
        while curr_sample < sample_total:
            curr_sample += 1
            count = sheet.cell_value(curr_otu, curr_sample)
            if count > 0:
                otu_name = 'OTU_' + str(int(sheet.cell_value(curr_otu, 0)))
                bpa_id_name = BPA_PREFIX + str(ingest_utils.get_int(sheet.cell_value(0, curr_sample)))
                otu = otu_cache.get(otu_name)

                sample = base_sample_cache.get(bpa_id_name)
                if sample:
                    sample_otu, created = SampleOTU.objects.get_or_create(otu=otu, count=count, sample=sample)


def truncate():
    from django.db import connection

    cursor = connection.cursor()
    cursor.execute('TRUNCATE TABLE "{0}" CASCADE'.format(OperationalTaxonomicUnit._meta.db_table))


def ingest():
    # OTU
    # ensure_data_file_is_available(TAXONOMY_URL, TAXONOMY_FILE)
    # ingest_otu(TAXONOMY_FILE)

    # OTU->Sample
    ensure_data_file_is_available(MAP_16S_OTU_URL, MAP_TAXONOMY_TO_SAMPLE_FILE)
    ingest_sample_to_otu(MAP_TAXONOMY_TO_SAMPLE_FILE)


def run():
    ingest()
    # truncate()






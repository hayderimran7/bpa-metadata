# -*- coding: utf-8 -*-

from unipath import Path
import requests

from libs import logger_utils
from libs import ingest_utils
from apps.base_otu.models import *
from apps.common.models import BPAUniqueID

import xlrd

logger = logger_utils.get_logger(__name__)

DATA_DIR = Path(Path(__file__).ancestor(3), "data/base/")
DEFAULT_OTU_FILE = Path(DATA_DIR, 'fake_otu.txt')
DEFAULT_MAP_FILE = Path(DATA_DIR, 'base_otu.xlst')
DEV_MAP_FILE = Path(DATA_DIR, 'small_otu.xlst')

# we were asked to use this for the time being
TEST_TAXONOMY_URL = 'https://downloads.bioplatforms.com/base/metadata/BASE_OTUs.silva.wang.taxonomy'
BASE_OTU_MAP='https://downloads.bioplatforms.com/base/metadata/BASE_biological_data.xlst'

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


def ingest_otu(file_name):
    logger.info('Ingesting OTUs')
    with open(file_name, 'r') as f:
        for line in f:
            #  split on space then ;
            otu_name, rest = line.split()
            kingdom, phylum, otu_class, order, family, genus, species = map(lambda s: s.split('(')[0],
                                                                            rest.split(';')[:7])

            otu, created = OperationalTaxonomicUnit.objects.get_or_create(
                name=otu_name,
                kingdom=kingdom,
                phylum='p_' + phylum,
                otu_class='c_' + otu_class,
                order='o_' + order,
                family='f_' + family,
                genus='g_' + genus,
                species='s_' + species)


def ingest_sample_to_otu(file_name):
    """
    populate the link table
    """
    logger.info('Now ingesting {0}'.format(file_name))
    workbook = xlrd.open_workbook(file_name)
    sheet = workbook.sheet_by_index(0) # the first sheet looks ok...

    otu_total = sheet.nrows - 1
    sample_total = sheet.ncols - 1
    curr_otu = 0 # skip header
    
    while curr_otu < otu_total:
        curr_otu += 1
        curr_sample = 0 # first col is otu id
        while curr_sample < sample_total:
            curr_sample += 1
            count = sheet.cell_value(curr_otu, curr_sample)
            if count > 0:
                otuname = 'OTU_' + str(int(sheet.cell_value(curr_otu, 0)))
                bpa_id_name= '102.100.100.' + str(ingest_utils.get_int(sheet.cell_value(0, curr_sample)))
                otu = OperationalTaxonomicUnit.objects.get(name=otuname)
                bpa_id = BPAUniqueID.objects.get(bpa_id=bpa_id_name)
                try:
                    sample = BaseSample.objects.get(bpa_id=bpa_id)
                except BaseSample.DoesNotExist:
                    logger.warning('BASE Sample with bpa_id {} not currently in DB'.format(bpa_id_name))
                    continue

                sample_otu, created = SampleOTU.objects.get_or_create(otu=otu, count=count, sample=sample)


def run():
    # OTU
    ensure_data_file_is_available(TEST_TAXONOMY_URL, DEFAULT_OTU_FILE)
    ingest_otu(DEFAULT_OTU_FILE)
    # OTU->Sample
    ensure_data_file_is_available(BASE_OTU_MAP, DEFAULT_MAP_FILE)
    ingest_sample_to_otu(DEFAULT_MAP_FILE)





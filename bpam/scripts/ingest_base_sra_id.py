
# -*- coding: utf-8 -*-

import csv
import sys

from libs import ingest_utils, user_helper, logger_utils
from libs.fetch_data import Fetcher, get_password
from apps.common.models import BPAUniqueID
from unipath import Path

logger = logger_utils.get_logger(__name__)

METADATA_URL = 'https://downloads.bioplatforms.com/base/metadata/'  # the folder
SAMPLE_ID_FILE = 'Biosample_accessions.csv'  # the file
DATA_DIR = Path(ingest_utils.METADATA_ROOT, 'biosample_id/')


def get_data(_file):
    with open(_file, 'rb') as ids:
        fieldnames = ['Accession', 'Sample Name']
        reader = csv.DictReader(ids, fieldnames=fieldnames)
        return ingest_utils.strip_all(reader)


def ingest_ids(ids_file):
    """ Biosample_accessions ID's assigned by SRA """

    for _map in get_data(ids_file):
        bpa_id = _map.get('Sample Name')
        bpa_id = bpa_id.replace('/', '.')
        sra_id = _map.get('Accession')
        try:
            bpa = BPAUniqueID.objects.get(bpa_id=bpa_id)
            bpa.sra_id = sra_id
            bpa.save()
        except BPAUniqueID.DoesNotExist as e:
            logger.info(bpa_id)
            logger.info(sra_id)
            logger.error(e)


def run():
    password = get_password('base')
    fetcher = Fetcher(DATA_DIR, METADATA_URL, auth=('base', password))
    fetcher.fetch(SAMPLE_ID_FILE)
    ingest_ids(DATA_DIR + SAMPLE_ID_FILE)

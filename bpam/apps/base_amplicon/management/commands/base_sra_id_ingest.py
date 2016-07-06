# -*- coding: utf-8 -*-

import csv

from libs import ingest_utils
from libs import logger_utils
from libs.fetch_data import Fetcher, get_password
from libs import management_command
from apps.common.models import BPAUniqueID
from unipath import Path

logger = logger_utils.get_logger(__name__)

METADATA_PATH = 'base/metadata/'
SAMPLE_ID_FILE = 'Biosample_accessions.csv'
DATA_DIR = Path(ingest_utils.METADATA_ROOT, METADATA_PATH)


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


class Command(management_command.BPACommand):
    help = 'Ingest BASE SRA IDs'

    def handle(self, *args, **options):

        fetcher = Fetcher(DATA_DIR, self.get_base_url(options) + METADATA_PATH, auth=("base", get_password('base')))
        fetcher.clean()
        fetcher.fetch(SAMPLE_ID_FILE)
        ingest_ids(DATA_DIR + SAMPLE_ID_FILE)

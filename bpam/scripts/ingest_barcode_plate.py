# -*- coding: utf-8 -*-

import csv
from unipath import Path

from libs import ingest_utils, logger_utils
from libs.fetch_data import Fetcher

logger = logger_utils.get_logger(__name__)

METADATA_URL = "https://downloads.bioplatforms.com/bpa/barcode/plate/"
DATA_DIR = Path(ingest_utils.METADATA_ROOT, "barcode_plate/")


def UnicodeDictReader(str_data, encoding="utf8", **kwargs):
    csv_reader = csv.DictReader(str_data, **kwargs)
    keymap = dict((k, k.decode(encoding)) for k in csv_reader.fieldnames)
    for row in csv_reader:
        yield dict((keymap[k], v.decode(encoding)) for k, v in row.iteritems())


def add_plates(plates):
    for plate in plates:
        print(plate)

def get_plate_data(plate_file):
    with open(plate_file, "r") as plates_f:
        reader = UnicodeDictReader(plates_f, encoding="cp1252")
        return ingest_utils.strip_all(reader)

def ingest_plates():
    """
    Herbarium plates
    """

    def is_csv(path):
        if path.isfile() and path.ext == ".csv":
            return True

    logger.info("Ingesting Plate data from {0}".format(DATA_DIR))
    for plate_file in DATA_DIR.walk(filter=is_csv):
        logger.info("Processing barcode plate {0}".format(plate_file))
        plates = list(get_plate_data(plate_file))
        add_plates(plates)


def run():
    fetcher = Fetcher(DATA_DIR, METADATA_URL)
    fetcher.clean()
    fetcher.fetch_metadata_from_folder()
    ingest_plates()

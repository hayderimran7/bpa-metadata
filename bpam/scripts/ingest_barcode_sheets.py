#/data/metadata/bar -*- coding: utf-8 -*-

from django.db import IntegrityError
import csv
from unipath import Path

from libs import ingest_utils, logger_utils
from libs.fetch_data import Fetcher

from apps.barcode.models import Sheet

logger = logger_utils.get_logger(__name__)

METADATA_URL = "https://downloads.bioplatforms.com/bpa/barcode/raw/pilbara_flora/sheet/"
DATA_DIR = Path(ingest_utils.METADATA_ROOT, "barcode_sheets/")


def add_sheets(sheets):

    def is_alien(val):
        val = val.strip().upper()
        if val == "Y":
            return True
        return False

    for sheet in sheets:
        try:
            sheet, created = Sheet.objects.get_or_create(
                    sheet_number=sheet["Sheet Number"],
                    name_id=sheet["NameID"],
                    plant_description=sheet["Plant Description"],
                    site_description=sheet["Site Description"],
                    vegetation=sheet["Vegetation"],

                    # position
                    latitude=sheet["Latitude"],
                    longitude=sheet["Longitude"],
                    datum=sheet["Datum"],
                    geocode_accuracy=ingest_utils.get_clean_float(sheet["Geocode Accuracy"]),
                    geocode_method=sheet["Geocode Method"],
                    barker_coordinate_accuracy_flag=ingest_utils.get_int(sheet["Barker Coordinate Accuracy Flag"]),

                    # flora
                    family=sheet["Family"],
                    genus=sheet["Genus"],
                    species=sheet["Species"],
                    rank=sheet["Rank"],
                    infraspecies_qualifier=sheet["Infraspecies Qualifier"],
                    infraspecies=sheet["Infraspecies"],
                    alien=is_alien(sheet["Alien"]),

                    # determination
                    author=sheet["Author"],
                    manuscript=sheet["Manuscript"],
                    conservation_code=sheet["Conservation Code"],
                    determiner_name=sheet["Determiner Name"],
                    date_of_determination=ingest_utils.get_date(sheet["Date of Determination"]),
                    determiner_role=sheet["Determiner Role"],
                    name_comment=sheet["Name Comment"],
                    frequency=sheet["Frequency"],
                    locality=sheet["Locality"],
                    state=sheet["State"],

                    # collector
                    collector=sheet["Collector"],
                    collector_number=sheet["Collector's Number"],
                    collection_date=ingest_utils.get_date(sheet["Collection Date"]),
                    voucher=sheet["Voucher"],
                    voucher_id=ingest_utils.get_int(sheet["VoucherID"]),
                    voucher_site=sheet["Voucher Site"],
                    type_status=sheet["Type Status"],

                    note=sheet["Other Notes"]
                    )
        except IntegrityError as e:
            logger.error("Sheet {} is duplicated".format(sheet["Sheet Number"]))
            logger.error("{}".format(e.message))
            logger.error("{}".format(sheet))

def UnicodeDictReader(str_data, encoding="utf8", **kwargs):
    csv_reader = csv.DictReader(str_data, **kwargs)
    keymap = dict((k, k.decode(encoding)) for k in csv_reader.fieldnames)
    for row in csv_reader:
        yield dict((keymap[k], v.decode(encoding)) for k, v in row.iteritems())

def get_sheet_data(sheet_file):
    with open(sheet_file, "r") as sheets_f:
        reader = UnicodeDictReader(sheets_f, encoding="cp1252")
        return ingest_utils.strip_all(reader)

def ingest_sheets():
    """ Herbarium sheets """

    def is_csv(path):
        if path.isfile() and path.ext == ".csv":
            return True

    logger.info("Ingesting sheet data from {0}".format(DATA_DIR))
    for sheet_file in DATA_DIR.walk(filter=is_csv):
        logger.info("Processing barcode sheet {0}".format(sheet_file))
        sheets = list(get_sheet_data(sheet_file))
        add_sheets(sheets)

def truncate():
    """ Truncate Amplicon DB tables """

    from django.db import connection

    cursor = connection.cursor()
    cursor.execute("TRUNCATE TABLE {0} CASCADE".format(Sheet._meta.db_table))

def run():
    fetcher = Fetcher(DATA_DIR, METADATA_URL)
    fetcher.clean()
    fetcher.fetch_metadata_from_folder()
    truncate()
    ingest_sheets()

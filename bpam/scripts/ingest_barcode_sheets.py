# -*- coding: utf-8 -*-

from django.db import IntegrityError
import csv
from unipath import Path

from libs import ingest_utils, logger_utils, bpa_id_utils
from libs.fetch_data import Fetcher

from apps.barcode.models import Sheet

logger = logger_utils.get_logger(__name__)


def UnicodeDictReader(str_data, encoding="utf8", **kwargs):
    csv_reader = csv.DictReader(str_data, **kwargs)
    keymap = dict((k, k.decode(encoding)) for k in csv_reader.fieldnames)
    for row in csv_reader:
        yield dict((keymap[k], v.decode(encoding)) for k, v in row.iteritems())


def get_csv_data(_file):
    with open(_file, "r") as _f:
        reader = UnicodeDictReader(_f, encoding="cp1252")
        return ingest_utils.strip_all(reader)


def truncate():
    """ Truncate Amplicon DB tables """

    from django.db import connection

    cursor = connection.cursor()
    cursor.execute("TRUNCATE TABLE {0} CASCADE".format(Sheet._meta.db_table))


class Mapper(object):
    """ Maps sheets to BPA IDs """

    def setmap(self, smap):
        for m in smap:
            bpa_idx = m["BPA unique  identifier"].replace("/", ".")
            sheet_number = ingest_utils.get_clean_number(m["Sheet number"])
            bpa_id, report = bpa_id_utils.get_bpa_id(bpa_idx, "BARCODE", "Barcode Pilbara Flora", "")

            try:
                sheet = Sheet.objects.get(sheet_number=sheet_number)
                sheet.bpa_id = bpa_id
                sheet.save()
            except Sheet.DoesNotExist:
                logger.error("No sheet number {} in database".format(sheet_number))

    def mapsheets(self):
        """ Map the herbarium sheets to BPA ID's """

        DATA_URL = "https://downloads.bioplatforms.com/bpa/barcode/raw/pilbara_flora/map/"
        DATA_DIR = Path(ingest_utils.METADATA_ROOT, "barcode_map/")

        fetcher = Fetcher(DATA_DIR, DATA_URL)
        fetcher.clean()
        fetcher.fetch_metadata_from_folder()

        def is_csv(path):
            if path.isfile() and path.ext == ".csv":
                return True

        logger.info("Ingesting herbarium sheet to BPA map data from {0}".format(DATA_DIR))
        for map_file in DATA_DIR.walk(filter=is_csv):
            logger.info("Processing map {0}".format(map_file))
            smap = list(get_csv_data(map_file))
            self.setmap(smap)


class SheetAdder(object):
    """ Add the sheet data """

    def add_sheets(self, sheets):

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

    def add(self):
        """ Adds all herbarium sheets """

        METADATA_URL = "https://downloads.bioplatforms.com/bpa/barcode/raw/pilbara_flora/sheets/"
        DATA_DIR = Path(ingest_utils.METADATA_ROOT, "barcode_sheets/")

        fetcher = Fetcher(DATA_DIR, METADATA_URL)
        fetcher.clean()
        fetcher.fetch_metadata_from_folder()

        def is_csv(path):
            if path.isfile() and path.ext == ".csv":
                return True

        logger.info("Ingesting sheet data from {0}".format(DATA_DIR))
        for sheet_file in DATA_DIR.walk(filter=is_csv):
            logger.info("Processing barcode sheet {0}".format(sheet_file))
            sheets = list(get_csv_data(sheet_file))
            self.add_sheets(sheets)


def run():
    truncate()

    SheetAdder().add()
    Mapper().mapsheets()

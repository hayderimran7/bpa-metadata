#!/usr/bin/env python
# coding: utf-8

"""
This tool takes the current base format document and re-flows it to a more normalised version.

Usage:
  reflow.py [options] INPUT_FILE [OUTPUT_FILE_PREFIX]

Options:
  -v, --verbose       Verbose mode.
  -s, --get-samples   Get samples.
  -c, --get-analysis  Get chemical analysis.
  -s, --get-sites     Get sites.
  -a, --get-all       Get everything.

"""

from unipath import Path
import logging
import sys
import csv
import pprint
import time
from collections import namedtuple
from docopt import docopt
from dateutil.parser import parse as date_parse

__author__ = 'ccg'
__version__ = '0.1'
DEFAULT_OUTPUT_FILE_PREFIX = "base"

logging.basicConfig()
logger = logging.getLogger("baseparser")
logger.setLevel(level=logging.INFO)


def parse_date(str):
    """
    Try to get a valid date from the passed in str
    """
    date = None
    err = None
    try:
        date = date_parse(str)
    except ValueError, e:
        err = e
    return date, err


# maps spreadsheet column name with attribute names, validator and converter functions, if any
ColumnSpec = namedtuple('ColumnSpec', 'name validator converter')
COLUMNS = {'Sample#': ColumnSpec('bpa_id', None, None),
           'Depth (cm)': ColumnSpec('depth', None, None),
           'Site / NP': ColumnSpec('site_name', None, None),
           'Date Sampled': ColumnSpec('sample_date', None, parse_date),
           'Soil moisture (%)': ColumnSpec('moisture', None, None),
           'color': ColumnSpec('color', None, None),
           'Gravel (%)': ColumnSpec('gravel', None, None),
           'Texture ()': ColumnSpec('texture', None, None),
           'Ammonium Nitrogen (mg/Kg)': ColumnSpec('ammonium_nitrogen', None, None),
           'Nitrate Nitrogen (mg/Kg)': ColumnSpec('nitrate_nitrogen', None, None),
           'Phosphorus Colwell (mg/Kg)': ColumnSpec('phosphorus_colwell', None, None),
           'Potassium Colwell (mg/Kg)': ColumnSpec('potassium_colwell', None, None),
           'Sulphur (mg/Kg)': ColumnSpec('sulphur', None, None),
           'Organic Carbon (%)': ColumnSpec('organic_carbon', None, None),
           'Conductivity (dS/m)': ColumnSpec('conductivity', None, None),
           'pH Level (CaCl2) (pH)': ColumnSpec('ph_cacl2', None, None),
           'pH Level (H2O) (pH)': ColumnSpec('ph_h20', None, None),
           'DTPA Copper (mg/Kg)': ColumnSpec('dtpa_copper', None, None),
           'DTPA Iron (mg/Kg)': ColumnSpec('dtpa_iron', None, None),
           'DTPA Manganese (mg/Kg)': ColumnSpec('dtpa_manganese', None, None),
           'DTPA Zinc (mg/Kg)': ColumnSpec('dtpa_zinc', None, None),
           'Exc. Aluminium (meq/100g)': ColumnSpec('exc_aluminium', None, None),
           'Exc. Calcium (meq/100g)': ColumnSpec('exc_calcium', None, None),
           'Exc. Magnesium (meq/100g)': ColumnSpec('exc_magnesium', None, None),
           'Exc. Potassium (meq/100g)': ColumnSpec('exc_potasium', None, None),
           'Exc. Sodium (meq/100g)': ColumnSpec('exc_sodium', None, None),
           'Boron Hot CaCl2 (mg/Kg)': ColumnSpec('exc_boron', None, None),
           'Clay (%)': ColumnSpec('clay', None, None),
           'Course Sand (%)': ColumnSpec('course_sand', None, None),
           'Fine Sand (%)': ColumnSpec('fine_sand', None, None),
           'Sand (%)': ColumnSpec('sand', None, None),
           'Silt  (%)': ColumnSpec('silt', None, None),
           'GPS lat. (GDA94?)': ColumnSpec('latitute', None, None),
           'GPS lon. (GDA94?)': ColumnSpec('longitude', None, None),
           'current land-use': ColumnSpec('land_use', None, None),
           'Vegetation Total cover (%)': ColumnSpec('vegetation_total_cover', None, None),
           'Vegetation Dom. Trees (%)': ColumnSpec('vegetation_dominant_trees', None, None),
           'Vegetation Dom. Shrubs (%)': ColumnSpec('vegetation_dominant_shrubs', None, None),
           'Vegetation Dom. Grasses (%)': ColumnSpec('vegetation_dominant_grasses', None, None),
           'Elevation (m)': ColumnSpec('elevation', None, None),
           'Slope (%)': ColumnSpec('slope', None, None),
           'Slope Aspect': ColumnSpec('slope_aspect', None, None),
           'Slope Position': ColumnSpec('slope_position', None, None),
           'Other comments': ColumnSpec('comments', None, None)}


# map the column map by attributes, so we can do a quick lookup from attribute to the validators
ATTRIBUTES = {}
AttributeSpec = namedtuple('AttributeSpec', 'column_name validator converter')
for c_name, col_spec in COLUMNS.items():
    ATTRIBUTES[col_spec.name] = AttributeSpec(c_name, col_spec.validator, col_spec.converter)


class Helper(object):
    field_spec = []

    @classmethod
    def get_date_str(cls, date):
        if date is not None:
            return date.strftime("%d/%m/%Y")
        else:
            return ''

    @classmethod
    def get_header(cls):
        header = []
        for atr in cls.field_spec:
            header.append(ATTRIBUTES[atr].column_name)
        return header

    @classmethod
    def unpack(cls, tup_name, reader):
        """
        Unpack the csv file to the named tuple type
        """
        named_tup = namedtuple(tup_name, ['row'] + cls.field_spec)

        for idx, row in enumerate(reader):
            tpl = [idx]
            for field in cls.field_spec:
                spec = ATTRIBUTES[field]
                val = row[spec.column_name].decode('utf-8').strip()

                converter_func = spec.converter
                validator_func = spec.validator

                if converter_func is not None:
                    val, err = converter_func(val)
                    if err is not None:
                        logger.error(err)

                if validator_func is not None:
                    val, err = validator_func(val)
                    if err is not None:
                        logger.error(err)

                tpl.append(val)
            yield named_tup(*tpl)


class SampleHelper(Helper):

    field_spec = ['bpa_id', 'depth', 'sample_date']

    @classmethod
    def write_samples(cls, args, samples):
        """
        Write list of sample objects to csv file
        """
        file_name = args['OUTPUT_FILE_PREFIX'] + '_samples.csv'
        with open(file_name, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(cls.get_header())
            for sample in samples:
                formatted = [sample.bpa_id, sample.depth, cls.get_date_str(sample.sample_date)]
                writer.writerow(formatted)  # don't want row in file

    @classmethod
    def get_samples(cls, args):
        """
        Parse samples
        """

        in_file = Path(args['INPUT_FILE'])
        with open(in_file) as fd:
            reader = csv.DictReader(fd)
            cls.write_samples(args, cls.unpack('Sample', reader))


class SiteHelper(Helper):
    @classmethod
    def get_sites(cls, args):
        in_file = Path(args['INPUT_FILE'])
        with open(in_file) as fd:
            reader = csv.DictReader(fd)



def main(args):
    if args['--get-sites'] is not None:
        site_helper = SiteHelper()
        site_helper.get_sites(args)

    if args['--get-samples'] is not None:
        sample_helper = SampleHelper()
        sample_helper.get_samples(args)


def args_check(args):
    """
    Aborts if passed parameters are not OK
    """
    in_file = Path(args['INPUT_FILE'])
    if not in_file.exists():
        sys.exit("The input file {0} does not exist. Quitting".format(in_file))


if __name__ == '__main__':
    args = docopt(__doc__, version=__version__)

    if args['OUTPUT_FILE_PREFIX'] is None:
        args['OUTPUT_FILE_PREFIX'] = DEFAULT_OUTPUT_FILE_PREFIX


    if args['--verbose']:
        logger.setLevel(level=logging.DEBUG)
        logger.info(pprint.pprint(args))

    args_check(args)
    main(args)

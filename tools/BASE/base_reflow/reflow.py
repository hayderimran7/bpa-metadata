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
import codecs
import logging
import sys
import csv
import pprint
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
           'GPS lat. (GDA94?)': ColumnSpec('latitude', None, None),
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

    def __init__(self, args):
        self.args = args

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
                # val = row[spec.column_name].decode('utf-8').strip()
                val = row[spec.column_name].strip()

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

    field_spec = ['bpa_id', 'depth', 'sample_date', 'latitude', 'longitude']

    def write_csv(self, samples):
        """
        Write list of sample objects to csv file
        """
        file_name = args['OUTPUT_FILE_PREFIX'] + '_samples.csv'
        with open(file_name, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(self.get_header())
            for sample in samples:
                formatted = [sample.bpa_id, sample.depth, self.get_date_str(sample.sample_date), sample.latitude, sample.longitude]
                writer.writerow(formatted)

    def to_file(self):
        """
        Parse samples
        """

        in_file = Path(args['INPUT_FILE'])
        with open(in_file, 'r') as fd:
            reader = csv.DictReader(fd)
            self.write_csv(self.unpack('Sample', reader))


class SiteHelper(Helper):
    field_spec = ['latitude',
                  'longitude',
                  'site_name',
                  'sample_date',
                  'land_use',
                  'vegetation_total_cover',
                  'vegetation_dominant_trees',
                  'vegetation_dominant_shrubs',
                  'vegetation_dominant_grasses',
                  'elevation',
                  'slope',
                  'slope_aspect',
                  'slope_position',
                  'comments']

    def write_csv(self, tuples):
        """
        Write list of sample objects to csv file
        """
        file_name = args['OUTPUT_FILE_PREFIX'] + '_sites.csv'
        with open(file_name, 'wb') as csvfile:
            sitedict = {}
            writer = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(self.get_header())
            for sample in tuples:
                formatted = [sample.latitude,
                             sample.longitude,
                             sample.site_name,
                             self.get_date_str(sample.sample_date),
                             sample.land_use,
                             sample.vegetation_total_cover,
                             sample.vegetation_dominant_trees,
                             sample.vegetation_dominant_shrubs,
                             sample.vegetation_dominant_grasses,
                             sample.elevation,
                             sample.slope,
                             sample.slope_aspect,
                             sample.slope_position,
                             sample.comments]

                sitedict[(sample.latitude, sample.longitude)] = formatted

            for _, v in sitedict.items():
                writer.writerow(v)

    def to_file(self):
        """
        Parse samples
        """

        in_file = Path(args['INPUT_FILE'])
        with open(in_file, 'r') as fd:
            reader = csv.DictReader(fd)
            self.write_csv(self.unpack('Site', reader))


class ChemHelper(Helper):
    field_spec = ['bpa_id',
                  'sample_date',
                  'moisture',
                  'color',
                  'gravel',
                  'texture',
                  'ammonium_nitrogen',
                  'nitrate_nitrogen',
                  'phosphorus_colwell',
                  'potassium_colwell',
                  'sulphur',
                  'organic_carbon',
                  'conductivity',
                  'ph_cacl2',
                  'ph_h20',
                  'dtpa_copper',
                  'dtpa_iron',
                  'dtpa_manganese',
                  'dtpa_zinc',
                  'exc_aluminium',
                  'exc_calcium',
                  'exc_magnesium',
                  'exc_potasium',
                  'exc_sodium',
                  'exc_boron',
                  'clay',
                  'course_sand',
                  'fine_sand',
                  'sand',
                  'silt']

    def write_csv(self, tuples):
        """
        Write list of chem vals to file
        """
        file_name = args['OUTPUT_FILE_PREFIX'] + '_chem.csv'
        with open(file_name, 'wb') as csvfile:

            writer = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(self.get_header())
            for sample in tuples:
                formatted = [
                    sample.bpa_id,
                    self.get_date_str(sample.sample_date),
                    sample.moisture,
                    sample.color,
                    sample.gravel,
                    sample.texture,
                    sample.ammonium_nitrogen,
                    sample.nitrate_nitrogen,
                    sample.phosphorus_colwell,
                    sample.potassium_colwell,
                    sample.sulphur,
                    sample.organic_carbon,
                    sample.conductivity,
                    sample.ph_cacl2,
                    sample.ph_h20,
                    sample.dtpa_copper,
                    sample.dtpa_iron,
                    sample.dtpa_manganese,
                    sample.dtpa_zinc,
                    sample.exc_aluminium,
                    sample.exc_calcium,
                    sample.exc_magnesium,
                    sample.exc_potasium,
                    sample.exc_sodium,
                    sample.exc_boron,
                    sample.clay,
                    sample.course_sand,
                    sample.fine_sand,
                    sample.sand,
                    sample.silt]

                writer.writerow(formatted)

    def to_file(self):
        """
        Parse samples
        """

        in_file = Path(args['INPUT_FILE'])
        with open(in_file, 'r') as fd:
            reader = csv.DictReader(fd)
            self.write_csv(self.unpack('Site', reader))


def main(args):
    if args['--get-sites'] is not None:
        site_helper = SiteHelper(args)
        site_helper.to_file()

    if args['--get-samples'] is not None:
        sample_helper = SampleHelper(args)
        sample_helper.to_file()

    if args['--get-analysis'] is not None:
        chem_helper = ChemHelper(args)
        chem_helper.to_file()


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

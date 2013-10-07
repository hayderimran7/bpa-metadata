#!/usr/bin/env python
# coding: utf-8

"""
This tool takes the current base format document and re-flows it to a more normalised version.

Usage:
  reflow.py [options] INPUT_FILE OUTPUT_FILE

Options:
  -v, --verbose    Verbose mode.

"""

from unipath import Path
import logging
import sys
import csv
from collections import namedtuple
from docopt import docopt

logging.basicConfig(level=logging.INFO)

__author__ = 'ccg'
__version__ = '0.1'

# maps spreadsheet column name with attribute names, validator and converter functions, if any
ColumnSpec = namedtuple('ColumnSpec', 'name validator converter')
COLUMNS = {'Sample#': ColumnSpec('bpa_id', None, None),
           'Depth (cm)': ColumnSpec('dept', None, None),
           'Site / NP': ColumnSpec('site_name', None, None),
           'Date Sampled': ColumnSpec('sample_date', None, None),
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


def parse_to_named_tuple(type_name, reader, fieldspec):
    """
    Pack the csv data into a type
    """

    typ = namedtuple(type_name, fieldspec)
    for attribute in fieldspec:



def get_samples(reader):
    """
    Unpack the samples
    """

    field_spec = ['bpaid', 'dept', 'sample_date']
    parse_to_named_tuple('Sample', reader, field_spec)


def main(args):
    in_file = Path(args['INPUT_FILE'])
    with open(in_file) as fd:
        reader = csv.DictReader(fd)
        samples = get_samples(reader)




def args_check(args):
    """
    Aborts if passed parameters are not OK
    """
    in_file = Path(args['INPUT_FILE'])
    if not in_file.exists():
        sys.exit("The input file {0} does not exist. Quitting".format(in_file))


if __name__ == '__main__':
    args = docopt(__doc__, version=__version__)

    if args['--verbose']:
        logging.basicConfig(level=logging.DEBUG)
        logging.info(args)

    args_check(args)
    main(args)

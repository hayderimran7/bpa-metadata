#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Converts GPS positions to Decimal degree

Usage:
  reflow.py [options] (POSITION_STRING)

Options:
  -v, --verbose       Verbose mode.

"""

from docopt import docopt
import logging
from collections import namedtuple
import re

logging.basicConfig()
logger = logging.getLogger('GPSConvert')
logger.setLevel(level=logging.INFO)

__author__ = 'ccg'
__version__ = '0.0.1'

PATTERN = re.compile(r"""
                         (?P<north_south>[NS])  # North or South
                         (?P<lat_deg>\d+)°      # Latitude Degrees
                         (?:(?P<lat_min>\d+)')? # Latitude Minutes (Optional)
                         (?:(?P<lat_sec>\d+(\.\d*))")? # Latitude Seconds (Optional)
                         [ ]
                         (?P<east_west>[EW])    # East or West
                         (?P<lon_deg>\d+)°      # Longitude Degrees
                         (?:(?P<lon_min>\d+)')? # Longitude Minutes (Optional)
                         (?:(?P<lon_sec>\d+(\.\d*))")? # Longitude Seconds (Optional)
                      """, re.VERBOSE)

LAT_FIELDS = ("lat_deg", "lat_min", "lat_sec")
LON_FIELDS = ("lon_deg", "lon_min", "lon_sec")
SIGN = {'N': 1, 'S': -1, 'E': 1, 'W': -1}

Position = namedtuple('Position', 'lat, lon')


def parse_dms_string(s, out_type=float):
    """
    Convert a string of the following form to a tuple of out_type latitude, longitude.

    Example input:
    S0°25'30.12", W91°7'
    """
    values = PATTERN.match(s).groupdict()
    pos = tuple(sum(out_type(values[field] or 0) / out_type(60 ** idx) for idx, field in enumerate(field_names)) for field_names in (LAT_FIELDS, LON_FIELDS))

    # fix the signs
    lat = pos[0] * SIGN[values['north_south']]
    lon = pos[1] * SIGN[values['east_west']]
    return Position(lat=lat, lon=lon)


if __name__ == '__main__':
    args = docopt(__doc__, version=__version__)

    if args['--verbose']:
        logger.setLevel(level=logging.DEBUG)

    # print parse_dms_string('''S18°32'40.90" E146°29'17.19"''')
    pos = parse_dms_string(args['POSITION_STRING'])
    print('{0:+f} {1:+f}'.format(pos.lat, pos.lon))

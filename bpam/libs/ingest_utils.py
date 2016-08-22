import string
import re
import unittest
import os
import json

import logger_utils
from datetime import date
from dateutil.parser import parse as date_parser
from ccg_django_utils.conf import EnvConfig
from django.utils.encoding import smart_text

# where to cache downloaded metadata
METADATA_ROOT = os.path.join(os.path.expanduser('~'), 'metadata')

INGEST_NOTE = 'Ingested from Source Document on {0}\n'.format(date.today())

logger = logger_utils.get_logger(__name__)
env = EnvConfig()

# list of chars to delete
remove_letters_map = dict((ord(char), None) for char in string.punctuation + string.ascii_letters)


def get_clean_number(val, default=None, debug=False):
    ''' Try to clean up numbers '''

    if debug:
        logger.debug('Value: {!r}'.format(val))

    if val in (None, ''):
        return default


    if isinstance(val, int):
        return val

    if isinstance(val, float):
        return val

    numbers_only = re.compile(r'[^\d.]+')
    parsed_val = numbers_only.sub('', val)
    if parsed_val == '':
        return default

    try:
        return int(parsed_val)
    except ValueError as e:
        logger.warning('{!r}'.format(e))
        return default


def get_int(val, default=None):
    ''' get a int from a string containing other alpha characters '''

    if val is None:
        return default

    if isinstance(val, int):
        return val

    clean_number = get_clean_number(val, default)
    if clean_number is None:
        return default

    try:
        return int(clean_number)
    except TypeError as e:
        logger.warning('{!r}'.format(e))
        return default


def get_clean_float(val, default=None, stringconvert=True):
    '''
    Try to hammer an arb value into a float.
    If stringconvert is true (the default behaviour), try to convert the string to a float,
    if not, return the given default value
    '''

    def to_float(var):
        try:
            return float(var)
        except ValueError as e:
            logger.warning('Value {0} not floatable, returning default {1}: {2!r}'.format(var, default, e))
            return default
        except TypeError as e:
            logger.warning('Value {0} not floatable, returning default {1}: {2!r}'.format(var, default, e))
            return default

    # if its a float, its probably ok
    if isinstance(val, float):
        return val

    # if its an integer, make it a float
    if isinstance(val, int):
        return to_float(val)

    # the empty string gets the default
    if val == '':
        return default

    # if its not a string, forget it, return the default
    if not isinstance(val, basestring):
        return default

    if stringconvert:
        return to_float(filter(lambda x: x.isdigit(), val))
    else:
        return default


def strip_all(reader):
    ''' Scrub extra whitespace from values in the reader dicts as read from the csv files '''

    entries = []
    for entry in reader:
        new_e = {}
        for k, v in entry.items():
            new_e[k] = smart_text(v.strip())
        entries.append(new_e)

    return entries


def get_date(dt):
    '''
    When reading in the data, and it was set as a date type in the excel sheet it should have been converted.
    if it wasn't, it may still be a valid date string.

    >>> get_date('12-10-1973')

    '''
    if dt is None:
        return None

    if isinstance(dt, date):
        return dt
    if isinstance(dt, basestring):
        if dt.strip() == '':
            return None
        try:
            return date_parser(dt)

        except TypeError as e:
            logger.error('Error parsing date [{}] error: {!r}'.format(dt, e))
            return None
        except ValueError as e:
            logger.error('Error parsing date [{}]: {!r}'.format(dt, e))
            return None
    return None


def pretty_print_namedtuple(named_tuple):
    ''' pretty prints the namedtuple '''

    def json_serial(obj):
        ''' JSON serializer for objects not serializable by default json code '''

        if isinstance(obj, date):
            serial = obj.isoformat()
            return serial

    return json.dumps(named_tuple._asdict(), indent=4, default=json_serial)


if __name__ == "__main__":
    import doctest
    doctest.testmod()



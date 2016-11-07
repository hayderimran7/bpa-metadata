import string
import re
import os
import json

import logger_utils
import datetime
from django.utils.encoding import smart_text

# where to cache downloaded metadata
METADATA_ROOT = os.path.join(os.path.expanduser('~'), 'metadata')

INGEST_NOTE = 'Ingested from Source Document on {0}\n'.format(datetime.date.today())

logger = logger_utils.get_logger(__name__)

# list of chars to delete
remove_letters_map = dict((ord(char), None) for char in string.punctuation + string.ascii_letters)


def get_clean_number(val, default=None, debug=False):
    '''
    Note this will only return ints
    Try to clean up numbers
    >>> get_clean_number(42)
    42
    >>> get_clean_number('42')
    42
    >>> get_clean_number('42.0002')
    42
    >>> get_clean_number('42.10002')
    42
    >>> get_clean_number(-42)
    -42
    >>> get_clean_number(+4)
    4
    '''

    if debug:
        logger.debug('Value: {!r}'.format(val))

    if val in (None, ''):
        return default

    if isinstance(val, int):
        return val

    if isinstance(val, float):
        return val
    float_pattern = re.compile(r'\d+')
    match = float_pattern.search(val)
    if match:
        parsed_val = match.group(0)
    else:
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

    >>> get_clean_float(0.01)
    0.01
    >>> get_clean_float('0.01')
    0.01
    >>> get_clean_float('42.42')
    42.42
    >>> get_clean_float('')
    >>> get_clean_float('0')
    0.0
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
        return to_float(filter(lambda x: x.isdigit() or x in (',', '.'), val))
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
    convert `dt` into a datetime.date, returning `dt` if it is already an
    instance of datetime.date. only two string date formats are supported:
    YYYY-mm-dd and dd/mm/YYYY. if conversion fails, returns None.
    '''

    if dt is None:
        return None

    if isinstance(dt, datetime.date):
        return dt

    if not isinstance(dt, basestring):
        return None

    if dt.strip() == '':
        return None

    try:
        return datetime.datetime.strptime(dt, '%Y-%m-%d').date()
    except ValueError:
        pass

    try:
        return datetime.datetime.strptime(dt, '%d/%m/%Y').date()
    except ValueError:
        pass

    logger.error('Date `{}` is not in a supported format'.format(dt))
    return None


def pretty_print_namedtuple(named_tuple):
    ''' pretty prints the namedtuple '''

    def json_serial(obj):
        ''' JSON serializer for objects not serializable by default json code '''

        if isinstance(obj, datetime.date):
            serial = obj.isoformat()
            return serial

    return json.dumps(named_tuple._asdict(), indent=4, default=json_serial)


if __name__ == "__main__":
    import doctest
    doctest.testmod()

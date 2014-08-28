import string
import pprint
from datetime import date
import unittest
import os
import dateutil
import logger_utils
import subprocess
import time
import sys
import requests

from ccg_django_utils.conf import EnvConfig
from django.utils.encoding import smart_text

# where to cache downloaded metadata
METADATA_ROOT = os.path.join(os.path.expanduser('~'), 'var/metadata')

INGEST_NOTE = "Ingested from Source Document on {0}\n".format(date.today())

logger = logger_utils.get_logger(__name__)
env = EnvConfig()


def fetch_metadata(source_path, target_path, use_cached=True):
    """
    Fetch the metadata from a webserver
    :return:
    """

    if use_cached and os.path.exists(target_path):
        logger.info('Using cached {0}'.format(target_path))
        return

    logger.info('Downloading {0} to {1}'.format(source_path, target_path))

    # ensure target directory exists
    target_path_parent = os.path.dirname(target_path)
    if not os.path.exists(target_path_parent):
        os.makedirs(target_path_parent)

    r = requests.get(source_path, stream=True)
    if r.status_code == 200:
        with open(target_path, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
    else:
        logger.error('URL {0} does not exist'.format(source_path))
        sys.exit()


def fetch_metadata_from_swift():
    logger.info("Fetching metadata from swift")

    swift_user = env.get('SWIFT_USER')
    swift_password = env.get('SWIFT_PASSWORD')

    cmd = 'swift -V 2 --os-auth-url={0} --os-username={1} --os-password={2} --os-tenant-name=bpa download {3}'.format(
        'https://keystone.bioplatforms.com/v2.0/',
        swift_user,
        swift_password,
        'bpa-metadata-source',
    )

    logger.info(cmd)
    if not os.path.exists(METADATA_ROOT):
        os.makedirs(METADATA_ROOT)

    # messy... shell=True is needed because swift lives in a virtualenv
    swift_process = subprocess.call(cmd, shell=True, cwd=METADATA_ROOT)
    swift_process.wait()


def ensure_metadata_is_current():
    """
    Ensure that the metadata folder exists and is relatively up to data
    """
    ONE_DAY = 86400  # seconds

    # if there is no metadata, get it
    if not os.path.exists(METADATA_ROOT):
        logger.warning("No metada locally available, fetching it from swift")
        fetch_metadata_from_swift()
        return

    # if the metadata is old, fetch it
    now = time.time()
    last_time = os.path.getmtime(METADATA_ROOT)
    if now - last_time > ONE_DAY:
        fetch_metadata_from_swift()


def get_clean_number(val, default=None):
    """
    Try to clean up numbers
    """
    if val in (None, ""):
        return default

    if isinstance(val, float):
        return val

    remove_letters_map = dict((ord(char), None) for char in string.letters)
    try:
        return int(val.translate(remove_letters_map))
    except ValueError:
        return default


def get_int(val, default=None):
    """
    get a int from a string containing other alpha characters
    """
    try:
        return int(get_clean_number(val, default))
    except TypeError:
        return default


def get_clean_float(val, default=None, stringconvert=True):
    """
    Try to hammer an arb value into a float.
    If stringconvert is true (the default behaviour), try to convert the string to a float,
    if not, return the given default value
    """

    def to_float(var):
        try:
            return float(var)
        except ValueError:
            logger.warning("ValueError Value '{0}' not floatable, returning default '{1}'".format(var, default))
            return default
        except TypeError:
            logger.warning("TypeError Value '{0}' not floatable, returning default '{1}'".format(var, default))
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
    """
    Scrub extra whitespace from values in the reader dicts as read from the csv files 
    """

    entries = []
    for entry in reader:
        new_e = {}
        for k, v in entry.items():
            new_e[k] = smart_text(v.strip())
        entries.append(new_e)

    return entries


def get_date(dt):
    """
    When reading in the data, and it was set as a date type in the excel sheet it should have been converted.
    if it wasn't, it may still be a valid date string.
    """

    if dt is None:
        return None

    if isinstance(dt, date):
        return dt
    if isinstance(dt, basestring):
        if dt.strip() == '':
            return None
        try:
            return dateutil.parser.parse(dt)
        except TypeError, e:
            logger.error("Date parsing error " + str(e))
            return None
    return None


def pretty_print_namedtuple(named_tuple):
    """
    pretty prints the namedtuple
    """
    return pprint.pformat(named_tuple._asdict())


class TestGetCleanFloat(unittest.TestCase):
    """
    get_clean_float tester
    """

    def setUp(self):
        self.floats = (12131.5345, 22.444, 33.0)

    def test_get_clean_float(self):
        for f in self.floats:
            self.assertTrue(f == get_clean_float(f))

    def test_xxx(self):
        self.assertTrue(get_clean_float('', 'XXX') == 'XXX')

    def test_none(self):
        self.assertTrue(get_clean_float('') is None)

    def test_int(self):
        self.assertTrue(get_clean_float(123) == 123)


if __name__ == '__main__':
    unittest.main()

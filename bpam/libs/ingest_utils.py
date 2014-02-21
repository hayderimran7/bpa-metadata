import string
import pprint
from datetime import date

import dateutil
from django.utils.encoding import smart_text

from apps.common.models import Organism, DNASource
from logger_utils import get_logger


INGEST_NOTE = "Ingested from GoogleDocs on {0}\n".format(date.today())

logger = get_logger('Ingest Utils')


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


def get_clean_float(val, default=None):
    """
    Try to hammer an arb value into a float
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

    remove_letters_map = dict((ord(char), None) for char in string.letters)
    return to_float(val.translate(None, string.letters))


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


def add_organism(genus='', species=''):
    """
    Only add organism if it does not already exist
    """
    try:
        Organism.objects.get(genus=genus, species=species)
    except Organism.DoesNotExist:
        organism = Organism(genus=genus, species=species)
        organism.save()


def get_dna_source(description):
    """
    Get a DNA source if it exists, if it doesn't make it.
    """

    description = description.capitalize()

    try:
        source = DNASource.objects.get(description=description)
    except DNASource.DoesNotExist:
        source = DNASource(description=description)
        source.save()

    return source


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



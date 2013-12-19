import string
import logging
from datetime import date
import dateutil

from django.utils.encoding import smart_text

from apps.common.models import Organism, DNASource


INGEST_NOTE = "Ingested from GoogleDocs on {0}".format(date.today())

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('UTILS')


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
    remove_letters_map = dict((ord(char), None) for char in string.letters)
    try:
        return float(val.translate(remove_letters_map))
    except ValueError:
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


def add_organism(genus='', species=''):
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
    if isinstance(dt, date):
        return dt
    if isinstance(dt, basestring):
        if dt.strip() == '':
            return None
        return dateutil.parser.parse(dt)
    return None




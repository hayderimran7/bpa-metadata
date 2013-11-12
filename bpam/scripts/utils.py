import string
import logging
from datetime import date
import dateutil

from django.utils.encoding import smart_text

from apps.common.models import Organism, BPAUniqueID, BPAProject, DNASource

BPA_ID = "102.100.100"
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


def get_date(val):
    """
    Because dates in he spreadsheets comes in all forms, dateutil is used to figure it out.  
    """
    return dateutil.parser.parse(val)


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


def add_organism(genus="", species=""):
    organism = Organism(genus=genus, species=species)
    organism.save()


def add_bpa_id(idx, project_name, note=INGEST_NOTE):
    """
    Add a BPA ID
    """

    lbl = BPAUniqueID(bpa_id=idx)
    lbl.project = BPAProject.objects.get(name=project_name)
    lbl.note = note
    lbl.save()
    logger.info("Added BPA Unique ID: " + str(lbl))


def ingest_bpa_ids(data, project_name):
    """
    The BPA ID's are unique
    """

    id_set = set()
    for e in data:
        bpa_id = e['bpa_id'].strip()
        if is_bpa_id(bpa_id):
            id_set.add(bpa_id)

    for bpa_id in id_set:
        add_bpa_id(bpa_id, project_name)


def get_bpa_id(bpa_id, project_name, note=INGEST_NOTE):
    """
    Get a BPA ID, if it does not exist, make it
    """

    try:
        bid = BPAUniqueID.objects.get(bpa_id=bpa_id)
    except BPAUniqueID.DoesNotExist:
        logger.info("BPA ID {0} does not exit, adding it".format(bpa_id))
        bid = BPAUniqueID(bpa_id=bpa_id)
        bid.project = BPAProject.objects.get(name=project_name)
        bid.note = note
        bid.save()

    return bid


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


def check_date(dt):
    """
    When reading in the data, and it was set as a date type in the excel sheet it should have been converted.
    if it wasn't, it may still be a valid date string.
    """
    if isinstance(dt, date):
        return dt
    if isinstance(dt, basestring):
        if dt.strip() == "":
            return None
        return dateutil.parser.parse(dt)


def is_bpa_id(bpa_id):
    """
    Determines if id is a good BPA ID
    """
    bpa_id = bpa_id.strip()
    # empties
    if bpa_id == '':
        return False

    # no BPA prefix
    if bpa_id.find(BPA_ID) == -1:
        return False

    # this function has failed to find a reason why this can't be a BPA ID....
    return True


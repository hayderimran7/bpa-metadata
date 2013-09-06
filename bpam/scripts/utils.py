import string
from datetime import date

from dateutil import parser

from bpaauth.models import BPAUser
from common.models import *


INGEST_NOTE = "Ingested from GoogleDocs on {0}".format(date.today())


def get_clean_number(str, default=None):
    try:
        return int(str.translate(None, string.letters))
    except ValueError:
        return default


def get_clean_float(str, default=None):
    try:
        return float(str.translate(None, string.letters))
    except ValueError:
        return default


def get_date(date_str):
    """
    Because dates in he spreadsheets comes in all forms, dateutil is used to figure it out.  
    """
    return parser.parse(date_str)


def strip_all(reader):
    """
    Scrub extra whitespace from values in the reader dicts as read from the csv files 
    """

    entries = []
    for entry in reader:
        new_e = {}
        for k, v in entry.items():
            new_e[k] = v.strip()
        entries.append(new_e)

    return entries


def add_organism(genus="", species=""):
    organism = Organism(genus=genus, species=species)
    organism.save()


def add_bpa_id(id, project_name, note=INGEST_NOTE):
    """
    Add a bpa
    ID"""

    lbl = BPAUniqueID(bpa_id=id)
    lbl.project = BPAProject.objects.get(name=project_name)
    lbl.note = note
    lbl.save()
    print("Added BPA Unique ID: " + str(lbl))


def ingest_bpa_ids(data, project_name):
    """ The BPA ID's are unique """

    id_set = set()
    for e in data:
        id_set.add(e['bpa_id'].strip())
    for id in id_set:
        add_bpa_id(id, project_name)


def get_bpa_id(id, project_name, note=INGEST_NOTE):
    """
    Get a BPA ID, if it does not exist, make it
    """

    try:
        bid = BPAUniqueID.objects.get(bpa_id=id)
    except BPAUniqueID.DoesNotExist:
        print("BPA ID {0} does not exit, adding it".format(id))
        bid = BPAUniqueID(bpa_id=id)
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

    

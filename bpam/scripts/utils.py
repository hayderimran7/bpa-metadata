import csv
import string
from datetime import date
from bpaauth.models import BPAUser
from common.models import *
from dateutil import parser
import pprint

INGEST_NOTE = "Ingested from GoogleDocs on {}".format(date.today()) 

def get_clean_number(str, default=None):
    try:
        return int(str.translate(None, string.letters))
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

def ingest_bpa_ids(data, project_name):
    """ The BPA ID's are unique """
    
    def add_BPA_ID(id):
        lbl = BPAUniqueID(bpa_id=id)
        lbl.project = BPAProject.objects.get(name=project_name)
        lbl.note = INGEST_NOTE
        lbl.save()
        print("Ingested BPA Unique ID: " + str(lbl))    
    
    id_set = set()
    for e in data:
        id_set.add(e['bpa_id'].strip()) 
    for id in id_set:
        add_BPA_ID(id)

def get_dna_source(description):
    """ Get a DNA source if it exists, if it doesn't make it. """

    description = description.capitalize()

    try:
        source = DNASource.objects.get(description=description)
    except DNASource.DoesNotExist:
        source = DNASource(description=description)
        source.save()
    
    return source

    

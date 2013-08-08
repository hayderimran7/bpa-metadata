import pprint
import csv
import string
from datetime import date

from apps.bpaauth.models import BPAUser
from apps.common.models import *
from apps.base_soil_agricultural.models import * 

from .utils import *

SAMPLE_FILE = './scripts/data/base_soil_agric_sample.csv'


def ingest_land_use_taxonomy():
    
    land_uses = ('Conservation and Natural Environments',
                 'Production from relatively natural Environments',
                 'Production from dryland agriculture and plantations',
                 'Production from irrigated agriculture and plantations',
                 'Intensive uses',
                 'Water')
    for use in land_uses:
        u = LandUse(description=use)
        u.save()
     

def get_sample_data():
    with open(SAMPLE_FILE, 'rb') as samples:
        fieldnames = ['bpa_id',
                      'sample_name',
                      'sample_depth',
                      'plot_description',
                      'owner',
                      'collection_date',
                      'country',
                      'state',
                      'location',
                      'image_url',
                      'lat',
                      'long',
                      'elevation',
                      'current_land_use',
                      'correction',
                      'current_vegetation',
                      'previous_land_use',
                      'crop_rotation',
                      'agrochemical_additions',
                      'tillage',
                      'fire',
                      'flooding',
                      'extreme_events',
                      'other',
                      'horizon',
                      'fao_classification_soil_type',
                      'australian_classification_soil_type',
                      'slope_gradient',
                      'slope_aspect',
                      'profile_position',
                      'drainage_classification',
                      'notes',
                      ]
                  
        reader = csv.DictReader(samples, fieldnames=fieldnames, restkey='the_rest')
        return strip_all(reader)


def get_collection_site(e):
    """ Add a collection site"""
    
    collection_site = CollectionSite()
    collection_site.sample_depth = e['sample_depth']
    collection_site.note = e['notes']
    collection_site.lat = e['lat']
    collection_site.long = e['long']
    collection_site.elevation = e['elevation']
    collection_site.slope_gradient = e['slope_gradient']
    collection_site.slope_aspect = e['slope_aspect']
    collection_site.profile_position = e['profile_position']
    collection_site.drainage = e['drainage_classification']
    collection_site.australian_classification_soil_type = e['australian_classification_soil_type']
    collection_site.note = e['notes']
    
    collection_site.save()
    
    return collection_site    

def add_sample(e):
    bpa_id = e['bpa_id']
    try:
        SoilSample.objects.get(bpa_id__bpa_id=bpa_id)
    except SoilSample.DoesNotExist:
        sample = SoilSample()
        sample.bpa_id = BPAUniqueID.objects.get(bpa_id=bpa_id)
        sample.name = e['sample_name']
        sample.collection_site = get_collection_site(e)
        sample.note = pprint.pprint(e)
        sample.save()
        print("Ingested Soil sample {}".format(sample.name))

def run():
    ingest_land_use_taxonomy()
        
    data = get_sample_data()
    ingest_bpa_ids(data, 'BASE Soil Agricultural')
    
    for e in data:
        add_sample(e)
    
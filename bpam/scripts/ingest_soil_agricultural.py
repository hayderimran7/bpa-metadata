import pprint
import csv
import string
from datetime import date

from apps.bpaauth.models import BPAUser
from apps.common.models import *
from apps.base_soil_agricultural.models import * 

from .utils import *

SAMPLE_FILE = './scripts/data/base_soil_agric_sample.csv'

def get_sample_data():
    with open(SAMPLE_FILE, 'rb') as samples:
        fieldnames = ['bpa_id',
                      'sample_name',
                      'soil_dept',
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


def add_sample(e):
    bpa_id = e['bpa_id']
    try:
        SoilSample.objects.get(bpa_id__bpa_id=bpa_id)
    except SoilSample.DoesNotExist:
        sample = SoilSample()
        sample.bpa_id = BPAUniqueID.objects.get(bpa_id=bpa_id)
        sample.name = e['sample_name']

        sample.note = e['notes']
        sample.save()
        print("Ingested Soil sample {}".format(sample.name))

def run():
    data = get_sample_data()
    ingest_bpa_ids(data, 'BASE Soil Agricultural')
    
    for e in data:
        add_sample(e)
    
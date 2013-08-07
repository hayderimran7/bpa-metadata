import csv
import string
from datetime import date
from bpaauth.models import BPAUser
from common.models import *
import pprint

from utils import *

SAMPLE_DATA = './scripts/data/base_soil_agric_sample.csv'

def get_sample_data():
    with open(SAMPLE_FILE, 'rb') as samples:
        fieldnames = ['bpa_id',
                      'name',
                      'soil_dept',
                      'plot_description',
                      'owner',
                      
                      ]
                  
        reader = csv.DictReader(samples, fieldnames=fieldnames)
        return strip_all(reader)

def run():
    data = get_sample_data()
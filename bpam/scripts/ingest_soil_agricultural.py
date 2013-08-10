import pprint
import csv
import string
from datetime import date

from apps.bpaauth.models import BPAUser
from apps.common.models import *
from apps.base_soil_agricultural.models import * 

from .utils import *

SAMPLE_FILE = './scripts/data/base_soil_agric_sample.csv'
CHEM_FILE = './scripts/data/base_soil_agric_chem.csv'

def get_sample_data():
    with open(SAMPLE_FILE, 'rb') as samples:
        fieldnames = ['bpa_id',
                      'sample_name',
                      'depth',
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

def get_chem_data():
    with open(CHEM_FILE, 'rb') as samples:        
        fieldnames = ['bpa_id',
                      'lab_name_id',
                      'customer',
                      'depth',
                      'colour',
                      'gravel',
                      'texture',
                      'ammonium_nitrogen',
                      'nitrate_nitrogen',
                      'phosphorus_colwell',    
                      'potassium_colwell',
                      'sulphur_colwell',
                      'organic_carbon',
                      'conductivity',
                      'cacl2_ph',    
                      'h2o_ph',
                      'dtpa_copper',
                      'dtpa_iron', 
                      'dtpa_manganese',
                      'dtpa_zinc',
                      'exc_aluminium', 
                      'exc_calcium', 
                      'exc_magnesium',
                      'exc_potassium',
                      'exc_sodium',
                      'boron_hot_cacl2', 
                      'clay',
                      'course_sand',
                      'fine_sand', 
                      'sand', 
                      'silt', 
                      'silt_unit',
                      'sodium',
                      'sodium_unit',
                      'magnesium',
                      'magnesium_unit', 
                      'aluminium',
                      'aluminium_unit',
                      'boron',
                      'boron_unit']
                  
        reader = csv.DictReader(samples, fieldnames=fieldnames, restkey='the_rest')
        return strip_all(reader)


def get_collection_site(e):
    """ Add a collection site"""
    
    collection_site = CollectionSite()
    collection_site.plot_description = e['plot_description']
    collection_site.sample_depth = e['depth']
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
        sample.note = pprint.pformat(e)
        sample.save()
        print("Ingested Soil sample {}".format(sample.name))

def add_chem_sample(e):
            
    chema = ChemicalAnalysis()
    chema.bpa_id = BPAUniqueID(e['bpa_id'])
    chema.lab_name_id = e['lab_name_id']
    chema.customer = e['customer']
    chema.depth = e['depth']
    chema.colour = e['colour']
    chema.gravel = e['gravel']
    chema.texture = e['texture']    
    chema.ammonium_nitrogen = get_clean_float(e['ammonium_nitrogen'])
    chema.nitrate_nitrogen = e['nitrate_nitrogen'] # <>
    chema.phosphorus_colwell = e['phosphorus_colwell'] # <>
    chema.potassium_colwell = get_clean_float(e['potassium_colwell'])
    chema.sulphur_colwell = get_clean_float(e['sulphur_colwell'])
    chema.organic_carbon = get_clean_float(e['organic_carbon'])
    chema.conductivity = get_clean_float(e['conductivity'])
    chema.cacl2_ph = get_clean_float(e['cacl2_ph'])
    chema.h20_ph = get_clean_float(e['h2o_ph'])
    chema.dtpa_copper = get_clean_float(e['dtpa_copper'])
    chema.dtpa_iron = get_clean_float(e['dtpa_iron'])
    chema.dtpa_manganese = get_clean_float(e['dtpa_manganese']) 
    chema.dtpa_zinc = get_clean_float(e['dtpa_zinc'])
    chema.exc_aluminium = get_clean_float(e['exc_aluminium'])
    chema.exc_calcium = get_clean_float(e['exc_calcium'])
    chema.exc_magnesium = get_clean_float(e['exc_magnesium'])
    chema.exc_potassium = get_clean_float(e['exc_potassium'])
    chema.exc_sodium = get_clean_float(e['exc_sodium'])
    chema.boron_hot_cacl2 = get_clean_float(e['boron_hot_cacl2'])
    
    chema.clay = get_clean_float(e['clay'])
    chema.course_sand = get_clean_float(e['course_sand'])
    chema.fine_sand = get_clean_float(e['fine_sand'])
    chema.sand = get_clean_float(e['sand'])
    chema.silt = get_clean_float(e['silt'])
    
    chema.save()

def run():
    
    LandUse.makeall()
    
    data = get_sample_data()
    ingest_bpa_ids(data, 'BASE Soil Agricultural')
              
    for e in data:
        add_sample(e)
    
    chem_data = get_chem_data()
    for e in chem_data:
        add_chem_sample(e)
    
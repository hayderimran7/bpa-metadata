import pprint
import csv
import re
import os.path
from datetime import date

from apps.BASE.models import GPSPosition, CollectionSite, SoilSample, ChemicalAnalysis, BPAUniqueID

from libs import ingest_utils

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
SAMPLE_FILE = os.path.join(DATA_DIR, 'base_soil_agric_sample.csv')
CHEM_FILE = os.path.join(DATA_DIR, 'base_soil_agric_chem.csv')


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
                      'location_name',
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
        return ingest_utils.strip_all(reader)


def get_chem_data():
    with open(CHEM_FILE, 'rb') as samples:
        fieldnames = ['bpa_id',
                      'lab_name_id',
                      'customer',
                      'depth',
                      'soilcolour',
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
        return ingest_utils.strip_all(reader)


def get_collection_site(e):
    """ Add a collection site"""

    point_regexp = r'\d{1,4}m [S|N]\d{1,2}.\d{5} [E|W]\d{1,3}.\d{5}'

    def get_gps_description(site):
        """ Construct a GPS description field """

        return "{0} {1} {2} {3}".format(site.country, site.state, site.location, site.plot_description)

    def add_position(site, e_lat, e_long, e_elevation):
        """ The current spreadsheet has all data in the lat column..."""

        found = re.findall(point_regexp, e_lat)

        for p in found:
            elevation, lat, long = p.split()
            elevation = ingest_utils.get_clean_float(elevation)
            lat = ingest_utils.get_clean_float(lat)
            long = ingest_utils.get_clean_float(long)

            gps = GPSPosition(longitude=long, latitude=lat, elevation=elevation)
            gps.description = get_gps_description(site)
            gps.save()
            site.positions.add(gps)

    collection_site = CollectionSite()
    collection_site.country = e['country']
    collection_site.state = e['state']
    collection_site.location = e['location_name']
    collection_site.image_url = e['image_url']
    collection_site.horizon = e['horizon']
    collection_site.plot_description = e['plot_description']
    collection_site.sample_depth = e['depth']
    collection_site.note = e['notes']
    collection_site.slope_gradient = e['slope_gradient']
    collection_site.slope_aspect = e['slope_aspect']
    collection_site.profile_position = e['profile_position']
    collection_site.drainage = e['drainage_classification']
    collection_site.australian_classification_soil_type = e['australian_classification_soil_type']
    collection_site.note = e['notes']
    collection_site.save()
    add_position(collection_site, e['lat'], e['long'], e['elevation'])

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
        sample.collection_date = ingest_utils.get_date(e['collection_date'])
        sample.note = pprint.pformat(e)
        sample.save()
        print("Ingested Soil sample {0}".format(sample.name))


def add_chem_sample(e):
    chema = ChemicalAnalysis()
    chema.bpa_id = ingest_utils.get_bpa_id(e['bpa_id'], project_name='BASE',
                              note="Created during chem sample ingestion on {0}".format(date.today()))
    chema.lab_name_id = e['lab_name_id']
    chema.customer = e['customer']
    chema.depth = e['depth']
    chema.colour = e['soilcolour']
    chema.gravel = e['gravel']
    chema.texture = e['texture']
    chema.ammonium_nitrogen = ingest_utils.get_clean_float(e['ammonium_nitrogen'])
    chema.nitrate_nitrogen = e['nitrate_nitrogen']  # <>
    chema.phosphorus_colwell = e['phosphorus_colwell']  # <>
    chema.potassium_colwell = ingest_utils.get_clean_float(e['potassium_colwell'])
    chema.sulphur_colwell = ingest_utils.get_clean_float(e['sulphur_colwell'])
    chema.organic_carbon = ingest_utils.get_clean_float(e['organic_carbon'])
    chema.conductivity = ingest_utils.get_clean_float(e['conductivity'])
    chema.cacl2_ph = ingest_utils.get_clean_float(e['cacl2_ph'])
    chema.h20_ph = ingest_utils.get_clean_float(e['h2o_ph'])
    chema.dtpa_copper = ingest_utils.get_clean_float(e['dtpa_copper'])
    chema.dtpa_iron = ingest_utils.get_clean_float(e['dtpa_iron'])
    chema.dtpa_manganese = ingest_utils.get_clean_float(e['dtpa_manganese'])
    chema.dtpa_zinc = ingest_utils.get_clean_float(e['dtpa_zinc'])
    chema.exc_aluminium = ingest_utils.get_clean_float(e['exc_aluminium'])
    chema.exc_calcium = ingest_utils.get_clean_float(e['exc_calcium'])
    chema.exc_magnesium = ingest_utils.get_clean_float(e['exc_magnesium'])
    chema.exc_potassium = ingest_utils.get_clean_float(e['exc_potassium'])
    chema.exc_sodium = ingest_utils.get_clean_float(e['exc_sodium'])
    chema.boron_hot_cacl2 = ingest_utils.get_clean_float(e['boron_hot_cacl2'])

    chema.clay = ingest_utils.get_clean_float(e['clay'])
    chema.course_sand = ingest_utils.get_clean_float(e['course_sand'])
    chema.fine_sand = ingest_utils.get_clean_float(e['fine_sand'])
    chema.sand = ingest_utils.get_clean_float(e['sand'])
    chema.silt = ingest_utils.get_clean_float(e['silt'])

    chema.save()


def run():
    data = get_sample_data()
    ingest_utils.ingest_bpa_ids(data, 'BASE')

    for e in data:
        add_sample(e)

    chem_data = get_chem_data()
    for e in chem_data:
        add_chem_sample(e)

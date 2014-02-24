# -*- coding: utf-8 -*-

from unipath import Path

from libs.excel_wrapper import ExcelWrapper
from libs import bpa_id_utils
from libs import ingest_utils
from libs import logger_utils
from apps.base.models.site import CollectionSite


logger = logger_utils.get_logger('BASE Contextual')

DATA_DIR = Path(Path(__file__).ancestor(3), "data/base/")
DEFAULT_SPREADSHEET_FILE = Path(DATA_DIR, 'contextual')

BPA_ID_PREFIX = "102.100.100"
BASE_DESCRIPTION = 'BASE'


def get_data(file_name):
    """
    The data sets is relatively small, so make a in-memory copy to simplify some operations.
    """
    field_spec = [('full_id', 'FULL_ID', None),
                  ('sample_id', 'Sample_id', None),  # the one I care about 102.100.100 + sample_id
                  ('date_sampled', 'Date sampled', ingest_utils.get_date),
                  ('lat', 'lat (-)', ingest_utils.get_clean_float),
                  ('lon', 'lon', ingest_utils.get_clean_float),
                  ('upper_depth', 'Upper Depth', None),
                  ('lower_depth', 'Lower depth', None),
                  ('horizon', 'Horizon controlled vocab (1)', None),
                  ('note', 'Notes', None),
                  ('description', 'Description', None),
                  ('current_land_use', 'Current land-use controlled vocab (2)', None),
                  ('general_ecological_zone', 'General Ecological Zone controlled vocab (3)', None),
                  ('vegetation_type_descriptive', 'Vegetation Type (descriptive)', None),
                  ('vegetation_type_controlled_vocab', 'Vegetation Type Controlled vocab (4)', None),
                  ('vegetation_total_cover', 'Vegetation Total cover (%)', None),
                  ('vegetation_dom_trees', 'Vegetation Dom. Trees (%)', None),
                  ('elevation', 'Elevation ()', None),
                  ('slope', 'Slope (%)', None),
                  ('slope_aspect', u'Slope Aspect (Direction or degrees; e.g., NW or 315°)', None),
                  ('profile_position', 'Profile Position controlled vocab (5)', None),
                  ('other_comments', 'Other comments', None),
                  ('australian_soil_classification', 'Australian Soil Classification controlled vocab (6)', None),
                  ('fao', 'FAO soil classification controlled vocab (7)', None),
                  ('immediate_previous_land_use', 'Immediate Previous Land Use controlled vocab (2)', None),
                  ('date_since_change_in_land_use', 'Date since change in Land Use', None),
                  ('crop_rotation_1', 'Crop rotation 1yr since present', None),
                  ('crop_rotation_2', 'Crop rotation 2yrs since present', None),
                  ('crop_rotation_3', 'Crop rotation 3yrs since present', None),
                  ('crop_rotation_4', ' Crop rotation 4yrs since present', None),  # notice the silly space
                  ('crop_rotation_5', 'Crop rotation 5yrs since present', None),
                  ('agrochemical_additions', 'Agrochemical Additions', None),
                  ('tillage', 'Tillage controlled vocab (9)', None),
                  ('last_fire', 'Fire', None),
                  ('fire_intensity', 'fire intensity if known', None),
                  ('flooding', 'Flooding', None),
                  ('extreme_events', 'Extreme Events', None),
                  # nice data
                  ('soil_moisture', 'Soil moisture (%)', None),
                  ('soil_color', 'Color controlled vocab (10)', None),
                  ('gravel', 'Gravel (%) - ( >2.0 mm)', None),
                  ('texture', 'Texture ()', None),
                  ('course_sand', u'Course Sand (%) (200-2000 µm)', None),
                  ('fine_sand', u'Fine Sand (%) - (20-200 µm)', None),
                  ('sand', 'Sand (%)', None),
                  ('silt', u'Silt  (%) (2-20 µm)', None),
                  ('clay', u'Clay (%) (<2 µm)', None),
                  ('ammonium_nitrogen', 'Ammonium Nitrogen (mg/Kg)', None),
                  ('nitrate_nitrogen', 'Nitrate Nitrogen (mg/Kg)', None),
                  ('phosphorus_collwell', 'Phosphorus Colwell (mg/Kg)', None),
                  ('potassium_collwell', 'Potassium Colwell (mg/Kg)', None),
                  ('sulphur', 'Sulphur (mg/Kg)', None),
                  ('organic_carbon', 'Organic Carbon (%)', None),
                  ('conductivity', 'Conductivity (dS/m)', None),
                  ('cacl_ph', 'pH Level (CaCl2) (pH)', None),
                  ('h20_ph', 'pH Level (H2O) (pH)', None),
                  ('dtpa_copper', 'DTPA Copper (mg/Kg)', None),
                  ('dtpa_iron', 'DTPA Iron (mg/Kg)', None),
                  ('dtpa_manganese', 'DTPA Manganese (mg/Kg)', None),
                  ('dtpa_zinc', 'DTPA Zinc (mg/Kg)', None),
                  ('exc_aluminium', 'Exc. Aluminium (meq/100g)', None),
                  ('exc_calcium', 'Exc. Calcium (meq/100g)', None),
                  ('exc_magnesium', 'Exc. Magnesium (meq/100g)', None),
                  ('exc_potassium', 'Exc. Potassium (meq/100g)', None),
                  ('exc_sodium', 'Exc. Sodium (meq/100g)', None),
                  ('boron_hot_cacl2', 'Boron Hot CaCl2 (mg/Kg)', None),
                  ('total_nitrogen', 'Total Nitrogen', None),
                  ('total_carbon', 'Total Carbon', None),
    ]

    wrapper = ExcelWrapper(field_spec,
                           file_name,
                           sheet_name='Sample_info',
                           header_length=1,
                           column_name_row_index=0)

    return wrapper.get_all()


def add_site(data):
    """
    Add site
    """
    for e in data:
        idx = '{0}.{1}'.format(BPA_ID_PREFIX, e.sample_id)  # make a BPA ID string
        bpa_id = bpa_id_utils.get_bpa_id(idx, 'BASE', 'BASE')
        if not bpa_id:
            logger.warning('Ignoring {0}, not a good BPA ID'.format(idx))
            continue

        # only make a site once, the first entry wins
        if e.lat is None or e.lon is None:
            continue
        site, created = CollectionSite.objects.get_or_create(lat=-1 * e.lat, lon=e.lon)
        if created:
            site.location_name = e.description
            site.save()


def run(file_name=DEFAULT_SPREADSHEET_FILE):
    """
    Pass parameters like below:
    vpython-bpam manage.py runscript ingest_base_454 --script-args Melanoma_study_metadata.xlsx
    """

    data = list(get_data(file_name))
    add_site(data)


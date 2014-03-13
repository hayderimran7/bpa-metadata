# -*- coding: utf-8 -*-

from unipath import Path

from libs.excel_wrapper import ExcelWrapper
from libs import bpa_id_utils
from libs import ingest_utils
from libs import logger_utils
from apps.base_contextual.models import *


logger = logger_utils.get_logger(__name__)

DATA_DIR = Path(Path(__file__).ancestor(3), "data/base/")
DEFAULT_SPREADSHEET_FILE = Path(DATA_DIR, 'contextual')

BPA_ID_PREFIX = "102.100.100"
BASE_DESCRIPTION = 'BASE'


def get_horizon_classifications(classification_str):
    """
    map the classification string to the classification object
    """

    def parse_classifiers(classification_str):
        """
        Return a tuple with the classifier or None
        """
        splitted = map(lambda s: s.strip(), classification_str.split(','))
        if len(splitted) == 1:
            tup = splitted[0], u''
        if len(splitted) == 2:
            tup = splitted

        return tup

    def get_classifier(class_str):
        if not class_str.strip():
            return None

        try:
            return HorizonClassification.objects.get(horizon=class_str)
        except HorizonClassification.DoesNotExist:
            logger.warning('No such Horizon Classification as >{0}<'.format(class_str))
            return None

    return map(get_classifier, parse_classifiers(classification_str))


def get_data(file_name):
    """
    The data sets is relatively small, so make a in-memory copy to simplify some operations.
    """

    field_spec = [('full_id', 'FULL_ID', None),
                  ('sample_id', 'Sample_id', ingest_utils.get_int),  # the one I care about 102.100.100 + sample_id
                  ('date_sampled', 'Date sampled', ingest_utils.get_date),
                  ('lat', 'lat (-)', ingest_utils.get_clean_float),
                  ('lon', 'lon', ingest_utils.get_clean_float),
                  ('upper_depth', 'Upper Depth', None),
                  ('lower_depth', 'Lower depth', None),
                  ('horizon_classification', 'Horizon controlled vocab (1)', None),
                  ('note', 'Notes', None),
                  ('description', 'Description', None),
                  ('current_land_use', 'Current land-use controlled vocab (2)', None),
                  ('general_ecological_zone', 'General Ecological Zone controlled vocab (3)', None),
                  ('vegetation_type_descriptive', 'Vegetation Type (descriptive)', None),
                  ('vegetation_type_controlled_vocab', 'Vegetation Type Controlled vocab (4)', None),
                  ('vegetation_total_cover', 'Vegetation Total cover (%)', None),
                  ('vegetation_dominant_trees', 'Vegetation Dom. Trees (%)', None),
                  ('elevation', 'Elevation ()', ingest_utils.get_clean_number),
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
                  ('fire_history', 'Fire', None),
                  ('fire_intensity', 'fire intensity if known', None),
                  ('flooding', 'Flooding', None),
                  ('extreme_events', 'Extreme Events', None),
                  # soil structual
                  ('soil_moisture', 'Soil moisture (%)', ingest_utils.get_clean_float),
                  ('soil_colour', 'Color controlled vocab (10)', None),
                  ('gravel', 'Gravel (%) - ( >2.0 mm)', None),
                  ('texture', 'Texture ()', ingest_utils.get_clean_float),
                  ('course_sand', u'Course Sand (%) (200-2000 µm)', ingest_utils.get_clean_float),
                  ('fine_sand', u'Fine Sand (%) - (20-200 µm)', ingest_utils.get_clean_float),
                  ('sand', 'Sand (%)', ingest_utils.get_clean_float),
                  ('silt', u'Silt  (%) (2-20 µm)', ingest_utils.get_clean_float),
                  ('clay', u'Clay (%) (<2 µm)', ingest_utils.get_clean_float),
                  # soil chemical
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


def get_bpa_id(e):
    """
    Get or make BPA ID
    """
    idx = '{0}.{1}'.format(BPA_ID_PREFIX, e.sample_id)  # make a BPA ID string
    bpa_id = bpa_id_utils.get_bpa_id(idx, 'BASE', 'BASE')
    if not bpa_id:
        logger.warning('Ignoring {0}, not a good BPA ID'.format(idx))
        return None
    return bpa_id


def get_landuse(entry):
    landuse_str = entry.current_land_use
    if landuse_str == '':
        return None

    try:
        return LandUse.objects.get(description__iexact=landuse_str)
    except LandUse.DoesNotExist:
        logger.warning('Land Use description "{0}" on line {1} not known'.format(landuse_str, entry.row))
        return None


def get_general_ecological_zone(entry):
    zone_str = entry.general_ecological_zone
    if zone_str == '':
        return None

    try:
        return GeneralEcologicalZone.objects.get(description__iexact=zone_str)
    except GeneralEcologicalZone.DoesNotExist:
        logger.warning('General Ecological Zone "{0}" on line {1} not known'.format(zone_str, entry.row))
        return None


def get_vegetation_type(entry):
    veg_str = entry.vegetation_type_controlled_vocab
    if veg_str == '':
        return None

    try:
        return BroadVegetationType.objects.get(vegetation__iexact=veg_str)
    except BroadVegetationType.DoesNotExist:
        logger.warning('Broad Vegetation Type "{0}" on line {1} not known'.format(veg_str, entry.row))
        return None


def get_australian_soil_classification(entry):
    classifcation_str = entry.australian_soil_classification
    if classifcation_str == '':
        return None
    try:
        return AustralianSoilClassification.objects.get(classification__iexact=classifcation_str)
    except AustralianSoilClassification.DoesNotExist:
        logger.warning(
            'Australian Soil Type classification "{0}" on line {1} not known'.format(classifcation_str, entry.row))
        return None


def get_fao_soil_classification(entry):
    classifcation_str = entry.fao
    if classifcation_str == '':
        return None
    try:
        return FAOSoilClassification.objects.get(classification__iexact=classifcation_str)
    except FAOSoilClassification.DoesNotExist:
        logger.warning('FAO Soil Type classification "{0}" on line {1} not known'.format(classifcation_str, entry.row))
        return None


def get_profile_position(entry):
    profile_str = entry.profile_position
    if profile_str == '':
        return None
    try:
        return ProfilePosition.objects.get(position__iexact=profile_str)
    except ProfilePosition.DoesNotExist:
        logger.warning('Profile Position "{0}" on line {1} not known'.format(profile_str, entry.row))
        return None


def get_soil_colour(entry):
    colour_str = entry.soil_colour
    if colour_str == '':
        return None
    try:
        return SoilColour.objects.get(code=colour_str)
    except SoilColour.DoesNotExist:
        logger.warning('Soil Colour "{0}" on line {1} not known'.format(colour_str, entry.row))
        return None


def get_site(entry):
    """
    Add or get a site
    """

    # only make a site once, the first entry wins
    if entry.lat is None or entry.lon is None:
        logger.warning('Site lat/lon empty, not creating site {0}'.format(entry.description))
        return None

    site, created = CollectionSite.objects.get_or_create(lat=-1 * entry.lat, lon=entry.lon)
    # the first set of site data wins
    # if created:

    site.elevation = entry.elevation
    site.date_sampled = entry.date_sampled
    site.location_name = entry.description
    site.note = entry.note + '\n' + entry.other_comments
    site.debug_note = ingest_utils.pretty_print_namedtuple(entry)

    site.vegetation_type_descriptive = entry.vegetation_type_descriptive
    site.vegetation_total_cover = entry.vegetation_total_cover
    site.vegetation_dominant_trees = entry.vegetation_dominant_trees

    site.slope = entry.slope
    site.slope_aspect = entry.slope_aspect

    # controlled vocabularies
    site.current_land_use = get_landuse(entry)
    site.general_ecological_zone = get_general_ecological_zone(entry)
    site.vegetation_type = get_vegetation_type(entry)
    site.soil_type_australian_classification = get_australian_soil_classification(entry)
    site.soil_type_fao_classification = get_fao_soil_classification(entry)

    site.profile_position = get_profile_position(entry)

    site.fire_history = entry.fire_history
    site.fire_intensity = entry.fire_intensity
    site.save()

    return site


def add_samples(data):
    """
    Add samples. There is a sample per line for the source document
    """
    for e in data:
        bpa_id = get_bpa_id(e)
        if bpa_id is None:
            continue

        sample, created = CollectionSample.objects.get_or_create(bpa_id=bpa_id)
        # always update, if the sample id is repeated more than once in the document, the last one wins
        sample.bpa_id = bpa_id
        sample.site = get_site(e)
        sample.upper_depth = e.upper_depth
        sample.lower_depth = e.lower_depth

        # horizons
        horizons = get_horizon_classifications(e.horizon_classification)
        sample.horizon_classification1 = horizons[0]
        sample.horizon_classification2 = horizons[1]

        sample.debug_note = ingest_utils.pretty_print_namedtuple(e)
        sample.save()


def add_chemical_analysis(data):
    """
    Add the chemical analysis
    """

    for e in data:
        bpa_id = get_bpa_id(e)
        if bpa_id is None:
            continue

        analysis, created = ChemicalAnalysis.objects.get_or_create(bpa_id=bpa_id)
        analysis.depth = e.upper_depth
        analysis.moisture = e.soil_moisture
        analysis.colour = get_soil_colour(e)
        analysis.gravel = e.gravel
        analysis.texture = e.texture
        analysis.course_sand = e.course_sand
        analysis.fine_sand = e.fine_sand
        analysis.sand = e.sand
        analysis.silt = e.silt
        analysis.clay = e.clay

        analysis.save()


def run(file_name=DEFAULT_SPREADSHEET_FILE):
    """
    Pass parameters like below:
    vpython-bpam manage.py runscript ingest_base_454 --script-args Melanoma_study_metadata.xlsx
    """

    data = list(get_data(file_name))
    add_samples(data)
    add_chemical_analysis(data)




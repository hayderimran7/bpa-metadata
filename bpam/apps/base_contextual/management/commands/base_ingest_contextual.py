# -*- coding: utf-8 -*-

import re

from unipath import Path
from libs.fetch_data import Fetcher, get_password
from libs.excel_wrapper import ExcelWrapper
from libs import bpa_id_utils
from libs import ingest_utils
from libs import logger_utils
from libs import management_command
from apps.base_contextual.models import (HorizonClassification, LandUse, GeneralEcologicalZone, BroadVegetationType,
                                         AustralianSoilClassification, FAOSoilClassification, ProfilePosition,
                                         SoilColour, TillageType, CollectionSite, SampleContext, ChemicalAnalysis)

logger = logger_utils.get_logger(__name__)

METADATA_PATH = 'base/metadata/contextual/2017-06-21/'
CONTEXTUAL_DATA_FILE = 'contextual-2017-06-21.xlsx'
DATA_DIR = Path(ingest_utils.METADATA_ROOT, METADATA_PATH)

BPA_ID_PREFIX = "102.100.100"
BASE_DESCRIPTION = 'BASE'
CHEM_MIN_SENTINAL_VALUE = 0.0001


def get_bpa_id(e):
    """
    Get or make BPA ID
    """
    bpa_id, report = bpa_id_utils.get_bpa_id(e.sample_id, 'BASE', 'BASE')
    if not bpa_id:
        logger.warning('Ignoring {0}, not a good BPA ID'.format(e.sample_id))
        return None
    return bpa_id


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


def get_float_or_sentinal(val):
    # if its a float, its probably ok
    if isinstance(val, float):
        return val

    # keep no data no data
    if val == '':
        return None

    # substitute the sentinal value for below threshold values
    if isinstance(val, basestring) and (val.find('<') != -1):
        return CHEM_MIN_SENTINAL_VALUE


def get_data(file_name):
    """
    The data sets is relatively small, so make a in-memory copy to simplify some operations.
    """

    field_spec = [('sample_id', 'Sample_ID', ingest_utils.extract_bpa_id),
                  ('date_sampled', 'Date sampled', ingest_utils.get_date),
                  ('lat', 'latitude', ingest_utils.get_clean_float),
                  ('lon', 'longitude', ingest_utils.get_clean_float),
                  ('depth', 'Depth', None),
                  ('horizon_classification', 'Horizon', None),
                  ('storage_method', 'soil sample storage method', None),
                  ('description', 'location description', None),
                  ('broad_land_use', 'broad land use', None),
                  ('current_land_use', 'Detailed land use', None),
                  ('general_ecological_zone', 'General Ecological Zone', None),
                  ('vegetation_type_controlled_vocab', 'Vegetation Type', None),
                  ('vegetation_total_cover', 'Vegetation Total cover (%)', None),
                  ('vegetation_dominant_trees', 'Vegetation Dom. Trees (%)', None),
                  ('elevation', 'Elevation ()', ingest_utils.get_clean_number),
                  ('slope', 'Slope (%)', None),
                  ('slope_aspect', re.compile(r'^slope aspect .*'), None),
                  ('profile_position', 'Profile Position controlled vocab (5)', None),
                  ('australian_soil_classification', 'Australian Soil Classification controlled vocab (6)', None),
                  ('fao', 'FAO soil classification controlled vocab (7)', None),
                  # historic data
                  ('immediate_previous_land_use', 'Immediate Previous Land Use controlled vocab (2)', None),
                  ('date_since_change_in_land_use', 'Date since change in Land Use', None),
                  ('crop_rotation_1', 'Crop rotation 1yr since present', None),
                  ('crop_rotation_2', 'Crop rotation 2yrs since present', None),
                  ('crop_rotation_3', 'Crop rotation 3yrs since present', None),
                  ('crop_rotation_4', 'Crop rotation 4yrs since present', None),
                  ('crop_rotation_5', 'Crop rotation 5yrs since present', None),
                  ('agrochemical_additions', 'Agrochemical Additions', None),
                  ('tillage', 'Tillage controlled vocab (9)', None),
                  ('fire_history', 'Fire', None),
                  ('fire_intensity', 'fire intensity if known', None),
                  ('flooding', 'Flooding', None),
                  ('extreme_event', 'Extreme Events', None),
                  # soil structual
                  ('soil_moisture', 'Soil moisture (%)', ingest_utils.get_clean_float),
                  ('soil_colour', 'Color controlled vocab (10)', None),
                  ('gravel', 'gravel (%)- ( >2.0 mm)'),
                  ('texture', 'Texture ()', ingest_utils.get_clean_float),
                  ('course_sand', re.compile(r'^course sand .*'), ingest_utils.get_clean_float),
                  ('fine_sand', re.compile(r'^fine sand .*'), ingest_utils.get_clean_float),
                  ('sand', 'Sand (%)', ingest_utils.get_clean_float),
                  ('silt', re.compile(r'^silt .*'), ingest_utils.get_clean_float),
                  ('clay', re.compile(r'^clay .*'), ingest_utils.get_clean_float),
                  # soil chemical
                  ('ammonium_nitrogen', 'Ammonium Nitrogen (mg/Kg)', get_float_or_sentinal),
                  ('nitrate_nitrogen', 'Nitrate Nitrogen (mg/Kg)', get_float_or_sentinal),
                  ('phosphorus_collwell', 'Phosphorus Colwell (mg/Kg)', get_float_or_sentinal),
                  ('potassium_collwell', 'Potassium Colwell (mg/Kg)', get_float_or_sentinal),
                  ('sulphur', 'Sulphur (mg/Kg)', get_float_or_sentinal),
                  ('organic_carbon', 'Organic Carbon (%)', get_float_or_sentinal),
                  ('conductivity', 'Conductivity (dS/m)', get_float_or_sentinal),
                  ('cacl2_ph', 'pH Level (CaCl2) (pH)', get_float_or_sentinal),
                  ('h20_ph', 'pH Level (H2O) (pH)', get_float_or_sentinal),
                  ('dtpa_copper', 'DTPA Copper (mg/Kg)', get_float_or_sentinal),
                  ('dtpa_iron', 'DTPA Iron (mg/Kg)', get_float_or_sentinal),
                  ('dtpa_manganese', 'DTPA Manganese (mg/Kg)', get_float_or_sentinal),
                  ('dtpa_zinc', 'DTPA Zinc (mg/Kg)', get_float_or_sentinal),
                  ('exc_aluminium', 'Exc. Aluminium (meq/100g)', get_float_or_sentinal),
                  ('exc_calcium', 'Exc. Calcium (meq/100g)', get_float_or_sentinal),
                  ('exc_magnesium', 'Exc. Magnesium (meq/100g)', get_float_or_sentinal),
                  ('exc_potassium', 'Exc. Potassium (meq/100g)', get_float_or_sentinal),
                  ('exc_sodium', 'Exc. Sodium (meq/100g)', get_float_or_sentinal),
                  ('boron_hot_cacl2', 'Boron Hot CaCl2 (mg/Kg)', get_float_or_sentinal), ]

    wrapper = ExcelWrapper(field_spec, file_name, sheet_name=None, header_length=1, column_name_row_index=0)

    return wrapper.get_all()


def get_land_use(land_use_str):
    """
    Translate the land use string to a the landuse controlled vocabulary
    """
    if land_use_str in ('', 'None'):
        return None
    try:
        return LandUse.objects.get(description__iexact=land_use_str)
    except LandUse.DoesNotExist:
        logger.warning('Land Use description "{0}" not known'.format(land_use_str))
        return None


def get_general_ecological_zone(entry):
    zone_str = entry.general_ecological_zone
    if zone_str == '':
        return None

    try:
        return GeneralEcologicalZone.objects.get(description__iexact=zone_str)
    except GeneralEcologicalZone.DoesNotExist:
        logger.warning('General Ecological Zone "{0}" not known'.format(zone_str))
        return None


def get_vegetation_type(entry):
    veg_str = entry.vegetation_type_controlled_vocab
    if veg_str in ('', 'None'):
        return None

    try:
        return BroadVegetationType.objects.get(vegetation__iexact=veg_str)
    except BroadVegetationType.DoesNotExist:
        logger.warning('Broad Vegetation Type "{0}" not known'.format(veg_str))
        return None


def get_australian_soil_classification(entry):
    classification_str = entry.australian_soil_classification
    if classification_str == '':
        return None
    try:
        return AustralianSoilClassification.objects.get(classification__iexact=classification_str)
    except AustralianSoilClassification.DoesNotExist:
        logger.warning('Australian Soil Type classification "{0}" not known'.format(classification_str))
        return None


def get_fao_soil_classification(entry):
    classification_str = entry.fao
    if classification_str == '':
        return None
    try:
        return FAOSoilClassification.objects.get(classification__iexact=classification_str)
    except FAOSoilClassification.DoesNotExist:
        logger.warning('FAO Soil Type classification "{0}" not known'.format(classification_str))
        return None


def get_profile_position(entry):
    profile_str = entry.profile_position
    if profile_str in ('', 'No data'):
        return None
    try:
        return ProfilePosition.objects.get(position__iexact=profile_str)
    except ProfilePosition.DoesNotExist:
        logger.warning('Profile Position "{0}" not known'.format(profile_str))
        return None


def get_soil_colour(entry):
    colour_str = entry.soil_colour
    if colour_str == '':
        return None
    try:
        return SoilColour.objects.get(code=colour_str)
    except SoilColour.DoesNotExist:
        logger.warning('Soil Colour "{0}" not known'.format(colour_str))
        return None


def get_tillage(entry):
    tillage_str = entry.tillage
    if tillage_str == '':
        return None
    try:
        return TillageType.objects.get(tillage__iexact=tillage_str)
    except TillageType.DoesNotExist:
        logger.warning('Tillage Type "{0}" not known'.format(tillage_str))
        return None


def get_site(entry):
    """
    Add or get a site
    """

    # only make a site once, the first entry wins
    if entry.lat is None or entry.lon is None:
        logger.warning('Site lat/lon empty, not creating site {0}'.format(entry.description))
        return None

    site, created = CollectionSite.objects.get_or_create(lat=entry.lat, lon=entry.lon)
    # the first set of site data wins
    if created:
        site.elevation = entry.elevation
        site.date_sampled = entry.date_sampled
        site.location_name = entry.description

        site.vegetation_total_cover = entry.vegetation_total_cover
        site.vegetation_dominant_trees = entry.vegetation_dominant_trees

        site.slope = entry.slope
        site.slope_aspect = entry.slope_aspect

        # controlled vocabularies
        site.current_land_use = get_land_use(entry.current_land_use)
        site.broad_land_use = get_land_use(entry.broad_land_use)
        site.general_ecological_zone = get_general_ecological_zone(entry)
        site.vegetation_type = get_vegetation_type(entry)
        site.soil_type_australian_classification = get_australian_soil_classification(entry)
        site.soil_type_fao_classification = get_fao_soil_classification(entry)

        site.profile_position = get_profile_position(entry)

        # history
        site.immediate_previous_land_use = get_land_use(entry.immediate_previous_land_use)
        site.date_since_change_in_land_use = entry.date_since_change_in_land_use
        site.crop_rotation_1 = entry.crop_rotation_1
        site.crop_rotation_2 = entry.crop_rotation_2
        site.crop_rotation_3 = entry.crop_rotation_3
        site.crop_rotation_4 = entry.crop_rotation_4
        site.crop_rotation_5 = entry.crop_rotation_5
        site.agrochemical_additions = entry.agrochemical_additions
        site.tillage = get_tillage(entry)
        site.fire_history = entry.fire_history
        site.fire_intensity = entry.fire_intensity
        site.flooding = entry.flooding
        site.environment_event = entry.extreme_event

        # notes
        site.debug_note = ingest_utils.pretty_print_namedtuple(entry)
        site.other_comments = None  # entry.other_comments

        site.save()

    return site


def get_chemical_analysis(e, bpa_id):
    """
    Add the chemical analysis
    """

    analysis, created = ChemicalAnalysis.objects.get_or_create(bpa_id=bpa_id)
    # structure
    analysis.depth = e.depth
    analysis.moisture = e.soil_moisture
    analysis.colour = get_soil_colour(e)
    analysis.gravel = e.gravel
    analysis.texture = e.texture
    analysis.course_sand = e.course_sand
    analysis.fine_sand = e.fine_sand
    analysis.sand = e.sand
    analysis.silt = e.silt
    analysis.clay = e.clay
    # soil chemical
    analysis.ammonium_nitrogen = e.ammonium_nitrogen
    analysis.nitrate_nitrogen = e.nitrate_nitrogen
    analysis.phosphorus_colwell = e.phosphorus_collwell
    analysis.potassium_colwell = e.potassium_collwell
    analysis.sulphur = e.sulphur
    analysis.organic_carbon = e.organic_carbon
    analysis.conductivity = e.conductivity
    analysis.cacl2_ph = e.cacl2_ph
    analysis.h20_ph = e.h20_ph
    analysis.dtpa_copper = e.dtpa_copper
    analysis.dtpa_iron = e.dtpa_iron
    analysis.dtpa_manganese = e.dtpa_manganese
    analysis.dtpa_zinc = e.dtpa_zinc
    analysis.exc_aluminium = e.exc_aluminium
    analysis.exc_calcium = e.exc_calcium
    analysis.exc_magnesium = e.exc_magnesium
    analysis.exc_potassium = e.exc_potassium
    analysis.exc_sodium = e.exc_sodium
    analysis.boron_hot_cacl2 = e.boron_hot_cacl2
    analysis.total_nitrogen = None  # e.total_nitrogen
    analysis.total_carbon = None  # e.total_carbon

    analysis.save()
    return analysis


def add_samples(data):
    """
    Add samples. There is a sample per line for the source document
    """
    for e in data:
        bpa_id = get_bpa_id(e)
        if bpa_id is None:
            continue

        sample, created = SampleContext.objects.get_or_create(bpa_id=bpa_id)
        # always update, if the sample id is repeated more than once in the document, the last one wins
        sample.bpa_id = bpa_id
        sample.site = get_site(e)
        sample.analysis = get_chemical_analysis(e, bpa_id)
        sample.depth = e.depth

        # horizons
        horizons = get_horizon_classifications(e.horizon_classification)
        sample.horizon_classification1 = horizons[0]
        sample.horizon_classification2 = horizons[1]
        sample.storage = e.storage_method
        sample.debug_note = ingest_utils.pretty_print_namedtuple(e)
        sample.methodological_notes = None  # e.methodological_notes
        sample.save()


def do_metadata():
    def is_metadata(path):
        if path.isfile() and path.ext == '.xlsx':
            return True

    logger.info('Ingesting BASE Contextual Data from {0}'.format(DATA_DIR))
    for metadata_file in DATA_DIR.walk(filter=is_metadata):
        logger.info('Processing BASE Contextual Data file {0}'.format(metadata_file))
        samples = list(get_data(metadata_file))
        add_samples(samples)


def truncate():
    from django.db import connection

    cursor = connection.cursor()
    cursor.execute('TRUNCATE TABLE "{0}" CASCADE'.format(CollectionSite._meta.db_table))
    cursor.execute('TRUNCATE TABLE "{0}" CASCADE'.format(SampleContext._meta.db_table))
    cursor.execute('TRUNCATE TABLE "{0}" CASCADE'.format(ChemicalAnalysis._meta.db_table))


class Command(management_command.BPACommand):
    help = 'Ingest BASE Contextual Data'

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument('--delete',
                            action='store_true',
                            dest='delete',
                            default=False,
                            help='Delete all contextual data', )

    def handle(self, *args, **options):

        if options['delete']:
            logger.info("Truncating Contextual data")
            truncate()

        fetcher = Fetcher(DATA_DIR, self.get_base_url(options) + METADATA_PATH, auth=('base', get_password('base')))
        fetcher.clean()
        fetcher.fetch(CONTEXTUAL_DATA_FILE)

        truncate()
        do_metadata()

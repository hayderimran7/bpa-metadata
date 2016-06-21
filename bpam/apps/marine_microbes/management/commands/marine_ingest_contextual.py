# -*- coding: utf-8 -*-

from unipath import Path
from libs import bpa_id_utils
from libs import ingest_utils
from libs import management_command
from libs.excel_wrapper import ExcelWrapper
from libs.fetch_data import Fetcher

from apps.common.models import Site
from ...models import MMSample

from libs.logger_utils import get_logger
logger = get_logger(__name__)

BPA_ID = "102.100.100"
PROJECT_ID = "marine_microbes"
PROJECT_DESCRIPTION = "Marine Microbes"

MM_CONTEXTUAL = "MM_Contextual.xlsx"
METADATA_PATH = "marine_microbes/metadata"
DATA_DIR = Path(ingest_utils.METADATA_ROOT, METADATA_PATH)


def add_pelagic_data(data):
    """ pack data into the DB """

    for entry in data:
        if entry.bpa_id is "":
            continue
        bpa_id, report = bpa_id_utils.get_bpa_id(entry.bpa_id, PROJECT_ID, PROJECT_DESCRIPTION, add_prefix=True)
        if not bpa_id:
            logger.info("Non BPA encountered when I expected one {}, skipping".format(report))
            continue

        sample, _ = MMSample.objects.get_or_create(bpa_id=bpa_id)
        # just fill in everything available from this spreadsheet
        if sample:
            sample.sample_type = MMSample.PELAGIC
            sample.site = Site.get_or_create(entry.lat, entry.lon, entry.site_description)
            sample.depth = entry.depth

            sample.save()


def ingest_data():
    def is_metadata(path):
        if path.isfile() and path.ext == ".xlsx":
            return True

    logger.info("Ingesting Sepsis BPA Contextual metadata from {0}".format(DATA_DIR))
    for metadata_file in DATA_DIR.walk(filter=is_metadata):
        logger.info("Processing Sepsis BPA Contextual file {0}".format(metadata_file))
        add_pelagic_data(list(get_pelagic_data(metadata_file)))


def get_pelagic_data(file_name):
    """ Parse fields from the metadata spreadsheet pelagic sheet"""

    # {{{
    # BPA_ID
    # Date sampled (Y-M-D)
    # Time sampled (hh:mm)
    # lat (decimal degrees)
    # long (decimal degrees)
    # Depth (m)
    # Notes
    # Location description
    # pH Level (H2O) (pH)
    # Oxygen (ml/L)
    # CTD Silicate (μmol/L)
    # Nitrate/Nitrite (μmol/L)
    # Phosphate (μmol/L)
    # Ammonium (μmol/L)
    # Total CO2 (μmol/kg)
    # Total alkalinity (μmol/kg)
    # Temperature [ITS-90, deg C]
    # Conductivity [S/m] Fluorescence, Wetlab
    # ECO-AFL/FL [mg/m^3]
    # Turbidity (Upoly 0, WET Labs FLNTURT)
    # Density [density, Kg/m^3]
    # Salinity [PSU] CTD
    # TSS [mg/L]
    # Inorganic Fraction [mg/L]
    # Organic Fraction [mg/L]
    # Secchi Depth (m)
    # Biomass (mg/m3)
    # ALLO [mg/m3]
    # ALPHA_BETA_CAR [mg/m3]
    # ANTH [mg/m3]
    # ASTA [mg/m3]
    # BETA_BETA_CAR [mg/m3]
    # BETA_EPI_CAR [mg/m3]
    # BUT_FUCO [mg/m3]
    # CANTHA [mg/m3]
    # CPHL_A [mg/m3]
    # CPHL_B [mg/m3]
    # CPHL_C1C2 [mg/m3]
    # CPHL_C1 [mg/m3]
    # CPHL_C2 [mg/m3]
    # CPHL_C3 [mg/m3]
    # CPHLIDE_A [mg/m3]
    # DIADCHR [mg/m3]
    # DIADINO [mg/m3]
    # DIATO [mg/m3]
    # DINO [mg/m3]
    # DV_CPHL_A_and_CPHL_A [mg/m3]
    # DV_CPHL_A [mg/m3]
    # DV_CPHL_B_and_CPHL_B [mg/m3]
    # DV_CPHL_B [mg/m3]
    # ECHIN [mg/m3] FUCO [mg/m3]
    # GYRO [mg/m3]
    # HEX_FUCO [mg/m3]
    # KETO_HEX_FUCO [mg/m3]
    # LUT [mg/m3]
    # LYCO [mg/m3]
    # MG_DVP [mg/m3]
    # NEO [mg/m3]
    # PERID [mg/m3]
    # PHIDE_A [mg/m3]
    # PHYTIN_A [mg/m3]
    # PHYTIN_B [mg/m3]
    # PRAS [mg/m3]
    # PYROPHIDE_A [mg/m3]
    # PYROPHYTIN_A [mg/m3]
    # VIOLA [mg/m3]
    # ZEA [mg/m3]
    # }}}

    field_spec = [
        ("bpa_id", "BPA_ID", lambda s: str(int(s))),
        ("date_sampled", "Date sampled (Y-M-D)", ingest_utils.get_date),
        ("time_sampled", "Time sampled (hh:mm)", None),
        ("lat", "lat (decimal degrees)", None),
        ("lon", "long (decimal degrees)", None),
        ("depth", "Depth (m)", None),
        ("notes", "Notes", None),
        ("site_description", "Location description", None),
    ]

    wrapper = ExcelWrapper(field_spec,
                           file_name,
                           sheet_name="Pelagic",
                           header_length=1,
                           column_name_row_index=0,
                           formatting_info=True)

    return wrapper.get_all()


class Command(management_command.BPACommand):
    help = 'Ingest Marine Microbes Contextual Data'

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument('--delete',
                            action='store_true',
                            dest='delete',
                            default=False,
                            help='Delete all contextual data', )

    def handle(self, *args, **options):

        if options['delete']:
            self.log_info("Deleting all Hosts")
            MMSample.objects.all().delete()

        fetcher = Fetcher(DATA_DIR, self.get_base_url(options) + METADATA_PATH)
        fetcher.clean()
        fetcher.fetch(MM_CONTEXTUAL)
        ingest_data()

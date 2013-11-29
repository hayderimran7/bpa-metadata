import sys
import pprint
from datetime import datetime
import logging

import xlrd
from unipath import Path

from apps.common.models import DNASource, Facility, BPAUniqueID, Sequencer

from apps.BASE.models import GPSPosition, CollectionSite, SoilSample, ChemicalAnalysis, BPAUniqueID

import utils
import user_helper


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('BASE 454')


DATA_DIR = Path(Path(__file__).ancestor(3), "data/base/")
DEFAULT_SPREADSHEET_FILE = Path(DATA_DIR, '454')

BPA_ID = "102.100.100"
BASE_DESCRIPTION = 'BASE'


def get_data(spreadsheet_file):
    """
    The data sets is relatively small, so make a in-memory copy to simplify some operations.
    """

    fieldnames = ['bpa_id',
                  'sample_id',
                  'aurora_purified',
                  'dna_storage_nunc_plate',
                  'dna_storage_nunc_tube',
                  'dna_storage_nunc_well_location',
                  'agrf_batch_number',
                  'submitter_name',
                  'date_received',
                  # Adelaide extraction
                  'adelaide_extraction_sample_weight',  # mg
                  'adelaide_fluorimetry',  # ng/uL gDNA'
                  'adelaide_pcr_inhibition',
                  'adelaide_pcr1',
                  'adelaide_pcr2',
                  'adelaide_shipped_to_agrf_454',
                  'adelaide_shipped_to_agrf_miseq',
                  'adelaid_shipped_to_ramacciotitti',
                  # Brisbane 454
                  'brisbane_16s_mid',
                  'brisbane_its_mid',
                  'brisbane_16s_pcr1',
                  'brisbane_16s_pcr2',
                  'brisbane_16s_pcr3',
                  'brisbane_its_pcr1_neat',
                  'brisbane_its_pcr2_1_10',
                  'brisbane_its_pcr3_fusion',
                  'brisbane_fluorimetry_16s',  # ng/uL 16S
                  'brisbane_fluorimetry_its',  # ng/uL 16S
                  'brisbane_16s_qpcr',
                  'brisbane_its_qpcr',
                  'brisbane_i6s_pooled',
                  'brisbane_its_pooled',
                  'brisbane_16s_reads',
                  'brisbane_itss_reads',
                  'note',
                  ]

    wb = xlrd.open_workbook(spreadsheet_file)
    sheet = wb.sheet_by_name('Sheet1')
    samples = []
    for row_idx in range(sheet.nrows)[2:]:  # the first two lines are headers
        vals = sheet.row_values(row_idx)

        if not utils.is_bpa_id(vals[0]):
            logger.warning('BPA ID {0} does not look like a real ID, ignoring'.format(vals[0]))
            continue

        # for date types try to convert to python dates
        types = sheet.row_types(row_idx)
        for i, t in enumerate(types):
            if t == xlrd.XL_CELL_DATE:
                vals[i] = datetime(*xlrd.xldate_as_tuple(vals[i], wb.datemode))

        samples.append(dict(zip(fieldnames, vals)))

    return samples


def run(spreadsheet_file=DEFAULT_SPREADSHEET_FILE):
    """
    Pass parameters like below:
    vpython-bpam manage.py runscript ingest_base_454 --script-args Melanoma_study_metadata.xlsx
    """

    data = get_data(spreadsheet_file)


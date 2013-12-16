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
import row_tools

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

    fieldnames = [('bpa_id', 'Unique ID', None),
                  ('sample_id', 'Sample ID', None),
                  ('aurora_purified', 'Aurora purified', None),
                  ('dna_storage_nunc_plate', 'DNA Storage Nunc Plate', None),
                  ('dna_storage_nunc_tube', 'DNA Storage Nunc Tube', None),
                  ('dna_storage_nunc_well_location', 'DNA Storage Well Location', None),
                  ('agrf_batch_number', 'AGRF Batch number', None),
                  ('submitter_name', 'Submitter Name', None),
                  ('date_received', 'Date received', None),
                  # Adelaide extraction
                  ('adelaide_extraction_sample_weight', 'Extraction Sample Weight (mg)', None),  # mg
                  ('adelaide_fluorimetry', 'Fluorimetry ng/uL gDNA', None),  # ng/uL gDNA'
                  ('adelaide_pcr_inhibition', 'PCR Inhibition (neat plus spike) 16S (V3-V8) p=pass, f=fail, NP = not performed', None),
                  ('adelaide_pcr1', 'PCR1 (neat) 16S (V3-V8) p=pass, f-fail  NP = not performed', None),
                  ('adelaide_pcr2', 'PCR2 (1:100) 16S (V3-V8) p=pass, f=fail   NP = not performed', None),
                  ('adelaide_date_shipped_to_agrf_454', 'DNA shipped to AGRF (454)', None),
                  ('adelaide_date_shipped_to_agrf_miseq', 'DNA shipped to AGRF (MiSeq)', None),
                  ('adelaide_date_shipped_to_ramacciotitti', 'DNA shipped to Ramaciotti', None),
                  # Brisbane 454
                  ('brisbane_16s_mid', '16S MID', None),
                  ('brisbane_its_mid', 'ITS MID', None),
                  ('brisbane_16s_pcr1', '16S (V1-V3) PCR1 (neat) p=pass, f=fail', None),
                  ('brisbane_16s_pcr2', '16S (V1-V3) PCR2 (1:10) p=pass, f=fail', None),
                  ('brisbane_16s_pcr3', '16S (V1-V3) PCR3 (fusion-primer) p=pass, f=fail', None),
                  ('brisbane_its_pcr1_neat', 'ITS PCR1 (neat) p=pass, f=fail', None),
                  ('brisbane_its_pcr2_1_10', 'ITS PCR1 (1:10) p=pass, f=fail', None),
                  ('brisbane_its_pcr3_fusion', 'ITS PCR3 (fusion-primer) p=pass, f=fail', None),
                  ('brisbane_fluorimetry_16s', 'Fluorimetry ng/uL 16S', None),  # ng/uL 16S
                  ('brisbane_fluorimetry_its', 'Fluorimetry ng/uL ITS', None),  # ng/uL 16S
                  ('brisbane_16s_qpcr', '16S qPCR', None),
                  ('brisbane_its_qpcr', 'ITS qPCR', None),
                  ('brisbane_i6s_pooled', '16S pooled y=yes, n=no', None),
                  ('brisbane_its_pooled', 'ITS pooled y=yes, n=no', None),
                  ('brisbane_16s_reads', '16S >3000 reads - Trim Back 150bp', None),
                  ('brisbane_itss_reads', 'ITS >3000 reads - Trim Back 150bp Run1', None),
                  ('note', 'Sample comments', None),
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


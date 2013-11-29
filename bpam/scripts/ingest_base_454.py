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
                  'extraction_sample_weight',  # mg
                  'fluorimetry',  # ng/uL gDNA'
                  'pcr_inhibition',
                  'pcr1',
                  'pcr2',
                  'shipped_to_agrf_454',
                  'shipped_to_agrf_miseq',
                  'shipped_to_ramacciotitti',
                  # Brisbane 454
                  '16s_mid',
                  'its_mid',
                  'pcr1',
                  'pcr2',
                  'pcr3',
                  'its_pcr1',
                  'its_pcr2',
                  'its_pcr3'


                  'sample_name',
                  'dna_concentration',
                  'total_dna',
                  'collection_site',
                  'collection_date',
                  'collector_name',
                  'gps_location',
                  'water_temp',
                  'ph',
                  'depth',
                  'collection_comment',
                  'other',
                  'requested_sequence_coverage',
                  'sequencing_notes',
                  'contact_scientist',
                  'contact_affiliation',
                  'contact_email',
                  'sample_dna_source',
                  'dna_extraction_protocol',
                  'dna_rna_concentration',
                  'total_dna_rna_shipped',
                  'sequencing_facility',
                  'date_received',
                  'comments_by_facility',
                  'sequencing_data_eta',
                  'date_sequenced',
                  'library',
                  'library_construction',
                  'requested_read_length',
                  'library_construction_protocol',
                  'index_number',
                  'sequencer',
                  'run_number',
                  'flow_cell_id',
                  'lane_number',
                  'sequence_filename',
                  'sequence_filetype',
                  'md5_checksum',
                  'contact_bioinformatician_name',
                  'contact_bioinformatician_email',
                  'date_data_sent',
                  'date_data_received',
    ]

    wb = xlrd.open_workbook(spreadsheet_file)
    sheet = wb.sheet_by_name('DNA library Sequencing - Pilot')
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



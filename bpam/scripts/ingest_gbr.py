import sys
import pprint
import csv
import xlrd
from datetime import datetime
from unipath import Path

from apps.bpaauth.models import BPAUser
from apps.common.models import *
from apps.gbr.models import *
from .utils import *

DATA_DIR = Path(Path(__file__).ancestor(3), "data/gbr/")
MELANOMA_SPREADSHEET_FILE = Path(DATA_DIR, 'BPA_ReFuGe2020_METADATA.xlsx')

BPA_ID = "102.100.100"

def get_dna_source(description):
    """
    Get a DNA source if it exists, if it doesn't make it.
    """

    description = description.capitalize()
    try:
        source = DNASource.objects.get(description=description)
    except DNASource.DoesNotExist:
        source = DNASource(description=description)
        source.save()

    return source


def get_tumor_stage(description):
    """
    Get the tumor stage if it exists, else make it.
    """

    description = description.capitalize()
    if description == "":
        description = "Not applicable"

    try:
        stage = TumorStage.objects.get(description=description)
    except TumorStage.DoesNotExist:
        stage = TumorStage(description=description)
        stage.save()

    return stage


def ingest_samples(samples):
    def get_facility(name, service):
        if name == '':
            name = "Unknown"
        if service == '':
            service = "Unknown"

        try:
            facility = Facility.objects.get(name=name, service=service)
        except Facility.DoesNotExist:
            facility = Facility(name=name, service=service)
            facility.save()

        return facility

    def get_protocol(e):
        def get_library_type(str):
            """
            (('PE', 'Paired End'), ('SE', 'Single End'), ('MP', 'Mate Pair'))
            """
            new_str = str.lower()
            if new_str.find('pair') >= 0:
                return 'PE'
            if new_str.find('single') >= 0:
                return 'SE'
            if new_str.find('mate') >= 0:
                return 'MP'
            return 'UN'

        base_pairs = get_clean_number(e['library_construction'])
        library_type = get_library_type(e['library'])
        library_construction_protocol = e['library_construction_protocol'].replace(',', '').capitalize()

        try:
            protocol = Protocol.objects.get(base_pairs=base_pairs, library_type=library_type,
                                            library_construction_protocol=library_construction_protocol)
        except Protocol.DoesNotExist:
            protocol = Protocol(base_pairs=base_pairs, library_type=library_type,
                                library_construction_protocol=library_construction_protocol)
            protocol.save()

        return protocol

    def get_gender(gender):
        if gender == "":
            gender = "U"
        return gender

    def add_sample(e):
        bpa_id = e['bpa_id']
        try:
            # Test if sample already exists
            # First come fist serve
            MelanomaSample.objects.get(bpa_id__bpa_id=bpa_id)
        except MelanomaSample.DoesNotExist:
            sample = MelanomaSample()
            sample.bpa_id = BPAUniqueID.objects.get(bpa_id=bpa_id)
            sample.name = e['sample_name']
            sample.requested_sequence_coverage = e['requested_sequence_coverage'].upper()
            sample.organism = Organism.objects.get(genus="Homo", species="Sapiens")
            sample.dna_source = get_dna_source(e['sample_dna_source'])
            sample.dna_extraction_protocol = e['dna_extraction_protocol']
            sample.tumor_stage = get_tumor_stage(e['sample_tumor_stage'])
            sample.gender = get_gender(e['sample_gender'])
            sample.histological_subtype = e['histological_subtype']
            sample.passage_number = get_clean_number(e['passage_number'])

            # facilities
            sample.array_analysis_facility = get_facility(e['array_analysis_facility'], 'Array Analysis')
            sample.whole_genome_sequencing_facility = get_facility(e['whole_genome_sequencing_facility'],
                                                                   'Whole Genome Sequencing')
            sample.sequencing_facility = get_facility(e['sequencing_facility'], 'Sequencing')

            sample.protocol = get_protocol(e)

            sample.note = INGEST_NOTE + pprint.pformat(e)
            sample.save()
            print("Ingested Melanoma sample {0}".format(sample.name))

    for sample in samples:
        add_sample(sample)


def ingest_arrays(arrays):
    """ Melanoma Arrays"""

    def get_gender(str):
        str = str.strip().lower()
        if str == "male":
            return 'M'
        if str == "female":
            return 'F'
        return 'U'

    for e in arrays:
        array = Array()
        array.batch_number = int(e['batch_no'])
        array.bpa_id = get_bpa_id(e['bpa_id'],
                                  project_name="Melanoma",
                                  note=u"Created during array ingestion on {0}".format(date.today()))
        array.mia_id = e['mia_id']
        array.array_id = e['array_id']
        array.call_rate = float(e['call_rate'])
        array.gender = get_gender(e['gender'])
        array.well_id = e['well_id']
        array.save()


def get_gbr_sample_data():
    """
    The data sets is relatively small, so make a in-memory copy to simplify some operations.
    """

    def filter_out_sample(sample):
        """
        Filter out a sample for whatever reason
        """
        # the csv file is a straight csv dump of the google doc
        if sample['bpa_id'].find(BPA_ID) == -1:
            print sample
            return True

        return False

Unique ID
Species
Dataset
Sample Description
DNA conc (ng/ul)
Total DNA (ug)
Site of collection
Date of collection
Collector
GPS Location
water temp
pH
Depth (m)
Other
Requested sequence coverage
Sequencing Notes
contact scientist
Contact affiliation
Contact email
DNA/RNA Source
DNA extraction protocol
DNA/RNA conc (ng/ul)
Total amount of DNA/RNA shipped (ul)
Genome Sequencing Facility
Date Received by sequencing facility
Comments by sequencing facility
Sequencing date ETA
Date sequenced
Library
Library Construction (insert size bp)
Requested read length (bp)
Library construction protocol
Index #
Sequencer
Run number
Run #:Flow Cell ID
Lane number
FILE NAMES - supplied by sequencing facility
file type
MD5 checksum
Contact bioinformatician
Email contact
Date data sent/transferred
Date data received
FILES NAME ON FTP at Murdoch (http://files.ivec.org/bpa/)


    fieldnames = ['bpa_id',
                  'species',
                  'dataset', # NEW (model?)
                  'description', # NEW
                  'dna_concentration', # NEW
                  'total_dna', # NEW
                  'collection_site', # NEW (model?)
                  'collection_date', # NEW
                  'collector', # NEW
                  'gps_location', # NEW
                  'water_temp', # NEW
                  'ph', # NEW
                  'depth', # NEW
                  'other', # NEW 
                  'requested_sequence_coverage',
                  'sequencing_notes', # NEW
                  'contact_scientist',
                  'contact_affiliation',
                  'contact_email',
                  'sample_dna_source',           
                  'dna_extraction_protocol',
                  'dna_rna_concentration' # NEW
                  'total_dna_rna_shipped', # NEW
                  'sequencing_facility',
                  'date_received',
                  'comments_by_facility', # NEW
                  'sequencing_data_eta', # NEW
                  'date_sequenced', # NEW,
                  'library',
                  'library_construction',
                  'requested_read_length', # NEW
                  'library_construction_protocol',
                  'index_number',
                  'sequencer',
                  'run_number',
                  'flow_cell_id',
                  'lane_number',
                  'sequence_filename',
                  'sequence_filetype',
                  'md5_checksum',
                  'contact_bioinformatician_name', # NEW
                  'contact_bioinformatician_email' # NEW
                  'date_data_sent', # NEW
                  'data_data_received', # NEW
                  ]

    wb = xlrd.open_workbook(MELANOMA_SPREADSHEET_FILE)
    sheet = wb.sheet_by_name('DNA library Sequencing - Pilot')
    samples = []
    for row_idx in range(sheet.nrows)[2:]:  # the first two lines are headers
        vals = sheet.row_values(row_idx)
        # for date types try to convert to python dates
        types = sheet.row_types(row_idx)
        for i, t in enumerate(types):
            if t == xlrd.XL_CELL_DATE:
                vals[i] = datetime(*xldate_as_tuple(vals[i], wb.datemode))

        samples.append(dict(zip(fieldnames, vals)))

    return samples


def get_array_data():
    """
    Copy if the 'Array Data' Tab from the Melanoma_study_metadata document
    """

    fieldnames = ['batch_no',
                  'well_id',
                  'bpa_id',
                  'mia_id',
                  'array_id',
                  'call_rate',
                  'gender',
                  ]

    wb = xlrd.open_workbook(MELANOMA_SPREADSHEET_FILE)
    sheet = wb.sheet_by_name('Array data')
    rows = []
    for row_idx in range(sheet.nrows)[1:]:
        vals = sheet.row_values(row_idx)
        # for date types try to convert to python dates
        types = sheet.row_types(row_idx)
        for i, t in enumerate(types):
            if t == xlrd.XL_CELL_DATE:
                vals[i] = datetime(*xldate_as_tuple(vals[i], wb.datemode))

        rows.append(dict(zip(fieldnames, vals)))


    return rows



def ingest_runs(sample_data):
    def get_sequencer(name):
        if name == "":
            name = "Unknown"
        try:
            sequencer = Sequencer.objects.get(name=name)
        except Sequencer.DoesNotExist:
            sequencer = Sequencer(name=name)
            sequencer.save()
        return sequencer

    def get_sample(bpa_id):
        try:
            sample = MelanomaSample.objects.get(bpa_id__bpa_id=bpa_id)
            print("Found sample {0}".format(sample))
            return sample
        except MelanomaSample.DoesNotExist:
            print("No sample with ID {0}, quiting now".format(bpa_id))
            sys.exit(1)

    def get_run_number(e):
        """
        ANU does not have their run numbers entered.
        """

        run_number = get_clean_number(e['run_number'])
        if run_number is None:
            # see if its ANU and parse the run_number from the filename
            if e['whole_genome_sequencing_facility'].strip() == 'ANU':
                filename = e['sequence_filename'].strip()
                if filename != "":
                    try:
                        run_number = get_clean_number(filename.split('_')[7])
                        print("ANU run_number {0} parsed from filename".format(run_number))
                    except IndexError:
                        print("Filename {0} wrong format".format(filename))

        return run_number

    def add_run(entry):
        """
        The run produced several files
        """
        flow_cell_id = entry['flow_cell_id'].strip()
        bpa_id = entry['bpa_id'].strip()
        run_number = get_run_number(entry)

        try:
            run = MelanomaRun.objects.get(flow_cell_id=flow_cell_id,
                                          run_number=run_number,
                                          sample__bpa_id__bpa_id=bpa_id)
        except MelanomaRun.DoesNotExist:
            run = MelanomaRun()
            run.flow_cell_id = flow_cell_id
            run.run_number = run_number
            run.sample = get_sample(bpa_id)
            run.passage_number = get_clean_number(entry['passage_number'])
            run.index_number = get_clean_number(entry['index_number'])
            run.sequencer = get_sequencer(MELANOMA_SEQUENCER)  # Ignore the empty column
            run.lane_number = get_clean_number(entry['lane_number'])
            run.save()

        return run

    def add_file(e, run):
        """
        Add each sequence file produced by a run
        """

        def check_date(dt):
            """
            When reading in the data, and it was set as a date type in the excel sheet it should have been converted.
            if it wasn't, it may still be a valid date string.
            """
            if isinstance(dt, date):
                return dt
            if isinstance(dt, basestring):
                return dateutil.parser.parse(dt)

        file_name = e['sequence_filename'].strip()
        if file_name != "":
            f = MelanomaSequenceFile()
            f.sample = MelanomaSample.objects.get(bpa_id__bpa_id=e['bpa_id'])
            f.date_received_from_sequencing_facility = check_date(e['date_received'])
            f.run = run
            f.index_number = get_clean_number(e['index_number'])
            f.lane_number = get_clean_number(e['lane_number'])
            f.filename = file_name
            f.md5 = e['md5_checksum']
            f.note = pprint.pformat(e)
            f.save()

    for e in sample_data:
        sequence_run = add_run(e)
        add_file(e, sequence_run)


def ingest_gbr():
    sample_data = get_gbr_sample_data()
    ingest_bpa_ids(sample_data, 'GBR')
    ingest_samples(sample_data)
    ingest_arrays(get_array_data())
    ingest_runs(sample_data)


def run():
    ingest_gbr()

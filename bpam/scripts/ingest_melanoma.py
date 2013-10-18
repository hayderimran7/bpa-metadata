import sys
import pprint
import logging
import xlrd
from datetime import datetime
from unipath import Path

from apps.bpaauth.models import BPAUser
from apps.common.models import *
from apps.melanoma.models import *
from .utils import *

DATA_DIR = Path(Path(__file__).ancestor(3), "data/melanoma/")
MELANOMA_SPREADSHEET_FILE = Path(DATA_DIR, 'Melanoma_study_metadata.xlsx')

MELANOMA_SEQUENCER = "Illumina Hi Seq 2000"
BPA_ID = "102.100.100"

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)


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


def get_facility(name):
    """
    Return the sequencing facility with this name, or a new facility.
    """
    if name == '':
        name = "Unknown"
    try:
        facility = Facility.objects.get(name=name)
    except Facility.DoesNotExist:
        facility = Facility(name=name)
        facility.save()

    return facility

def ingest_samples(samples):
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
            sample.requested_sequence_coverage = e['sequence_coverage'].upper()
            sample.organism = Organism.objects.get(genus="Homo", species="Sapiens")
            sample.dna_source = get_dna_source(e['sample_dna_source'])
            sample.dna_extraction_protocol = e['dna_extraction_protocol']
            sample.tumor_stage = get_tumor_stage(e['sample_tumor_stage'])
            sample.gender = get_gender(e['sample_gender'])
            sample.histological_subtype = e['histological_subtype']
            sample.passage_number = get_clean_number(e['passage_number'])

            # facilities
            sample.array_analysis_facility = get_facility(e['array_analysis_facility'])
            sample.whole_genome_sequencing_facility = get_facility(e['whole_genome_sequencing_facility'])
            sample.sequencing_facility = get_facility(e['sequencing_facility'])

            sample.note = INGEST_NOTE + pprint.pformat(e)
            sample.save()
            logger.info("Ingested Melanoma sample {0}".format(sample.name))

    for sample in samples:
        add_sample(sample)


def ingest_arrays(arrays):
    """
    Melanoma Arrays
    """

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


def get_melanoma_sample_data():
    """
    The data sets is relatively small, so make a in-memory copy to simplify some operations.
    """

    fieldnames = ['bpa_id',
                  'sample_name',
                  'sequence_coverage',
                  'sequencing_facility',
                  'species',
                  'contact_scientist', # FIXME this isn't imported anywhere
                  'contact_affiliation',
                  'contact_email',
                  'sample_gender',
                  'sample_dna_source',
                  'sample_tumor_stage',
                  'histological_subtype',
                  'passage_number',
                  'dna_extraction_protocol',
                  'array_analysis_facility',
                  'date_sent_for_sequencing',
                  'whole_genome_sequencing_facility',
                  'date_received',
                  'library',
                  'library_construction',
                  'library_construction_protocol',
                  'index_number',
                  'sequencer',
                  'run_number',
                  'flow_cell_id',
                  'lane_number',
                  'sequence_filename',
                  'md5_checksum',
                  'file_path',
                  'file_url',
                  'analysed',
                  'analysed_url']

    wb = xlrd.open_workbook(MELANOMA_SPREADSHEET_FILE)
    sheet = wb.sheet_by_name('Melanoma_study_metadata')
    samples = []
    for row_idx in range(sheet.nrows)[2:]:  # the first two lines are headers
        vals = sheet.row_values(row_idx)

        # get rid of "" ID's
        if vals[0].strip() == "":
            continue

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

         # get rid of "" ID's
        if vals[2].strip() == "":
            continue

        # for date types try to convert to python dates
        types = sheet.row_types(row_idx)
        for i, t in enumerate(types):
            if t == xlrd.XL_CELL_DATE:
                vals[i] = datetime(*xldate_as_tuple(vals[i], wb.datemode))

        rows.append(dict(zip(fieldnames, vals)))

    return rows





def ingest_runs(sample_data):

    def get_protocol(entry):
        def get_library_type(library):
            """
            (('PE', 'Paired End'), ('SE', 'Single End'), ('MP', 'Mate Pair'))
            """
            new_str = library.lower()
            if new_str.find('pair') >= 0:
                return 'PE'
            if new_str.find('single') >= 0:
                return 'SE'
            if new_str.find('mate') >= 0:
                return 'MP'
            return 'UN'

        base_pairs = get_clean_number(entry['library_construction'])
        library_type = get_library_type(entry['library'])
        library_construction_protocol = entry['library_construction_protocol'].replace(',', '').capitalize()

        try:
            protocol = MelanomaProtocol.objects.get(
                base_pairs=base_pairs,
                library_type=library_type,
                library_construction_protocol=library_construction_protocol)
        except MelanomaProtocol.DoesNotExist:
            protocol = MelanomaProtocol(
                base_pairs=base_pairs,
                library_type=library_type,
                library_construction_protocol=library_construction_protocol)
            protocol.save()

        return protocol

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
            logger.info("Found sample {0}".format(sample))
            return sample
        except MelanomaSample.DoesNotExist:
            logger.error("No sample with ID {0}, quiting now".format(bpa_id))
            sys.exit(1)

    def get_run_number(e):
        """
        ANU does not have their run numbers entered.
        """

        run_number = get_clean_number(e['run_number'])
        if run_number in (None, ""):
            # see if its ANU and parse the run_number from the filename
            if e['whole_genome_sequencing_facility'].strip() == 'ANU':
                filename = e['sequence_filename'].strip()
                if filename != "":
                    try:
                        run_number = get_clean_number(filename.split('_')[7])
                        logger.info("ANU run_number {0} parsed from filename".format(run_number))
                    except IndexError:
                        logger.error("Filename {0} wrong format".format(filename))

        return run_number

    def add_run(entry):
        """
        The run produced several files
        """
        flow_cell_id = entry['flow_cell_id'].strip()
        bpa_id = entry['bpa_id'].strip()
        run_number = get_run_number(entry)

        try:
            run = MelanomaRun.objects.get(flow_cell_id=flow_cell_id, run_number=run_number, sample__bpa_id__bpa_id=bpa_id)
        except MelanomaRun.DoesNotExist:
            run = MelanomaRun()
            run.flow_cell_id = flow_cell_id
            run.run_number = run_number
            run.sample = get_sample(bpa_id)
            run.passage_number = get_clean_number(entry['passage_number'])
            run.index_number = get_clean_number(entry['index_number'])
            run.sequencer = get_sequencer(MELANOMA_SEQUENCER)  # Ignore the empty column
            run.lane_number = get_clean_number(entry['lane_number'])
            run.sequencing_facility = get_facility(entry['sequencing_facility'])
            run.array_analysis_facility = get_facility(entry['array_analysis_facility'])
            run.whole_genome_sequencing_facility = get_facility(entry['whole_genome_sequencing_facility'])
            run.DNA_extraction_protocol = entry['dna_extraction_protocol']
            run.protocol = get_protocol(entry)
            run.save()

        return run

    def add_file(e, run):
        """
        Add each sequence file produced by a run
        """

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


def ingest_melanoma():
    sample_data = get_melanoma_sample_data()
    ingest_bpa_ids(sample_data, 'Melanoma')
    ingest_samples(sample_data)
    ingest_arrays(get_array_data())
    ingest_runs(sample_data)


def run():
    add_organism(genus="Homo", species="Sapiens")
    ingest_melanoma()

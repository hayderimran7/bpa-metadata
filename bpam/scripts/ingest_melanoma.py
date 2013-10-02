import sys
import pprint
import csv
from datetime import date
import os.path

from apps.bpaauth.models import BPAUser
from apps.common.models import *
from apps.melanoma.models import *
from .utils import *


DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
MELANOMA_SAMPLE_FILE = os.path.join(DATA_DIR, 'melanoma_samples.csv')
MELANOMA_ARRAY_FILE = os.path.join(DATA_DIR, 'melanoma_arrays.csv')

MELANOMA_SEQUENCER = "Illumina Hi Seq 2000"
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
            sample.requested_sequence_coverage = e['sequence_coverage'].upper()
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


def get_melanoma_sample_data():
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

    with open(MELANOMA_SAMPLE_FILE, 'rb') as melanoma_files:
        fieldnames = ['bpa_id',
                      'sample_name',
                      'sequence_coverage',
                      'sequencing_facility',
                      'species',
                      'contact_scientist',
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
                      'md5_cheksum',
                      'file_path',
                      'file_url',
                      'analysed',
                      'analysed_url']

        reader = csv.DictReader(melanoma_files, fieldnames=fieldnames)
        # maybe use map() ?
        samples = []
        for sample in strip_all(reader):
            if not filter_out_sample(sample):
                samples.append(sample)
        return samples


def get_array_data():
    """
    Copy if the 'Array Data' Tab from the Melanoma_study_metadata document
    """

    with open(MELANOMA_ARRAY_FILE, 'rb') as array_data:
        fieldnames = ['batch_no',
                      'well_id',
                      'bpa_id',
                      'mia_id',
                      'array_id',
                      'call_rate',
                      'gender',
                      ]

        reader = csv.DictReader(array_data, fieldnames=fieldnames)
        return strip_all(reader)


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
        file_name = e['sequence_filename'].strip()
        if file_name != "":
            f = MelanomaSequenceFile()
            f.sample = MelanomaSample.objects.get(bpa_id__bpa_id=e['bpa_id'])
            f.date_received_from_sequencing_facility = get_date(e['date_received'].strip())
            f.run = run
            f.index_number = get_clean_number(e['index_number'])
            f.lane_number = get_clean_number(e['lane_number'])
            f.filename = file_name
            f.md5 = e['md5_cheksum']
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
    add_organism(genus="Homo", species="Sapient")
    ingest_melanoma()

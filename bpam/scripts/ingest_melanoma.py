import sys
import pprint
import logging
from datetime import datetime
from datetime import date

import xlrd
from unipath import Path

from apps.common.models import DNASource, Facility, Sequencer
from apps.melanoma.models import (
    TumorStage,
    MelanomaSample,
    Organism,
    MelanomaProtocol,
    Array,
    BPAUniqueID,
    MelanomaRun,
    MelanomaSequenceFile)

from libs import ingest_utils, user_helper
from libs import bpa_id_utils


# some defaults to fall back on
DEFAULT_DATA_DIR = Path(Path(__file__).ancestor(3), "data/melanoma/")
DEFAULT_SPREADSHEET_FILE = Path(DEFAULT_DATA_DIR, 'Melanoma_study_metadata.xlsx')

MELANOMA_SEQUENCER = "Illumina Hi Seq 2000"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('MELANOMA')


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
        if gender == '':
            gender = 'U'
        return gender

    def get_contact_scientist(names):
        """
        Get a user associated with this sample.
        Names in the source doc looks like this:
        James Wilmott/Grant McCathur/Mark Shackleton
        or
        James Wilmott
        So pick the first one. We don't have more than one scientist associated with a sample.
        If they want that, make a group.
        """

        if names.find('/') != -1:
            name = names.split('/')[0]
            return user_helper.get_user_by_full_name(name)
        return user_helper.get_user_by_full_name(names)

    def add_sample(e):
        bpa_id = e['bpa_id']
        try:
            # Test if sample already exists
            sample = MelanomaSample.objects.get(bpa_id__bpa_id=bpa_id)
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
        sample.passage_number = ingest_utils.get_clean_number(e['passage_number'])

        sample.contact_scientist = get_contact_scientist(e['contact_scientists'])

        # facilities
        sample.array_analysis_facility = get_facility(e['array_analysis_facility'])
        sample.whole_genome_sequencing_facility = get_facility(e['whole_genome_sequencing_facility'])
        sample.sequencing_facility = get_facility(e['sequencing_facility'])

        sample.note = u'{0} {1} {2}'.format(e['contact_scientists'], e['contact_affiliation'], e['contact_email'])
        sample.debug_note = ingest_utils.INGEST_NOTE + pprint.pformat(e)
        sample.save()
        logger.info("Ingested Melanoma sample {0}".format(sample.name))

    for s in samples:
        add_sample(s)


def ingest_arrays(arrays):
    """
    Melanoma Arrays
    """

    def get_gender(gender):
        gender = gender.strip().lower()
        if gender == "male":
            return 'M'
        if gender == "female":
            return 'F'
        return 'U'

    for e in arrays:
        try:
            array = Array.objects.get(bpa_id__bpa_id=e['bpa_id'])
        except Array.DoesNotExist:
            array = Array()
            array.bpa_id = bpa_id_utils.get_bpa_id(e['bpa_id'], project_name="Melanoma")
            array.note = u"Created during array ingestion on {0}".format(date.today())

        array.batch_number = int(e['batch_no'])
        array.mia_id = e['mia_id']
        array.array_id = e['array_id']
        array.call_rate = float(e['call_rate'])
        array.gender = get_gender(e['gender'])
        array.well_id = e['well_id']
        array.save()


def get_melanoma_sample_data(spreadsheet_file):
    """
    The data sets is relatively small, so make a in-memory copy to simplify some operations.
    """

    fieldnames = ['bpa_id',
                  'sample_name',
                  'sequence_coverage',
                  'sequencing_facility',
                  'species',
                  'contact_scientists',
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

    wb = xlrd.open_workbook(spreadsheet_file)
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
                vals[i] = datetime(*xlrd.xldate_as_tuple(vals[i], wb.datemode))

        samples.append(dict(zip(fieldnames, vals)))

    return samples


def get_array_data(spreadsheet_file):
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

    wb = xlrd.open_workbook(spreadsheet_file)
    sheet = wb.sheet_by_name('Array data')
    rows = []
    for row_idx in range(sheet.nrows)[1:]:
        vals = sheet.row_values(row_idx)

        # get rid of "" ID's
        if vals[2].strip() == "":
            continue

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

        base_pairs = ingest_utils.get_clean_number(entry['library_construction'])
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

    def get_run_number(entry):
        """
        ANU does not have their run numbers entered.
        """

        run_number = ingest_utils.get_clean_number(entry['run_number'])
        if run_number in (None, ""):
            # see if its ANU and parse the run_number from the filename
            if entry['whole_genome_sequencing_facility'].strip() == 'ANU':
                filename = entry['sequence_filename'].strip()
                if filename != "":
                    try:
                        run_number = ingest_utils.get_clean_number(filename.split('_')[7])
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
            nrun = MelanomaRun.objects.get(flow_cell_id=flow_cell_id, run_number=run_number,
                                           sample__bpa_id__bpa_id=bpa_id)
        except MelanomaRun.DoesNotExist:
            nrun = MelanomaRun()
            nrun.flow_cell_id = flow_cell_id
            nrun.run_number = run_number
            nrun.sample = get_sample(bpa_id)

            # Update FIXME
            nrun.passage_number = ingest_utils.get_clean_number(entry['passage_number'])
            nrun.index_number = ingest_utils.get_clean_number(entry['index_number'])
            nrun.sequencer = get_sequencer(MELANOMA_SEQUENCER)  # Ignore the empty column
            nrun.lane_number = ingest_utils.get_clean_number(entry['lane_number'])
            nrun.sequencing_facility = get_facility(entry['sequencing_facility'])
            nrun.array_analysis_facility = get_facility(entry['array_analysis_facility'])
            nrun.whole_genome_sequencing_facility = get_facility(entry['whole_genome_sequencing_facility'])
            nrun.DNA_extraction_protocol = entry['dna_extraction_protocol']

            nrun.protocol = get_protocol(entry)
            nrun.save()
            # this just seems wrong to me...
            nrun.protocol.run = nrun
            nrun.protocol.save()

        return nrun

    def add_file(entry, run):
        """
        Add each sequence file produced by a run
        """

        file_name = entry['sequence_filename'].strip()
        md5 = entry['md5_checksum'].strip()

        if file_name == '':
            logger.warning('Filename is not set, ignoring')
            return

        try:
            f = MelanomaSequenceFile.objects.get(filename=file_name, md5=md5)
        except MelanomaSequenceFile.DoesNotExist:
            f = MelanomaSequenceFile()

        f.sample = MelanomaSample.objects.get(bpa_id__bpa_id=entry['bpa_id'])
        f.date_received_from_sequencing_facility = ingest_utils.get_date(entry['date_received'])
        f.run = run
        f.index_number = ingest_utils.get_clean_number(entry['index_number'])
        f.lane_number = ingest_utils.get_clean_number(entry['lane_number'])
        f.filename = file_name
        f.md5 = md5
        f.note = pprint.pformat(entry)
        f.save()

    for e in sample_data:
        sequence_run = add_run(e)
        add_file(e, sequence_run)


def ingest_melanoma(spreadsheet_file):
    sample_data = get_melanoma_sample_data(spreadsheet_file)
    bpa_id_utils.ingest_bpa_ids(sample_data, 'Melanoma')
    ingest_samples(sample_data)
    ingest_arrays(get_array_data(spreadsheet_file))
    ingest_runs(sample_data)


def run(spreadsheet_file=DEFAULT_SPREADSHEET_FILE):
    """
    Pass parameters like below:
    vpython-bpam manage.py runscript ingest_melanoma --script-args Melanoma_study_metadata.xlsx
    """

    logger.info('Ingesting spreadsheet: ' + spreadsheet_file)
    ingest_utils.add_organism(genus="Homo", species="Sapiens")
    ingest_melanoma(spreadsheet_file)

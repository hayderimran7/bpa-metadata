# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from libs.excel_wrapper import ExcelWrapper
from libs.fetch_data import Fetcher, get_password
from apps.common.models import DNASource, Facility, Sequencer
from apps.melanoma.models import (TumorStage, MelanomaSample, Organism, MelanomaProtocol, Array, MelanomaRun,
                                  MelanomaSequenceFile)
from libs import ingest_utils, user_helper, bpa_id_utils, logger_utils
from unipath import Path

MELANOMA_SEQUENCER = "Illumina Hi Seq 2000"

METADATA_URL = 'https://downloads-qcif.bioplatforms.com/bpa/melanoma/metadata/'  # the folder
METADATA_FILE = 'metadata.xlsx'  # the file
DATA_DIR = Path(ingest_utils.METADATA_ROOT, 'melanoma/')

logger = logger_utils.get_logger(__name__)


def _get_bpa_id(entry):
    """
    Get or make BPA ID
    """

    bpa_id, report = bpa_id_utils.get_bpa_id(entry.bpa_id, 'MELANOMA', 'Melanoma', 'ID Created by Melanoma Ingestor')
    if bpa_id is None:
        logger.warning('Could not add entry in {}, row {}, BPA ID Invalid: {}'.format(entry.file_name, entry.row,
                                                                                      report))
        return None
    return bpa_id


def get_dna_source(description):
    """ Get a DNA source if it exists, if it doesn't make it. """

    source, _ = DNASource.objects.get_or_create(description=description.capitalize())
    return source


def get_tumor_stage(description):
    """ Get the tumor stage if it exists, else make it. """

    description = description.capitalize()
    if description == "":
        description = "Not applicable"

    stage, _ = TumorStage.objects.get_or_create(description=description)
    return stage


def get_facility(name):
    """
    Return the sequencing facility with this name, or a new facility.
    """
    if name == '':
        name = "Unknown"

    facility, _ = Facility.objects.get_or_create(name=name)
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
        bpa_id = _get_bpa_id(e)
        if bpa_id is None:
            return

        organism, _ = Organism.objects.get_or_create(genus="Homo", species="Sapiens")

        sample, created = MelanomaSample.objects.get_or_create(bpa_id=bpa_id, organism=organism)
        if created:
            sample.bpa_id = bpa_id
            sample.name = e.sample_name
            sample.requested_sequence_coverage = e.sequence_coverage.upper()
            sample.dna_source = get_dna_source(e.sample_dna_source)
            sample.dna_extraction_protocol = e.dna_extraction_protocol
            sample.tumor_stage = get_tumor_stage(e.sample_tumor_stage)
            sample.gender = get_gender(e.sample_gender)
            sample.histological_subtype = e.histological_subtype
            sample.passage_number = ingest_utils.get_clean_number(e.passage_number)

            sample.contact_scientist = get_contact_scientist(e.contact_scientists)

            # facilities
            sample.array_analysis_facility = get_facility(e.array_analysis_facility)
            sample.whole_genome_sequencing_facility = get_facility(e.whole_genome_sequencing_facility)
            sample.sequencing_facility = get_facility(e.sequencing_facility)

            sample.note = u'{0} {1} {2}'.format(e.contact_scientists, e.contact_affiliation, e.contact_email)
            sample.debug_note = ingest_utils.pretty_print_namedtuple(e)
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
        bpa_id = _get_bpa_id(e)
        if bpa_id is None:
            return
        Array.objects.get_or_create(bpa_id=bpa_id,
                                    batch_number=int(e.batch_no),
                                    mia_id=e.mia_id,
                                    array_id=e.array_id,
                                    call_rate=float(e.call_rate),
                                    gender=get_gender(e.gender),
                                    well_id=e.well_id)


def strip_path(fname):
    """strips / """
    i = fname.rfind("/")
    if i != -1:
        return fname[i:]
    return fname


def get_melanoma_sample_data(file_name):
    """ The data sets is relatively small, so make a in-memory copy to simplify some operations. """

    field_spec = [('bpa_id', 'Unique Identifier', lambda s: s.replace('/', '.')),
                  ('sample_name', 'Sample Name', None),
                  ('sequence_coverage', 'Sequence coverage', None),
                  ('sequencing_facility', 'Sequencing faciltiy', None),
                  ('species', 'Species', None),
                  ('contact_scientists', 'Melanoma contact scientist', None),
                  ('contact_affiliation', 'Contact affiliation', None),
                  ('contact_email', 'Contact email', None),
                  ('sample_gender', 'Sex', None),
                  ('sample_dna_source', 'DNA Source', None),
                  ('sample_tumor_stage', 'Tumor Staging (where applicable)', None),
                  ('histological_subtype', 'histological subtype', None),
                  ('passage_number', 'Passage Number (if known)', None),
                  ('dna_extraction_protocol', 'DNA extraction protocol', None),
                  ('array_analysis_facility', 'Array analysis facility', None),
                  ('date_sent_for_sequencing', 'Date sent to sequencing Facility', None),
                  ('whole_genome_sequencing_facility', 'Name of Whole Genome Sequencing Facility', None),
                  ('date_received', 'Date Received', None),
                  ('library', 'Library', None),
                  ('library_construction', 'Library Construction', None),
                  ('library_construction_protocol', 'Library construction protocol', None),
                  ('index_number', 'Index #', None),
                  ('sequencer', 'Sequencer', None),
                  ('run_number', 'Run number', None),
                  ('flow_cell_id', 'Run #:Flow Cell ID', None),
                  ('lane_number', 'Lane number', None),
                  ('sequence_filename', 'Sequence file names - supplied by sequencing facility', strip_path),
                  ('md5_checksum', 'MD5 checksum', None), ]

    wrapper = ExcelWrapper(field_spec,
                           file_name,
                           sheet_name='Melanoma_study_metadata',
                           header_length=1,
                           column_name_row_index=0)
    return wrapper.get_all()


def get_array_data(file_name):
    """
    Copy if the 'Array Data' Tab from the Melanoma_study_metadata document
    """

    field_spec = [
        ('batch_no', 'Batch No', None),
        ('well_id', 'Well ID', None),
        ('bpa_id', 'BPA ID', lambda s: s.replace('/', '.')),
        ('mia_id', 'MIA ID', None),
        ('array_id', 'Array ID', None),
        ('call_rate', 'Call Rate', None),
        ('gender', 'Gender', None),
    ]

    wrapper = ExcelWrapper(field_spec, file_name, sheet_name='Array data', header_length=1, column_name_row_index=0)
    return wrapper.get_all()


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

        base_pairs = ingest_utils.get_clean_number(entry.library_construction)
        library_type = get_library_type(entry.library)
        library_construction_protocol = entry.library_construction_protocol.replace(',', '').capitalize()

        protocol, _ = MelanomaProtocol.objects.get_or_create(
            base_pairs=base_pairs,
            library_type=library_type,
            library_construction_protocol=library_construction_protocol)

        return protocol

    def get_sequencer(name):
        if name == "":
            name = "Unknown"

        sequencer, _ = Sequencer.objects.get_or_create(name=name)
        return sequencer

    def get_run_number(entry):
        """
        ANU does not have their run numbers entered.
        """

        run_number = ingest_utils.get_clean_number(entry.run_number)
        if run_number in (None, ""):
            # see if its ANU and parse the run_number from the filename
            if entry.whole_genome_sequencing_facility.strip() == 'ANU':
                filename = entry.sequence_filename.strip()
                if filename != "":
                    try:
                        run_number = ingest_utils.get_clean_number(filename.split('_')[7])
                    except IndexError:
                        logger.error("Filename {0} wrong format".format(filename))

        return run_number

    def add_run(entry):
        """
        The run produced several files
        """
        bpa_id = _get_bpa_id(entry)
        if bpa_id is None:
            return
        run_number = get_run_number(entry)
        flow_cell_id = entry.flow_cell_id.strip()
        sample, _ = MelanomaSample.objects.get_or_create(bpa_id=bpa_id)
        nrun, created = MelanomaRun.objects.get_or_create(flow_cell_id=flow_cell_id,
                                                          run_number=run_number,
                                                          sample=sample)
        if created:
            nrun.flow_cell_id = flow_cell_id
            nrun.run_number = run_number
            nrun.passage_number = ingest_utils.get_clean_number(entry.passage_number)
            nrun.index_number = ingest_utils.get_clean_number(entry.index_number)
            nrun.sequencer = get_sequencer(MELANOMA_SEQUENCER)  # Ignore the empty column
            nrun.lane_number = ingest_utils.get_clean_number(entry.lane_number)
            nrun.sequencing_facility = get_facility(entry.sequencing_facility)
            nrun.array_analysis_facility = get_facility(entry.array_analysis_facility)
            nrun.whole_genome_sequencing_facility = get_facility(entry.whole_genome_sequencing_facility)
            nrun.DNA_extraction_protocol = entry.dna_extraction_protocol

            nrun.protocol = get_protocol(entry)
            nrun.save()
            # this just seems wrong to me...
            nrun.protocol.run = nrun
            nrun.protocol.save()

        return nrun

    def add_file(entry, _run):
        """
        Add each sequence file produced by a run
        """
        bpa_id = _get_bpa_id(entry)
        if bpa_id is None:
            return

        file_name = entry.sequence_filename.strip()
        md5 = entry.md5_checksum.strip()

        if file_name == '':
            logger.warning('Filename is not set, ignoring')
            return

        sample = MelanomaSample.objects.get(bpa_id=bpa_id)
        f, created = MelanomaSequenceFile.objects.get_or_create(run=_run, sample=sample)
        if created:
            f.date_received_from_sequencing_facility = ingest_utils.get_date(entry.date_received)
            f.run = _run
            f.index_number = ingest_utils.get_clean_number(entry.index_number)
            f.lane_number = ingest_utils.get_clean_number(entry.lane_number)
            f.filename = file_name
            f.md5 = md5
            f.debug_note = ingest_utils.pretty_print_namedtuple(entry)
            f.save()

    for e in sample_data:
        sequence_run = add_run(e)
        if sequence_run:
            add_file(e, sequence_run)


def ingest(spreadsheet_file):
    sample_data = list(get_melanoma_sample_data(spreadsheet_file))
    # add all the ID's
    bpa_id_utils.ingest_bpa_ids(sample_data, 'MELANOMA', 'Melanoma')
    ingest_samples(sample_data)
    ingest_arrays(list(get_array_data(spreadsheet_file)))
    ingest_runs(sample_data)


class Command(BaseCommand):
    help = 'Ingest Melanoma'

    def handle(self, *args, **options):
        password = get_password("melanoma")
        logger.info('Ingesting spreadsheet: from {0}'.format(METADATA_URL))
        # Organism.objects.get_or_create(genus="Homo", species="Sapiens")
        fetcher = Fetcher(DATA_DIR, METADATA_URL, auth=('melanoma', password))

        fetcher.fetch(METADATA_FILE)
        ingest(DATA_DIR + METADATA_FILE)

from unipath import Path

from apps.common.models import DNASource, Sequencer, Facility

from apps.wheat_pathogens_transcript.models import (
    WheatPathogenTranscriptSample,
    WheatPathogenTranscriptProtocol,
    WheatPathogenTranscriptRun,
    WheatPathogenTranscriptSequenceFile,
    Organism,
)

from libs import ingest_utils, user_helper, bpa_id_utils
from libs.logger_utils import get_logger
from libs.excel_wrapper import ExcelWrapper

PROJECT_DESCRIPTION = 'Wheat Pathogens Transcript'
PROJECT_ID = 'WHEAT_PATHOGENS_TRANCRIPT'

logger = get_logger(__name__)

DATA_DIR = Path(Path(__file__).ancestor(3), "data/wheat_pathogens/")
DEFAULT_SPREADSHEET_FILE = Path(DATA_DIR, 'current')

BPA_ID = "102.100.100"
DESCRIPTION = 'Wheat Pathogens Transcript'
METADATA_URL = "https://downloads.bioplatforms.com/wheat_pathogens_transcript/metadata/Wheat_Pathogen_Transcript_data.xlsx"


def ingest_samples(samples):
    def get_facility(name):
        """
        Return the sequencing facility with this name, or a new facility.
        """
        if name.strip() == '':
            name = 'Unknown'

        facility, created = Facility.objects.get_or_create(name=name)

        return facility

    def add_sample(e):
        """
        Adds new sample or updates existing sample
        """

        bpa_id = bpa_id_utils.get_bpa_id(e.bpa_id, PROJECT_ID, PROJECT_DESCRIPTION)
        if bpa_id is None:
            return

        pathogen_sample, created = WheatPathogenTranscriptSample.objects.get_or_create(bpa_id=bpa_id)
        pathogen_sample.name = e.sample_name
        pathogen_sample.index = e.index_sequence
        # scientist
        logger.debug(e)
        pathogen_sample.contact_scientist = user_helper.get_user(
            e.contact_scientist,
            '',
            (DESCRIPTION, ''))

        logger.info("Ingested Pathogens sample {0}".format(pathogen_sample.name))

    for sample in samples:
        add_sample(sample)


def ingest_runs(sample_data):
    def get_protocol(entry):
        def get_library_type(libtype):
            """
            (('PE', 'Paired End'), ('SE', 'Single End'), ('MP', 'Mate Pair'))
            """
            new_str = libtype.lower()
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

        protocol, created = WheatPathogenTranscriptProtocol.objects.get_or_create(
            base_pairs=base_pairs,
            library_type=library_type,
            library_construction_protocol=library_construction_protocol)

        if created:
            logger.debug('Created Protocol {0}'.format(protocol))

        return protocol

    def get_sequencer(name):
        if name == '':
            name = u'Unknown'

        sequencer, created = Sequencer.objects.get_or_create(name=name)
        return sequencer

    def get_sample(bpa_id):
        sample, created = WheatPathogenTranscriptSample.objects.get_or_create(bpa_id__bpa_id=bpa_id)
        if created:
            logger.debug("Created sample ID {0}".format(bpa_id))
        return sample

    def get_run_number(entry):
        run_number = ingest_utils.get_clean_number(entry.run_number.replace('RUN #', ''))
        return run_number

    def get_lane_number(entry):
        lane_number = ingest_utils.get_clean_number(entry.lane_number.replace('LANE', ''))
        return lane_number

    def add_run(entry):
        """
        The run produced several files
        """
        flow_cell_id = entry.flow_cell_id.strip()
        run_number = get_run_number(entry)

        bpa_id = bpa_id_utils.get_bpa_id(entry.bpa_id, '%s' % PROJECT_ID, PROJECT_DESCRIPTION)
        if bpa_id is None:
            return
        try:
            pathogen_sample = WheatPathogenTranscriptSample.objects.get(bpa_id=bpa_id)
        except WheatPathogenTranscriptSample.DoesNotExist:
            logger.error('Wheat Pathogen Transcript sample with BPA ID {0} does not exist'.format(bpa_id))
            return

        pathogen_run, created = WheatPathogenTranscriptRun.objects.get_or_create(
            flow_cell_id=flow_cell_id,
            run_number=run_number,
            sample=pathogen_sample,
            sequencer=get_sequencer(entry.sequencer))

        # always update
        pathogen_run.flow_cell_id = flow_cell_id
        pathogen_run.run_number = run_number
        pathogen_run.sample = get_sample(bpa_id)
        pathogen_run.index_number = ingest_utils.get_clean_number(entry.index_number)
        pathogen_run.lane_number = ingest_utils.get_clean_number(entry.lane_number)
        pathogen_run.protocol = get_protocol(e)
        pathogen_run.save()

        # FIXME, I'm sure this is wrong
        pathogen_run.protocol.run = pathogen_run
        pathogen_run.protocol.save()

        return pathogen_run

    def add_file(entry, pathogen_run):
        """
        Add each sequence file produced by a run
        """
        bpa_id = bpa_id_utils.get_bpa_id(entry.bpa_id, PROJECT_ID, PROJECT_DESCRIPTION)
        if bpa_id is None:
            return

        file_name = entry.sequence_filename.strip()
        if file_name != '':
            f = WheatPathogenTranscriptSequenceFile()
            f.sample = WheatPathogenTranscriptSample.objects.get(bpa_id=bpa_id)
            f.run = pathogen_run
            f.index_number = ingest_utils.get_clean_number(entry.index_number)
            f.lane_number = get_lane_number(entry)
            f.filename = file_name
            f.md5 = entry.md5_checksum
            f.note = ingest_utils.pretty_print_namedtuple(entry)
            f.save()

    for e in sample_data:
        sequence_run = add_run(e)
        add_file(e, sequence_run)


def ingest(file_name):
    sample_data = list(get_pathogen_sample_data(file_name))
    bpa_id_utils.ingest_bpa_ids(sample_data, PROJECT_ID, PROJECT_DESCRIPTION)
    ingest_samples(sample_data)
    ingest_runs(sample_data)


def get_pathogen_sample_data(file_name):
    """
    The data sets is relatively small, so make a in-memory copy to simplify some operations.
    """

    field_spec = [('bpa_id', 'Unique ID', lambda s: s.replace('/', '.')),
                  ('submission_document', 'Submission document', None),
                  ('sample_number', 'Sample Number', None),
                  ('sample_name', 'Sample name (supplied by researcher)', None),
                  ('contact_scientist', 'Contact researcher', None),
                  ('index_sequence', 'Index', None),
                  ('library', 'Library', None),
                  ('library_construction', 'Library Construction (insert size bp)', None),
                  ('library_construction_protocol', 'Library construction protocol', None),
                  ('sequencer', 'Sequencer', None),
                  ('run_number', 'Run number', None),
                  ('flow_cell_id', 'Run #:Flow Cell ID', None),
                  ('lane_number', 'Lane number', None),
                  ('sequence_filename', 'File name', None),
                  ('md5_checksum', 'MD5 checksum', None),
    ]

    wrapper = ExcelWrapper(
        field_spec,
        file_name,
        sheet_name='Sheet1',
        header_length=2,
        column_name_row_index=0)
    return wrapper.get_all()


def truncate():
    from django.db import connection

    cursor = connection.cursor()
    cursor.execute('TRUNCATE TABLE "{0}" CASCADE'.format(WheatPathogenTranscriptSample._meta.db_table))
    cursor.execute('TRUNCATE TABLE "{0}" CASCADE'.format(WheatPathogenTranscriptRun._meta.db_table))
    cursor.execute('TRUNCATE TABLE "{0}" CASCADE'.format(WheatPathogenTranscriptProtocol._meta.db_table))
    cursor.execute('TRUNCATE TABLE "{0}" CASCADE'.format(WheatPathogenTranscriptSequenceFile._meta.db_table))

def run(file_name=DEFAULT_SPREADSHEET_FILE):
    """
    Pass parameters like below:
    vpython-bpam manage.py runscript ingest_gbr --script-args Wheat_pathogens_genomic_metadata.xlsx
    """
    truncate()
    ingest_utils.fetch_metadata(METADATA_URL, file_name)
    ingest(file_name)

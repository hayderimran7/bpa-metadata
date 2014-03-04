from unipath import Path

from apps.common.models import DNASource, BPAUniqueID, Sequencer
from apps.wheat_cultivars.models import Organism, CultivarProtocol, CultivarSample, CultivarRun, CultivarSequenceFile
from libs import ingest_utils
from libs import bpa_id_utils
from libs.logger_utils import get_logger
from libs.excel_wrapper import ExcelWrapper


logger = get_logger(__name__)

DATA_DIR = Path(Path(__file__).ancestor(3), "data/wheat_cultivars/")
DEFAULT_SPREADSHEET_FILE = Path(DATA_DIR, 'current')

BPA_ID = "102.100.100"
DESCRIPTION = 'Wheat Cultivars'


def get_dna_source(description):
    """
    Get a DNA source if it exists, if it doesn't make it.
    """

    description = description.strip().capitalize()
    if description == '':
        logger.debug('Set blank description to unknown')
        description = 'Unknown'

    try:
        source = DNASource.objects.get(description=description)
    except DNASource.DoesNotExist:
        source = DNASource(description=description)
        source.note = 'Added by Cultivars Project'
        source.save()

    return source


def ingest_samples(samples):
    """
    Add all the cultivar samples
    """
    wheat_organism = Organism(genus='Triticum', species='Aestivum')
    wheat_organism.save()

    def add_sample(e):
        """
        Adds new sample or updates existing sample
        """

        bpa_id = e.bpa_id

        if not bpa_id_utils.is_good_bpa_id(bpa_id):
            logger.warning('BPA ID {0} does not look like a real ID, ignoring'.format(bpa_id))
            return

        try:
            # Test if sample already exists
            cultivar_sample = CultivarSample.objects.get(bpa_id__bpa_id=bpa_id)
        except CultivarSample.DoesNotExist:
            cultivar_sample = CultivarSample()
            cultivar_sample.bpa_id = BPAUniqueID.objects.get(bpa_id=bpa_id)

        cultivar_sample.organism = wheat_organism
        cultivar_sample.name = e.name
        cultivar_sample.dna_extraction_protocol = e.dna_extraction_protocol
        cultivar_sample.cultivar_code = e.cultivar_code
        cultivar_sample.extract_name = e.extract_name
        cultivar_sample.casava_version = e.casava_version
        cultivar_sample.protocol_reference = e.protocol_reference
        cultivar_sample.debug_note = ingest_utils.INGEST_NOTE + ingest_utils.pretty_print_namedtuple(e)

        cultivar_sample.save()
        logger.info("Ingested Cultivars sample {0}".format(cultivar_sample.name))

    for sample in samples:
        add_sample(sample)


def get_cultivar_sample_data(file_name):
    """
    The data sets is relatively small, so make a in-memory copy to simplify some operations.
    """

    field_spec = [('bpa_id', 'Unique ID', None),
                  ('name', 'Variety', None),
                  ('cultivar_code', 'Comment[Sample code]', None),  # C
                  ('dna_extraction_protocol', 'Protocol REF', None),
                  ('extract_name', 'Extract Name', None),
                  ('library_construction_protocol', 'Protocol REF', None),
                  ('library_construction', 'Library nominal fragment size', None),
                  ('library', 'Library', None),
                  ('index_sequence', 'Index', None),
                  ('protocol_reference', 'Protocol REF', None),
                  ('index_number', 'Parameter Value[Cycle count]', None),  # cycle count CHECK
                  ('sequencer', 'Sequencing instrument', None),
                  ('casava_version', 'CASAVA version', None),
                  ('run_number', 'Parameter Value[run number]', None),
                  ('flow_cell_id', 'Parameter Value[flow cell identifier]', None),
                  ('lane_number', 'Parameter Value[lane number]', None),
                  ('sequence_filename', 'Raw Data File', None),
                  ('corrected_sequence_filename', 'Comment[Corrected file name]', None),
                  ('sequence_filetype', 'Comment[file format]', None),
                  ('md5_checksum', 'Comment[MD5 checksum]', None),
    ]

    wrapper = ExcelWrapper(
        field_spec,
        file_name,
        sheet_name='a_genome_seq_assay_BPA-Wheat-Cu',
        header_length=1,
        column_name_row_index=0)
    return wrapper.get_all()


def ingest_runs(sample_data):
    def get_protocol(entry):
        def get_library_type(libtype):
            """
            (('PE', 'Paired End'), ('SE', 'Single End'), ('MP', 'Mate Pair'))
            """
            new_str = libtype.lower()
            if new_str.find('paired') >= 0:
                return 'PE'
            if new_str.find('single') >= 0:
                return 'SE'
            if new_str.find('mate') >= 0:
                return 'MP'
            return 'UN'

        base_pairs = ingest_utils.get_clean_number(entry.library_construction)
        library_type = get_library_type(entry.library)
        library_construction_protocol = entry.library_construction_protocol.replace(',', '').capitalize()

        try:
            protocol = CultivarProtocol.objects.get(base_pairs=base_pairs,
                                                    library_type=library_type,
                                                    library_construction_protocol=library_construction_protocol)
        except CultivarProtocol.DoesNotExist:
            protocol = CultivarProtocol(base_pairs=base_pairs,
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
        sample, created = CultivarSample.objects.get_or_create(bpa_id__bpa_id=bpa_id)
        if created:
            logger.info("New sample with ID {0}".format(bpa_id))
        return sample

    def get_run_number(entry):
        run_number = ingest_utils.get_clean_number(entry.run_number)
        return run_number

    def add_run(entry):
        """
        The run produced several files
        """
        flow_cell_id = entry.flow_cell_id.strip()
        bpa_id = entry.bpa_id.strip()
        run_number = get_run_number(entry)

        cultivar_run, created = CultivarRun.objects.get_or_create(
            flow_cell_id=flow_cell_id,
            run_number=run_number,
            sample__bpa_id__bpa_id=bpa_id)

        # just update
        cultivar_run.flow_cell_id = flow_cell_id
        cultivar_run.run_number = run_number
        cultivar_run.sample = get_sample(bpa_id)
        cultivar_run.index_number = ingest_utils.get_clean_number(entry.index_number)
        cultivar_run.sequencer = get_sequencer(entry.sequencer)
        cultivar_run.lane_number = ingest_utils.get_clean_number(entry.lane_number)
        cultivar_run.protocol = get_protocol(e)
        cultivar_run.save()

        # FIXME, I'm sure this is wrong
        cultivar_run.protocol.run = cultivar_run
        cultivar_run.protocol.save()

        return cultivar_run

    def add_file(entry, cultivar_run):
        """
        Add each sequence file produced by a run
        """

        # Use the corrected sequence filename, as for this project (Wheat Cultivars),
        # that's what the user wants to see
        file_name = entry.corrected_sequence_filename.strip()
        if file_name != "":
            f = CultivarSequenceFile()
            f.sample = CultivarSample.objects.get(bpa_id__bpa_id=entry.bpa_id)
            f.run = cultivar_run
            f.index_number = ingest_utils.get_clean_number(entry.index_number)
            f.lane_number = ingest_utils.get_clean_number(entry.lane_number)
            f.filename = file_name
            f.original_sequence_filename = entry.sequence_filename
            f.md5 = entry.md5_checksum
            f.note = ingest_utils.pretty_print_namedtuple(entry)
            f.save()

    for e in sample_data:
        sequence_run = add_run(e)
        add_file(e, sequence_run)


def ingest(spreadsheet_file):
    logger.info('Starting Wheat Cultivar metadata import')
    sample_data = list(get_cultivar_sample_data(spreadsheet_file))
    bpa_id_utils.ingest_bpa_ids(sample_data, 'WHEAT_CULTIVAR', 'Wheat Cultivars')
    ingest_samples(sample_data)
    ingest_runs(sample_data)
    logger.info('Wheat Cultivar metadata import complete')


def run(file_name=DEFAULT_SPREADSHEET_FILE):
    """
    Pass parameters like below:
    vpython-bpam manage.py runscript ingest_gbr --script-args Wheat_cultivars.xlsx
    """

    ingest(file_name)

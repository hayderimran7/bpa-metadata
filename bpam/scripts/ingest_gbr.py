import sys
from unipath import Path

from apps.common.models import DNASource, Facility, BPAUniqueID, Sequencer
from apps.gbr.models import Organism, CollectionEvent, GBRSample, GBRRun, GBRProtocol, GBRSequenceFile
from libs import ingest_utils, user_helper
from libs import bpa_id_utils
from libs.logger_utils import get_logger
from libs.excel_wrapper import ExcelWrapper


logger = get_logger(__name__)

DATA_DIR = Path(Path(__file__).ancestor(3), "data/gbr/")
DEFAULT_SPREADSHEET_FILE = Path(DATA_DIR, 'current')

BPA_ID = "102.100.100"
GBR_DESCRIPTION = 'Great Barrier Reef'


def get_bpa_id(named_tup):
    """ Get a BPA ID object from id string in named tuple.
    :param named_tup: Named tuple with a bpa_id member.
    :type named_tup: tuple
    :rtype BPAUniqueID:
    """
    if bpa_id_utils.is_good_bpa_id(named_tup.bpa_id):
        return bpa_id_utils.get_bpa_id(named_tup.bpa_id, GBR_DESCRIPTION, 'GBR', note='Great Barrier Reef Sample')
    else:
        return None


def get_dna_source(description):
    """
    Get a DNA source if it exists, if it doesn't make it.
    """

    description = str(description).strip().capitalize()
    if description == '':
        logger.debug('Set blank description to unknown')
        description = 'Unknown'

    source, created = DNASource.objects.get_or_create(description=description)
    if created:
        source.note = 'Added by GBR Project'
        source.save()

    return source


def ingest_samples(samples):

    def get_organism(name):
        """
        Set the organism
        """

        try:
            genus, species = name.strip().split()
        except ValueError, e:
            logger.error('Problem Parsing organism from {0} : {1}'.format(name, e))
            return None

        organism, created = Organism.objects.get_or_create(genus=genus, species=species)
        if created:
            logger.info('Adding Organism {0}'.format(name))
            organism.note = 'GBR Related Organism'
            organism.save()
        return organism

    def get_collection_event(entry):
        """
        The site where the sample has been collected from.
        """
        collection_date = ingest_utils.get_date(entry.collection_date)
        collection_event, created = CollectionEvent.objects.get_or_create(
            site_name=entry.collection_site,
            collection_date=collection_date)

        if created:
            collection_event.water_temp = ingest_utils.get_clean_number(entry.water_temp)
            collection_event.ph = ingest_utils.get_clean_number(entry.ph)
            collection_event.depth = entry.depth
            # TODO http://maps.google.com/maps?&z=14&ll=39.211374,-82.978277
            if len(entry.gps_location) > 0:
                print entry.gps_location
                lat, lon = entry.gps_location.split()
                collection_event.lat = float(lat)
                collection_event.lon = float(lon)
            collection_event.note = entry.collection_comment

            # sample collector
            collection_event.collector = user_helper.get_user(
                entry.collector_name,
                entry.contact_email,
                (GBR_DESCRIPTION, ))

            collection_event.save()

        return collection_event

    def add_sample(e):
        """
        Adds new sample or updates existing sample
        """
        from django.db.utils import IntegrityError

        bpa_id = get_bpa_id(e)
        if bpa_id is None:
            logger.warning('BPA ID {0} does not look like a real ID, ignoring'.format(bpa_id))
            return

        try:
            gbr_sample, created = GBRSample.objects.get_or_create(
                bpa_id=bpa_id,
                organism=get_organism(e.species),
                collection_event = get_collection_event(e)
                )
        except IntegrityError, ex:
            logger.error('Failed to ingest sample with BPA ID {0} : {1}'.format(e.bpa_id, ex))
            return


        gbr_sample.name = e.sample_description

        gbr_sample.dna_source = get_dna_source(e.dna_rna_source)
        gbr_sample.dataset = e.dataset
        gbr_sample.dna_extraction_protocol = e.dna_extraction_protocol

        # scientist
        gbr_sample.contact_scientist = user_helper.get_user(
            e.contact_scientist,
            e.contact_email,
            (GBR_DESCRIPTION, e.contact_affiliation))

        # bio informatician
        gbr_sample.contact_bioinformatician_name = user_helper.get_user(
            e.contact_bioinformatician_name,
            e.contact_bioinformatician_email,
            (GBR_DESCRIPTION,))

        gbr_sample.sequencing_notes = e.sequencing_notes
        gbr_sample.dna_rna_concentration = ingest_utils.get_clean_float(e.dna_rna_concentration)
        gbr_sample.total_dna_rna_shipped = ingest_utils.get_clean_float(e.total_dna_rna_shipped)
        gbr_sample.comments_by_facility = e.comments_by_facility
        gbr_sample.date_sequenced = ingest_utils.get_date(e.date_sequenced)
        gbr_sample.requested_read_length = ingest_utils.get_clean_number(e.requested_read_length)
        gbr_sample.date_data_sent = ingest_utils.get_date(e.date_data_sent)

        # facilities
        gbr_sample.sequencing_facility, _ = Facility.objects.get_or_create(name=e.sequencing_facility)
        gbr_sample.note = e.other
        gbr_sample.debug_note = ingest_utils.INGEST_NOTE + ingest_utils.pretty_print_namedtuple(e)


        gbr_sample.save()

        logger.info("Ingested GBR sample {0}".format(gbr_sample.name))

    for sample in samples:
        add_sample(sample)


def get_gbr_sample_data(file_name):
    """
    The data sets is relatively small, so make a in-memory copy to simplify some operations.
    """

    field_spec = [
        ('bpa_id', 'Unique ID', lambda s: s.replace('/', '.')),
        ('species', 'Species', None),
        ('dataset', 'Dataset', None),
        ('sample_description', 'Sample Description', None),
        ('collection_site', 'Site of collection', None),
        ('collection_date', 'Date of collection', None),
        ('collector_name', 'Collector', None),
        ('gps_location', 'GPS Location', None),
        ('water_temp', 'water temp', None),
        ('ph', 'pH', None),
        ('depth', 'Depth (m)', None),
        ('collection_comment', 'Comment (free text)', None),
        ('other', 'Other', None),  # more comments
        ('sequencing_notes', 'Sequencing Notes', None),
        ('contact_scientist', 'contact scientist', None),
        ('contact_affiliation', 'Contact affiliation', None),
        ('contact_email', 'Contact email', None),
        ('dna_rna_source', 'DNA/RNA Source', None),
        ('dna_extraction_protocol', 'DNA extraction protocol', None),
        ('dna_rna_concentration', 'DNA/RNA conc (ng/ul)', None),
        ('total_dna_rna_shipped', 'Total volume of DNA/RNA shipped (uL)', None),
        ('sequencing_facility', 'Genome Sequencing Facility', None),
        ('date_received_by_genome_sequencing_facility', 'Date Received by sequencing facility', None),
        ('comments_by_facility', 'Comments by sequencing facility', None),
        ('date_sequenced', 'Date sequenced', None),
        ('library', 'Library', None),
        ('library_construction', 'Library Construction (insert size bp)', None),
        ('requested_read_length', 'Requested read length (bp)', None),
        ('library_construction_protocol', 'Library construction protocol', None),
        ('index_number', 'Index sequence', None),
        ('sequencer', 'Sequencer', None),
        ('run_number', 'Run number', None),
        ('flow_cell_id', 'Run #:Flow Cell ID', None),
        ('lane_number', 'Lane number', None),
        ('sequence_filename', 'FILE NAMES - supplied by sequencing facility', None),
        ('sequence_filetype', 'file type', None),
        ('md5_checksum', 'MD5 checksum', None),
        ('contact_bioinformatician_name', 'Contact bioinformatician', None),
        ('contact_bioinformatician_email', 'Email contact', None),
        ('date_data_sent', 'Date data sent/transferred', None),
    ]

    wrapper = ExcelWrapper(
        field_spec,
        file_name,
        sheet_name='DNA library Sequencing - Pilot',
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
            if new_str.find('pair') >= 0:
                return 'PE'
            if new_str.find('single') >= 0:
                return 'SE'
            if new_str.find('mate') >= 0:
                return 'MP'
            return 'UN'


        base_pairs = ingest_utils.get_clean_number(entry.requested_read_length)
        library_type = get_library_type(entry.library)
        library_construction_protocol = entry.library_construction_protocol.replace(',', '').capitalize()

        try:
            protocol = GBRProtocol.objects.get(base_pairs=base_pairs,
                                               library_type=library_type,
                                               library_construction_protocol=library_construction_protocol)
        except GBRProtocol.DoesNotExist:
            protocol = GBRProtocol(base_pairs=base_pairs,
                                   library_type=library_type,
                                   library_construction_protocol=library_construction_protocol)
            protocol.library_construction = entry.library_construction
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
            sample = GBRSample.objects.get(bpa_id__bpa_id=bpa_id)
            logger.debug("Found sample {0}".format(sample))
            return sample
        except GBRSample.DoesNotExist:
            logger.error("No sample with ID {0}, quiting now".format(bpa_id))
            sys.exit(1)

    def get_run_number(entry):
        """
        ANU does not have their run numbers entered.
        """

        run_number = ingest_utils.get_clean_number(entry.run_number)
        if run_number is None:
            # see if its ANU and parse the run_number from the filename
            if entry.sequencing_facility.strip() == 'ANU':
                filename = entry.sequence_filename.strip()
                if filename != "":
                    try:
                        run_number = ingest_utils.get_clean_number(filename.split('_')[7])
                        logger.info("ANU run_number {0} parsed from filename".format(run_number))
                    except IndexError:
                        logger.info("Filename {0} wrong format".format(filename))

        return run_number

    def add_run(entry):
        """The run produced several files
        :param entry:
        :type entry: tuple
        """
        flow_cell_id = entry.flow_cell_id.strip()
        bpa_id = get_bpa_id(entry)
        run_number = get_run_number(entry)
        gbr_run, created = GBRRun.objects.get_or_create(
            flow_cell_id=flow_cell_id,
            run_number=run_number,
            sample=get_sample(bpa_id))

        gbr_run.flow_cell_id = flow_cell_id
        gbr_run.run_number = run_number

        gbr_run.index_number = ingest_utils.get_clean_number(entry.index_number)
        gbr_run.sequencer = get_sequencer(entry.sequencer)
        gbr_run.lane_number = ingest_utils.get_clean_number(entry.lane_number)
        gbr_run.protocol = get_protocol(e)
        gbr_run.save()

        # FIXME, I'm sure this is wrong
        gbr_run.protocol.run = gbr_run
        gbr_run.protocol.save()

        return gbr_run

    def add_file(entry, gbr_run):
        """
        Add each sequence file produced by a run
        """

        file_name = entry.sequence_filename.strip()
        if file_name != "":
            f = GBRSequenceFile()
            f.sample = GBRSample.objects.get(bpa_id__bpa_id=entry.bpa_id)
            f.date_received_from_sequencing_facility = ingest_utils.get_date(
                entry.date_received_by_genome_sequencing_facility)
            f.run = gbr_run
            f.index_number = ingest_utils.get_clean_number(entry.index_number)
            f.lane_number = ingest_utils.get_clean_number(entry.lane_number)
            f.filename = file_name
            f.md5 = entry.md5_checksum
            f.note = ingest_utils.pretty_print_namedtuple(entry)
            f.save()

    for e in sample_data:
        sequence_run = add_run(e)
        add_file(e, sequence_run)


def ingest(file_name):
    sample_data = list(get_gbr_sample_data(file_name))
    # pre-populate the BPA ID's
    bpa_id_utils.add_id_set(set([e.bpa_id for e in sample_data]), 'GBR', 'Great Barrier Reef')
    ingest_samples(sample_data)
    ingest_runs(sample_data)

def truncate():
    from django.db import connection

    cursor = connection.cursor()
    cursor.execute('TRUNCATE TABLE "{0}" CASCADE'.format(GBRSample._meta.db_table))
    cursor.execute('TRUNCATE TABLE "{0}" CASCADE'.format(GBRRun._meta.db_table))
    cursor.execute('TRUNCATE TABLE "{0}" CASCADE'.format(GBRProtocol._meta.db_table))


def run(file_name=DEFAULT_SPREADSHEET_FILE):
    """
    Pass parameters like below:
    vpython-bpam manage.py runscript ingest_gbr --script-args Melanoma_study_metadata.xlsx
    """

    truncate()
    ingest(file_name)

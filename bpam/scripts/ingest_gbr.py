# -*- coding: utf-8 -*-

import sys

from apps.common.models import DNASource, Facility, Sequencer
from apps.gbr.models import CollectionSite, Organism, CollectionEvent, GBRSample, GBRRun, GBRProtocol, GBRSequenceFile
from libs import ingest_utils, user_helper
from libs import bpa_id_utils
from libs.logger_utils import get_logger
from libs.excel_wrapper import ExcelWrapper, ColumnNotFoundException
from libs.fetch_data import Fetcher
from unipath import Path
from collections import namedtuple

logger = get_logger(__name__)

BPA_ID = "102.100.100"
PROJECT_ID = "GBR"
PROJECT_DESCRIPTION = "Great Barrier Reef"

# the old google doc format
OLD_METADATA_URL = 'https://downloads.bioplatforms.com/gbr/old_format_metadata/'  # the folder
OLD_METADATA_FILE = 'refuge2020_metadata.xlsx'
OLD_DATA_DIR = Path(ingest_utils.METADATA_ROOT, 'gbr/old_format')

# the newer format
METADATA_URL = 'https://downloads.bioplatforms.com/gbr/metadata/'  # this is where the new metadata is kept
DATA_DIR = Path(ingest_utils.METADATA_ROOT, 'gbr/metadata')


def get_bpa_id(entry):
    """ Get a BPA ID object from id string in named tuple.
    :param named_tup: Named tuple with a bpa_id member.
    :type entry: tuple
    :rtype BPAUniqueID:
    """

    bpa_id, report = bpa_id_utils.get_bpa_id(entry.bpa_id, PROJECT_ID, 'GBR', note='Great Barrier Reef Sample')
    if bpa_id is None:
        logger.warning('Could not add entry in {}, row {}, BPA ID Invalid: {}'.format(entry.file_name, entry.row, report))
        return None
    return bpa_id


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
        """ Get or create and get the organism
        :param name: Name to parse for organism fields.
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

    def get_collection_site(entry):
        """ Get or create and get a collection site
        :param entry: data tuple
        :type entry: tuple
        """
        if entry.gps_location.strip() == '':
            return None

        lat, lon = entry.gps_location.split()
        lat = float(lat)
        lon = float(lon)
        site, created = CollectionSite.objects.get_or_create(lat=lat,
                                                             lon=lon,
                                                             defaults={'site_name': entry.collection_site})

        return site

    def get_collection_event(entry):
        """
        The site where the sample has been collected from.
        """
        collection_date = ingest_utils.get_date(entry.collection_date)
        # sample collector
        collector = user_helper.get_user(
            entry.collector_name,
            entry.contact_email,
            (PROJECT_DESCRIPTION, ))
        collection_event, created = CollectionEvent.objects.get_or_create(
            collection_date=collection_date,
            collector=collector)

        collection_event.site = get_collection_site(entry)
        collection_event.water_temp = ingest_utils.get_clean_number(entry.water_temp)
        collection_event.ph = ingest_utils.get_clean_number(entry.ph)
        collection_event.depth = entry.depth
        collection_event.note = entry.collection_comment
        collection_event.save()

        return collection_event

    def get_protocol(entry):
        """ Get or create and get a GBRProtocol
        :param entry: Data tuple
        :type entry: tuple
        """

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

        base_pairs_string = entry.library_construction
        library_type = get_library_type(entry.library)
        library_construction_protocol = entry.library_construction_protocol.replace(',', '').capitalize()

        protocol, _ = GBRProtocol.objects.get_or_create(
            base_pairs_string=base_pairs_string,
            library_type=library_type,
            library_construction_protocol=library_construction_protocol)

        return protocol

    def add_sample(e):
        """
        Adds new sample or updates existing sample
        """

        bpa_id = get_bpa_id(e)
        if bpa_id is None:
            logger.warning('BPA ID {0} does not look like a real ID, ignoring'.format(bpa_id))
            return

        gbr_sample, created = GBRSample.objects.get_or_create(
            bpa_id=bpa_id,
            defaults={
                'organism': get_organism(e.species),
                'collection_event': get_collection_event(e)
            }
        )

        gbr_sample.protocol = get_protocol(e)
        gbr_sample.name = e.sample_description
        gbr_sample.dna_source = get_dna_source(e.dna_rna_source)
        gbr_sample.dataset = e.dataset
        gbr_sample.dna_extraction_protocol = e.dna_extraction_protocol

        # scientist
        gbr_sample.contact_scientist = user_helper.get_user(
            e.contact_scientist,
            e.contact_email,
            (PROJECT_DESCRIPTION, e.contact_affiliation))

        # bio informatician
        gbr_sample.contact_bioinformatician_name = user_helper.get_user(
            e.contact_bioinformatician_name,
            e.contact_bioinformatician_email,
            (PROJECT_DESCRIPTION,))

        gbr_sample.sequencing_notes = e.sequencing_notes
        gbr_sample.dna_rna_concentration = ingest_utils.get_clean_float(e.dna_rna_concentration)
        gbr_sample.total_dna_rna_shipped = ingest_utils.get_clean_float(e.total_dna_rna_shipped)
        gbr_sample.comments_by_facility = e.comments_by_facility
        gbr_sample.date_sequenced = ingest_utils.get_date(e.date_sequenced)
        gbr_sample.requested_read_length = ingest_utils.get_clean_number(e.requested_read_length)
        gbr_sample.date_data_sent = ingest_utils.get_date(e.date_data_sent)
        gbr_sample.sequencing_facility, _ = Facility.objects.get_or_create(name=e.sequencing_facility)
        gbr_sample.note = e.other
        gbr_sample.debug_note = ingest_utils.INGEST_NOTE + ingest_utils.pretty_print_namedtuple(e)

        gbr_sample.save()

        logger.info("Ingested GBR sample {0}".format(gbr_sample.name))

    for sample in samples:
        add_sample(sample)


def get_gbr_sample_data_old_format(file_name):
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


def get_gbr_sample_data(file_name):
    """
    Parses dample data from GBR metadata file
    :param file_name:
    :return:
    """

    field_spec = [
        ('bpa_id', 'Sample unique ID', lambda s: s.replace('/', '.')),
        ('sequencing_facility', 'Sequencing facility', None),
        ('index_number', 'Index', None),
        ('library', 'Library', None),
        ('library_code', 'Library code', None),  # no need to figure out like with the older format
        ('library_construction', 'Library Construction - average insert size', None),
        ('library_construction_range', 'Insert size range', None),
        ('library_construction_protocol', 'Library construction protocol', None),
        ('sequencer', 'Sequencer', None),
        ('run_number', 'Run number', None),
        ('flow_cell_id', 'Run #:Flow Cell ID', None),
        ('lane_number', 'Lane number', None)]

    wrapper = ExcelWrapper(
        field_spec,
        file_name,
        sheet_name='Sheet1',
        header_length=3,
        column_name_row_index=1)
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

        file_name = entry.sequence_filename.strip().replace("-", "_")
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


def _ingest(sample_data):
    """
    Ingest the sample data
    :param sample_data:
    :return:
    """
    # pre-populate the BPA ID's
    bpa_id_utils.add_id_set(set([e.bpa_id for e in sample_data]), PROJECT_ID, PROJECT_DESCRIPTION) 
    ingest_samples(sample_data)
    ingest_runs(sample_data)


def ingest_old_format(file_name):
    logger.info('Ingesting GBR metadata from {0} (Old google doc)'.format(DATA_DIR))
    sample_data = list(get_gbr_sample_data_old_format(file_name))
    _ingest(sample_data)


def ingest():
    """
    Ingest new format data
    :return:
    """

    def is_metadata(path):
        if path.isfile() and path.ext == '.xlsx':
            return True

    logger.info('Ingesting GBR metadata from {0}'.format(DATA_DIR))
    for metadata_file in DATA_DIR.walk(filter=is_metadata):
        logger.info('Processing GBR Metadata file {0}'.format(metadata_file))
        try:
            sample_data = get_gbr_sample_data(metadata_file)
            _ingest(sample_data)
        except ColumnNotFoundException, e:
            logger.error('File {0} could not be ingested, column name error: {1}'.format(metadata_file, e))


class MD5ParsedLine(object):
    def __init__(self, line):
        self._line = line

        self.bpa_id = None
        self.vendor = None
        self.lib_type = None
        self.lib_size = None
        self.flowcell = None
        self.barcode = None

        self.md5 = None
        self.filename = None

        self._lane = None
        self._read = None

        self._ok = False

        self.__parse_line()

    def is_ok(self):
        return self._ok

    @property
    def lane(self):
        return self._lane

    @lane.setter
    def lane(self, val):
        self._lane = int(val[1:])

    @property
    def read(self):
        return self._read

    @read.setter
    def read(self, val):
        self._read = int(val[1:])

    def __parse_line(self):
        """ unpack the md5 line """
        self.md5, self.filename = self._line.split()

        filename_parts = self.filename.split('.')[0].split('_')
        # [bpaid]_[vendor]_[Library_Type]_[Library_Size]_[FLowcel]_[Barcode]_L[Lane_number]_R[Read_Number].
        # ['14706', 'GBR', 'UNSW', 'PE', '399bp', 'HB049ADXX', 'CGTACG', 'L001', 'R1', '001']
        if len(filename_parts) == 10:
            self.bpa_id, _, self.vendor, self.lib_type, self.lib_size, self.flowcell, self.barcode, self.lane, self.read, _ = filename_parts
            self._ok = True
        elif len(filename_parts) == 11:
            # ['14658', 'GBR', 'UNSW', '16Sa', 'AB50N', 'TAAGGCGA', 'TCGACTAG', 'S1', 'L001', 'I1', '001']
            self.bpa_id, _, self.vendor, self.amplicon, self.flowcell, index1, index2, self.i5index, self.lane, self.read, _ = filename_parts
            self.index = index1 + '-' + index2
            self._ok = True
        elif len(filename_parts) == 8:
            # ['13208', 'GBR', 'UNSW', 'H8P31ADXX', 'TCCTGAGC', 'L002', 'R2', '001']
            print("whaaaat")
            print(filename_parts)
            self.bpa_id, _, self.vendor,  self.flowcell, self.index, self.lane, self.read, _ = filename_parts
            self._ok = True
        else:
            print("XXXX")
            print(filename_parts)
            self._ok = False



def parse_md5_file(md5_file):
    """
    Parse md5 file
    """

    data = []

    with open(md5_file) as f:
        for line in f.read().splitlines():
            line = line.strip()
            if line == '':
                continue

            parsed_line = MD5ParsedLine(line)
            if parsed_line.is_ok():
                data.append(parsed_line)

    return data

def add_md5(md5_lines):
    """
    Add md5 data
    """

    for md5_line in md5_lines:
        bpa_idx = md5_line.bpa_id
        bpa_id, report = bpa_id_utils.get_bpa_id(bpa_idx, PROJECT_ID, PROJECT_DESCRIPTION, add_prefix=True)
        print(bpa_id)

        if bpa_id is None:
            continue

        f = GBRSequenceFile()
        sample, created = GBRSample.objects.get_or_create(bpa_id=bpa_id)
        f.sample = sample
        f.flowcell = md5_line.flowcell
        f.barcode = md5_line.barcode
        f.read_number = md5_line.read
        f.lane_number = md5_line.lane

        f.filename = md5_line.filename
        f.md5 = md5_line.md5
        f.save()


def ingest_md5():
    """
    Ingest the md5 files
    """

    def is_md5file(path):
        if path.isfile() and path.ext == '.md5':
            return True

    logger.info('Ingesting GBR md5 file information from {0}'.format(DATA_DIR))
    for md5_file in DATA_DIR.walk(filter=is_md5file):
        logger.info('Processing GBR md5 file {0}'.format(md5_file))
        data = parse_md5_file(md5_file)
        add_md5(data)

def truncate():
    from django.db import connection

    cursor = connection.cursor()
    cursor.execute('TRUNCATE TABLE "{0}" CASCADE'.format(GBRSample._meta.db_table))
    cursor.execute('TRUNCATE TABLE "{0}" CASCADE'.format(GBRRun._meta.db_table))
    cursor.execute('TRUNCATE TABLE "{0}" CASCADE'.format(GBRProtocol._meta.db_table))
    cursor.execute('TRUNCATE TABLE "{0}" CASCADE'.format(CollectionEvent._meta.db_table))
    cursor.execute('TRUNCATE TABLE "{0}" CASCADE'.format(CollectionSite._meta.db_table))


def run():
    # fetch the old data file
    fetcher = Fetcher(OLD_DATA_DIR, OLD_METADATA_URL, auth=('bpa', 'gbr33f'))
    fetcher.fetch(OLD_METADATA_FILE)

    # fetch the new data formats
    fetcher = Fetcher(DATA_DIR, METADATA_URL, auth=('bpa', 'gbr33f'))
    #fetcher.clean()
    #fetcher.fetch_metadata_from_folder()

    truncate()

    ingest_old_format(Path(OLD_DATA_DIR, OLD_METADATA_FILE))

    ingest_md5()

    ingest()

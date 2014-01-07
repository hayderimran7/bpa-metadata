import sys
from datetime import datetime
import logging
import pprint

import xlrd
from unipath import Path

from apps.common.models import DNASource, Facility, BPAUniqueID, Sequencer
from apps.gbr.models import Organism, CollectionEvent, GBRSample, GBRRun, GBRProtocol, GBRSequenceFile
from libs import ingest_utils, user_helper
from libs import bpa_id_utils


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('GBR')

DATA_DIR = Path(Path(__file__).ancestor(3), "data/gbr/")
DEFAULT_SPREADSHEET_FILE = Path(DATA_DIR, 'current')

BPA_ID = "102.100.100"
GBR_DESCRIPTION = 'Great Barrier Reef'


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
        source.note = 'Added by GBR Project'
        source.save()

    return source


def ingest_samples(samples):
    def get_facility(name):
        """
        Return the sequencing facility with this name, or a new facility.
        """
        if name.strip() == '':
            name = 'Unknown'
        try:
            facility = Facility.objects.get(name=name)
        except Facility.DoesNotExist:
            facility = Facility(name=name)
            facility.save()

        return facility

    def get_organism(name):
        """
        Set the organism
        """
        genus, species = name.strip().split()

        try:
            organism = Organism.objects.get(genus=genus, species=species)
        except Organism.DoesNotExist:
            logger.debug('Adding Organism ' + name)
            organism = Organism()
            organism.genus = genus
            organism.species = species
            organism.note = 'GBR Related Organism'
            organism.save()
        return organism

    def get_collection_event(entry):
        """
        The site where the sample has been collected from.
        """
        collection_date = ingest_utils.get_date(entry['collection_date'])
        try:
            collection_event = CollectionEvent.objects.get(
                name=entry['collection_site'],
                collection_date=collection_date)
        except CollectionEvent.DoesNotExist:
            collection_event = CollectionEvent()
            collection_event.name = entry['collection_site']
            collection_event.collection_date = collection_date

            collection_event.water_temp = ingest_utils.get_clean_number(entry['water_temp'])
            collection_event.ph = ingest_utils.get_clean_number(entry['ph'])
            collection_event.depth = ingest_utils.get_clean_number(entry['depth'])
            collection_event.gps_location = entry['gps_location']
            collection_event.note = entry['collection_comment']

            # sample collector
            collection_event.collector = user_helper.get_user(
                entry['collector_name'],
                entry['contact_email'],
                (GBR_DESCRIPTION, ))

            collection_event.save()

        return collection_event

    def add_sample(e):
        """
        Adds new sample or updates existing sample
        """

        bpa_id = e['bpa_id']

        if not bpa_id_utils.is_good_bpa_id(bpa_id):
            logger.warning('BPA ID {0} does not look like a real ID, ignoring'.format(bpa_id))
            return

        try:
            # Test if sample already exists
            gbr_sample = GBRSample.objects.get(bpa_id__bpa_id=bpa_id)
        except GBRSample.DoesNotExist:
            gbr_sample = GBRSample()
            gbr_sample.bpa_id = BPAUniqueID.objects.get(bpa_id=bpa_id)

        gbr_sample.name = e['sample_name']
        gbr_sample.requested_sequence_coverage = e['requested_sequence_coverage'].upper()
        gbr_sample.organism = get_organism(e['species'])
        gbr_sample.dna_source = get_dna_source(e['sample_dna_source'])
        gbr_sample.dna_extraction_protocol = e['dna_extraction_protocol']
        gbr_sample.dna_concentration = ingest_utils.get_clean_number(e['dna_concentration'])
        gbr_sample.total_dna = ingest_utils.get_clean_number(e['total_dna'])

        # scientist
        gbr_sample.contact_scientist = user_helper.get_user(
            e['contact_scientist'],
            e['contact_email'],
            (GBR_DESCRIPTION, e['contact_affiliation']))

        # bio informatician
        gbr_sample.contact_bioinformatician_name = user_helper.get_user(
            e['contact_bioinformatician_name'],
            e['contact_bioinformatician_email'],
            (GBR_DESCRIPTION,))

        gbr_sample.requested_sequence_coverage = e['requested_sequence_coverage']
        gbr_sample.sequencing_notes = e['sequencing_notes']
        gbr_sample.dna_rna_concentration = ingest_utils.get_clean_number(e['dna_rna_concentration'])
        gbr_sample.total_dna_rna_shipped = ingest_utils.get_clean_number(e['total_dna_rna_shipped'])
        gbr_sample.comments_by_facility = e['comments_by_facility']
        gbr_sample.sequencing_data_eta = ingest_utils.get_date(e['sequencing_data_eta'])
        gbr_sample.date_sequenced = ingest_utils.get_date(e['date_sequenced'])
        gbr_sample.requested_read_length = ingest_utils.get_clean_number(e['requested_read_length'])
        gbr_sample.date_data_sent = ingest_utils.get_date(e['date_data_sent'])
        gbr_sample.date_data_received = ingest_utils.get_date(e['date_data_received'])

        # facilities
        gbr_sample.sequencing_facility = get_facility(e['sequencing_facility'])
        gbr_sample.note = e['other']
        gbr_sample.debug_note = ingest_utils.INGEST_NOTE + pprint.pformat(e)

        gbr_sample.collection_event = get_collection_event(e)
        gbr_sample.save()

        logger.info("Ingested GBR sample {0}".format(gbr_sample.name))

    for sample in samples:
        add_sample(sample)


def get_gbr_sample_data(spreadsheet_file):
    """
    The data sets is relatively small, so make a in-memory copy to simplify some operations.
    """

    fieldnames = ['bpa_id',
                  'species',
                  'dataset',
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

        if not bpa_id_utils.is_good_bpa_id(vals[0]):
            logger.warning('BPA ID {0} does not look like a real ID, ignoring'.format(vals[0]))
            continue

        # for date types try to convert to python dates
        types = sheet.row_types(row_idx)
        for i, t in enumerate(types):
            if t == xlrd.XL_CELL_DATE:
                vals[i] = datetime(*xlrd.xldate_as_tuple(vals[i], wb.datemode))

        samples.append(dict(zip(fieldnames, vals)))

    return samples


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

        base_pairs = ingest_utils.get_clean_number(entry['library_construction'])
        library_type = get_library_type(entry['library'])
        library_construction_protocol = entry['library_construction_protocol'].replace(',', '').capitalize()

        try:
            protocol = GBRProtocol.objects.get(base_pairs=base_pairs,
                                               library_type=library_type,
                                               library_construction_protocol=library_construction_protocol)
        except GBRProtocol.DoesNotExist:
            protocol = GBRProtocol(base_pairs=base_pairs,
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

        run_number = ingest_utils.get_clean_number(entry['run_number'])
        if run_number is None:
            # see if its ANU and parse the run_number from the filename
            if entry['sequencing_facility'].strip() == 'ANU':
                filename = entry['sequence_filename'].strip()
                if filename != "":
                    try:
                        run_number = ingest_utils.get_clean_number(filename.split('_')[7])
                        logger.info("ANU run_number {0} parsed from filename".format(run_number))
                    except IndexError:
                        logger.info("Filename {0} wrong format".format(filename))

        return run_number

    def add_run(entry):
        """
        The run produced several files
        """
        flow_cell_id = entry['flow_cell_id'].strip()
        bpa_id = entry['bpa_id'].strip()
        run_number = get_run_number(entry)

        try:
            gbr_run = GBRRun.objects.get(flow_cell_id=flow_cell_id,
                                         run_number=run_number,
                                         sample__bpa_id__bpa_id=bpa_id)
        except GBRRun.DoesNotExist:
            gbr_run = GBRRun()

        gbr_run.flow_cell_id = flow_cell_id
        gbr_run.run_number = run_number
        gbr_run.sample = get_sample(bpa_id)
        gbr_run.index_number = ingest_utils.get_clean_number(entry['index_number'])
        gbr_run.sequencer = get_sequencer(entry['sequencer'])
        gbr_run.lane_number = ingest_utils.get_clean_number(entry['lane_number'])
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

        file_name = entry['sequence_filename'].strip()
        if file_name != "":
            f = GBRSequenceFile()
            f.sample = GBRSample.objects.get(bpa_id__bpa_id=entry['bpa_id'])
            f.date_received_from_sequencing_facility = ingest_utils.get_date(entry['date_received'])
            f.run = gbr_run
            f.index_number = ingest_utils.get_clean_number(entry['index_number'])
            f.lane_number = ingest_utils.get_clean_number(entry['lane_number'])
            f.filename = file_name
            f.md5 = entry['md5_checksum']
            f.note = pprint.pformat(entry)
            f.save()

    for e in sample_data:
        sequence_run = add_run(e)
        add_file(e, sequence_run)


def ingest_gbr(spreadsheet_file):
    sample_data = get_gbr_sample_data(spreadsheet_file)
    bpa_id_utils.ingest_bpa_ids(sample_data, 'GBR')
    ingest_samples(sample_data)
    ingest_runs(sample_data)


def run(spreadsheet_file=DEFAULT_SPREADSHEET_FILE):
    """
    Pass parameters like below:
    vpython-bpam manage.py runscript ingest_gbr --script-args Melanoma_study_metadata.xlsx
    """

    ingest_gbr(spreadsheet_file)

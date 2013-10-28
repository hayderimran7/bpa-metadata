import sys
import pprint
from datetime import datetime

import xlrd
from unipath import Path

from apps.bpaauth.models import BPAUser
from apps.common.models import *
from apps.gbr.models import *
from .utils import *
import user_helper

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)

DATA_DIR = Path(Path(__file__).ancestor(3), "data/gbr/")
DEFAULT_SPREADSHEET_FILE = Path(DATA_DIR, 'BPA_ReFuGe2020_METADATA.xlsx')

BPA_ID = "102.100.100"
GBR = 'Great Barrier Reef'


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


def ingest_samples(samples):
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
            organism.note = 'GBR'
            organism.save()
        return organism

    def get_collection_event(entry):
        """
        The site where the sample has been collected from.
        """
        collection_date = check_date(entry['collection_date'])
        try:
            collection_event = CollectionEvent.objects.get(
                name=entry['collection_site'],
                collection_date=collection_date)
        except CollectionEvent.DoesNotExist:
            collection_event = CollectionEvent()
            collection_event.name = entry['collection_site']
            collection_event.collection_date = collection_date

        collection_event.water_temp = get_clean_number(entry['water_temp'])
        collection_event.ph = get_clean_number(entry['ph'])
        collection_event.depth = get_clean_number(entry['depth'])
        # site.gps_location = smart_text(e['gps_location'])
        # site.note = entry['gps_location'] # FIXME

         # sample collector
        collection_event.collector = user_helper.get_user(
            entry['collector_name'],
            entry['contact_email'],
            (GBR, ))

        collection_event.save()

        return collection_event

    def add_sample(e):
        """
        Adds new sample or updates existing sample
        """

        bpa_id = e['bpa_id']

        if not is_bpa_id(bpa_id):
            logger.warning('BPA ID {0} does not look like a real ID, ignoring'.format(bpa_id))
            return

        try:
            # Test if sample already exists
            sample = GBRSample.objects.get(bpa_id__bpa_id=bpa_id)
        except GBRSample.DoesNotExist:
            sample = GBRSample()
            sample.bpa_id = BPAUniqueID.objects.get(bpa_id=bpa_id)

        sample.name = e['sample_name']
        sample.requested_sequence_coverage = e['requested_sequence_coverage'].upper()
        sample.organism = get_organism(e['species'])
        sample.dna_source = get_dna_source(e['sample_dna_source'])
        sample.dna_extraction_protocol = e['dna_extraction_protocol']
        sample.dna_concentration = get_clean_number(e['dna_concentration'])
        sample.total_dna = get_clean_number(e['total_dna'])


        # scientist
        sample.contact_scientist = user_helper.get_user(
            e['contact_scientist'],
            e['contact_email'],
            (GBR, e['contact_affiliation']))

        # bioinformatician
        sample.contact_bioinformatician_name = user_helper.get_user(
            e['contact_bioinformatician_name'],
            e['contact_bioinformatician_email'],
            (GBR,))

        sample.requested_sequence_coverage = e['requested_sequence_coverage']
        sample.sequencing_notes = e['sequencing_notes']
        sample.dna_rna_concentration = get_clean_number(e['dna_rna_concentration'])
        sample.total_dna_rna_shipped = get_clean_number(e['total_dna_rna_shipped'])
        sample.comments_by_facility = e['comments_by_facility']
        sample.sequencing_data_eta = check_date(e['sequencing_data_eta'])
        sample.date_sequenced = check_date(e['date_sequenced'])
        sample.requested_read_length = get_clean_number(e['requested_read_length'])
        sample.date_data_sent = check_date(e['date_data_sent'])
        sample.date_data_received = check_date(e['date_data_received'])

        # facilities
        sample.sequencing_facility = get_facility(e['sequencing_facility'])
        sample.note = e['other']
        sample.debug_note = INGEST_NOTE + pprint.pformat(e)

        sample.collection_event = get_collection_event(e)
        sample.save()

        logger.info("Ingested GBR sample {0}".format(sample.name))

    for sample in samples:
        add_sample(sample)


def get_gbr_sample_data(spreadsheet_file):
    """
    The data sets is relatively small, so make a in-memory copy to simplify some operations.
    """

    fieldnames = ['bpa_id',
                  'species',
                  'dataset', # NEW (model?)
                  'sample_name',
                  'dna_concentration', # NEW
                  'total_dna', # NEW
                  'collection_site', # NEW (model?)
                  'collection_date',
                  'collector_name',  # NEW
                  'gps_location',  # NEW
                  'water_temp',  # NEW
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
                  'dna_rna_concentration', # NEW
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
                  'contact_bioinformatician_email', # NEW
                  'date_data_sent', # NEW
                  'date_data_received', # NEW
    ]

    wb = xlrd.open_workbook(spreadsheet_file)
    sheet = wb.sheet_by_name('DNA library Sequencing - Pilot')
    samples = []
    for row_idx in range(sheet.nrows)[2:]:  # the first two lines are headers
        vals = sheet.row_values(row_idx)

        if not is_bpa_id(vals[0]):
            logger.warning('BPA ID {0} does not look like a real ID, ignoring'.format(vals[0]))
            continue

        # for date types try to convert to python dates
        types = sheet.row_types(row_idx)
        for i, t in enumerate(types):
            if t == xlrd.XL_CELL_DATE:
                vals[i] = datetime(*xldate_as_tuple(vals[i], wb.datemode))

        samples.append(dict(zip(fieldnames, vals)))

    print("debug sample print")
    for field in fieldnames:
        print "%44s: %s" % (field, samples[0][field])

    return samples


def ingest_runs(sample_data):
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

    def get_run_number(e):
        """
        ANU does not have their run numbers entered.
        """

        run_number = get_clean_number(e['run_number'])
        if run_number is None:
            # see if its ANU and parse the run_number from the filename
            if e['sequencing_facility'].strip() == 'ANU':
                filename = e['sequence_filename'].strip()
                if filename != "":
                    try:
                        run_number = get_clean_number(filename.split('_')[7])
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
            run = GBRRun.objects.get(flow_cell_id=flow_cell_id,
                                     run_number=run_number,
                                     sample__bpa_id__bpa_id=bpa_id)
        except GBRRun.DoesNotExist:
            run = GBRRun()
            run.flow_cell_id = flow_cell_id
            run.run_number = run_number
            run.sample = get_sample(bpa_id)
            run.index_number = get_clean_number(entry['index_number'])
            run.sequencer = get_sequencer(entry['sequencer'])
            run.lane_number = get_clean_number(entry['lane_number'])
            run.protocol = get_protocol(e)
            run.save()

        return run

    def add_file(e, run):
        """
        Add each sequence file produced by a run
        """

        file_name = e['sequence_filename'].strip()
        if file_name != "":
            f = GBRSequenceFile()
            f.sample = GBRSample.objects.get(bpa_id__bpa_id=e['bpa_id'])
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


def ingest_gbr(spreadsheet_file):
    sample_data = get_gbr_sample_data(spreadsheet_file)
    ingest_bpa_ids(sample_data, 'GBR')
    ingest_samples(sample_data)
    ingest_runs(sample_data)


def run(spreadsheet_file=DEFAULT_SPREADSHEET_FILE):
    """
    Pass parameters like below:
    vpython-bpam manage.py runscript ingest_gbr --script-args Melanoma_study_metadata.xlsx
    """

    ingest_gbr(spreadsheet_file)

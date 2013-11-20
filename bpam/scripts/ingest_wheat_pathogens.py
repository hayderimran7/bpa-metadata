import sys
import pprint
from datetime import datetime
import logging

import xlrd
from unipath import Path

from apps.common.models import *
from apps.wheat_pathogens.models import *
import utils
import user_helper


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('WheatPathogens')


DATA_DIR = Path(Path(__file__).ancestor(3), "data/wheat_pathogens/")
DEFAULT_SPREADSHEET_FILE = Path(DATA_DIR, 'Wheat_pathogens_genomic_metadata.xlsx')

BPA_ID = "102.100.100"
DESCRIPTION = 'Wheat Pathogens'


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
        source.note = 'Added by Pathogens Project'
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

    def get_organism(kingdom, phylum, species):
        """
        Set the organism
        """
        genus, species = species.strip().split()

        try:
            organism = Organism.objects.get(kingdom=kingdom, phylum=phylum, genus=genus, species=species)
        except Organism.DoesNotExist:
            logger.debug('Adding Organism {0} {1} {2} {3}'.format(kingdom, phylum, genus, species))
            organism = Organism()
            organism.kingdom = kingdom
            organism.phylum = phylum
            organism.genus = genus
            organism.species = species
            organism.note = 'Wheat Pathogens Related Organism'
            organism.save()
        return organism

    def add_sample(e):
        """
        Adds new sample or updates existing sample
        """

        bpa_id = e['bpa_id']

        if not utils.is_bpa_id(bpa_id):
            logger.warning('BPA ID {0} does not look like a real ID, ignoring'.format(bpa_id))
            return

        try:
            # Test if sample already exists
            pathogen_sample = PathogenSample.objects.get(bpa_id__bpa_id=bpa_id)
        except PathogenSample.DoesNotExist:
            pathogen_sample = PathogenSample()
            pathogen_sample.bpa_id = BPAUniqueID.objects.get(bpa_id=bpa_id)

        pathogen_sample.name = e['sample_id']
        pathogen_sample.sample_label = e['other_id']
        pathogen_sample.organism = get_organism(e['kingdom'], e['phylum'], e['species'])
        pathogen_sample.dna_source = get_dna_source(e['sample_dna_source'])
        pathogen_sample.official_variety_name = e['official_variety']
        pathogen_sample.original_source_host_species = e['original_source_host_species']

        # scientist
        pathogen_sample.contact_scientist = user_helper.get_user(
            e['contact_scientist'],
            '',
            (DESCRIPTION, ''))

        # collection
        pathogen_sample.collection_date = utils.check_date(e['collection_date'])
        pathogen_sample.collection_location = e['collection_location']
        pathogen_sample.dna_extraction_protocol = e['dna_extraction_protocol']

        # facilities
        pathogen_sample.sequencing_facility = get_facility('AGRF')
        pathogen_sample.note = e['note']
        pathogen_sample.debug_note = utils.INGEST_NOTE + pprint.pformat(e)

        pathogen_sample.save()
        logger.info("Ingested Pathogens sample {0}".format(pathogen_sample.name))

    for sample in samples:
        add_sample(sample)


def get_pathogen_sample_data(spreadsheet_file):
    """
    The data sets is relatively small, so make a in-memory copy to simplify some operations.
    """

    fieldnames = ['bpa_id',
                  'official_variety',
                  'kingdom',
                  'phylum',
                  'species',
                  'sample_id',
                  'other_id',
                  'original_source_host_species',
                  'collection_date',
                  'collection_location',
                  'wheat_pathogenicity',
                  'contact_scientist',
                  'sample_dna_source',
                  'dna_extraction_protocol',
                  'library',
                  'library_construction',
                  'library_construction_protocol',
                  'sequencer',
                  'sample_label',
                  'library_id',
                  'index_number',
                  'index_sequence',
                  'run_number',
                  'flow_cell_id',
                  'lane_number',
                  'qc_software', # empty
                  'sequence_filename',
                  'sequence_filetype',
                  'md5_checksum',
                  'reported_file_size',
                  'analysis_performed',
                  'genbank_project',
                  'locus_tag',
                  'note'
    ]

    wb = xlrd.open_workbook(spreadsheet_file)
    sheet = wb.sheet_by_name('Metadata')
    samples = []
    for row_idx in range(sheet.nrows)[2:]:  # the first two lines are headers
        vals = sheet.row_values(row_idx)

        if not utils.is_bpa_id(vals[0]):
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

        base_pairs = utils.get_clean_number(entry['library_construction'])
        library_type = get_library_type(entry['library'])
        library_construction_protocol = entry['library_construction_protocol'].replace(',', '').capitalize()

        try:
            protocol = PathogenProtocol.objects.get(base_pairs=base_pairs,
                                                    library_type=library_type,
                                                    library_construction_protocol=library_construction_protocol)
        except PathogenProtocol.DoesNotExist:
            protocol = PathogenProtocol(base_pairs=base_pairs,
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
            sample = PathogenSample.objects.get(bpa_id__bpa_id=bpa_id)
            logger.debug("Found sample {0}".format(sample))
            return sample
        except PathogenSample.DoesNotExist:
            logger.error("No sample with ID {0}, quiting now".format(bpa_id))
            sys.exit(1)

    def get_run_number(entry):
        run_number = utils.get_clean_number(entry['run_number'].replace('RUN #', ''))
        return run_number

    def add_run(entry):
        """
        The run produced several files
        """
        flow_cell_id = entry['flow_cell_id'].strip()
        bpa_id = entry['bpa_id'].strip()
        run_number = get_run_number(entry)

        try:
            pathogen_run = PathogenRun.objects.get(flow_cell_id=flow_cell_id,
                                                   run_number=run_number,
                                                   sample__bpa_id__bpa_id=bpa_id)
        except PathogenRun.DoesNotExist:
            pathogen_run = PathogenRun()
            pathogen_run.flow_cell_id = flow_cell_id
            pathogen_run.run_number = run_number
            pathogen_run.sample = get_sample(bpa_id)
            pathogen_run.index_number = utils.get_clean_number(entry['index_number'])
            pathogen_run.sequencer = get_sequencer(entry['sequencer'])
            pathogen_run.lane_number = utils.get_clean_number(entry['lane_number'])
            pathogen_run.protocol = get_protocol(e)
            pathogen_run.save()

        return pathogen_run

    def add_file(entry, pathogen_run):
        """
        Add each sequence file produced by a run
        """

        file_name = entry['sequence_filename'].strip()
        if file_name != "":
            f = PathogenSequenceFile()
            f.sample = PathogenSample.objects.get(bpa_id__bpa_id=entry['bpa_id'])
            f.run = pathogen_run
            f.index_number = utils.get_clean_number(entry['index_number'])
            f.lane_number = utils.get_clean_number(entry['lane_number'])
            f.filename = file_name
            f.md5 = entry['md5_checksum']
            f.note = pprint.pformat(entry)
            f.save()

    for e in sample_data:
        sequence_run = add_run(e)
        add_file(e, sequence_run)


def ingest(spreadsheet_file):
    sample_data = get_pathogen_sample_data(spreadsheet_file)
    utils.ingest_bpa_ids(sample_data, 'Wheat Pathogens')
    ingest_samples(sample_data)
    ingest_runs(sample_data)


def run(spreadsheet_file=DEFAULT_SPREADSHEET_FILE):
    """
    Pass parameters like below:
    vpython-bpam manage.py runscript ingest_gbr --script-args Wheat_pathogens_genomic_metadata.xlsx
    """

    ingest(spreadsheet_file)

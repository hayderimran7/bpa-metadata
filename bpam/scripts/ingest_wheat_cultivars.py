# -*- coding: utf-8 -*-

import os
from apps.common.models import DNASource, Sequencer
from apps.wheat_cultivars.models import Organism, CultivarProtocol, CultivarSample, CultivarRun, CultivarSequenceFile
from libs import ingest_utils
from libs import bpa_id_utils
from libs.logger_utils import get_logger
from libs.excel_wrapper import ExcelWrapper


logger = get_logger(__name__)

BPA_ID = "102.100.100"
DESCRIPTION = 'Wheat Cultivars'
METADATA_URL = "https://downloads.bioplatforms.com/wheat_cultivars/metadata/current.xlsx"
SOURCE_FILE = os.path.join(ingest_utils.METADATA_ROOT, 'wheat_cultivars/current.xlsx')


def get_dna_source(description):
    """
    Get a DNA source if it exists, if it doesn't make it.
    """

    description = description.strip().capitalize()
    if description == '':
        logger.debug('Set blank description to unknown')
        description = 'Unknown'

    source, created = DNASource.objects.get_or_create(description=description)
    if created:
        source.note = 'Added by Wheat Cultivars Project'
        source.save()

    return source


def get_bpa_id(e):
    """
    Get or make BPA ID
    """
    idx = e.bpa_id
    bpa_id = bpa_id_utils.get_bpa_id(idx, 'WHEAT_CULTIVAR', 'Wheat Cultivars')
    if not bpa_id:
        logger.warning('Ignoring {0}, not a good BPA ID'.format(idx))
        return None
    return bpa_id


def ingest_samples(samples):
    """
    Add all the cultivar samples
    """
    def add_sample(e):
        """
        Adds new sample or updates existing sample
        """

        bpa_id = get_bpa_id(e)
        wheat_organism, _ = Organism.objects.get_or_create(genus='Triticum', species='Aestivum')
        cultivar_sample, created = CultivarSample.objects.get_or_create(bpa_id=bpa_id, organism=wheat_organism)

        cultivar_sample.organism = wheat_organism
        cultivar_sample.name = e.variety
        cultivar_sample.cultivar_code = e.cultivar_code
        cultivar_sample.extract_name = e.extract_name
        cultivar_sample.casava_version = e.casava_version
        cultivar_sample.debug_note = ingest_utils.INGEST_NOTE + ingest_utils.pretty_print_namedtuple(e)
        cultivar_sample.save()
        logger.info("Ingested Cultivars sample {0}".format(cultivar_sample.name))

    for sample in samples:
        add_sample(sample)


def get_cultivar_sample_data(file_name):
    """
    The data sets is relatively small, so make a in-memory copy to simplify some operations.
    """

    field_spec = [('bpa_id', 'Unique ID', lambda s: s.replace('/', '.')),
                  ('variety', 'Variety', None),
                  ('cultivar_code', 'Comment[Sample code]', None),  # C
                  ('library', 'Parameter Value[library layout]', None),
                  ('library_construction', 'Parameter Value[library nominal fragment size]', ingest_utils.get_clean_number),
                  ('index', 'Parameter Value[index]', None),
                  ('extract_name', 'Extract Name', None),
                  ('cycle_count', 'Parameter Value[Cycle count]', ingest_utils.get_clean_number),
                  ('sequencer', 'Parameter Value[sequencing instrument]', None),
                  ('casava_version', 'Parameter Value[CASAVA version]', None),
                  ('run_number', 'Parameter Value[run number]', ingest_utils.get_clean_number),
                  ('flow_cell_id', 'Parameter Value[flow cell identifier]', None),
                  ('lane_number', 'Parameter Value[lane number]', ingest_utils.get_clean_number),
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

        base_pairs = entry.library_construction
        print("XXXXXXXXXXXX" + str(base_pairs))
        library_type = get_library_type(entry.library)
        protocol, created = CultivarProtocol.objects.get_or_create(base_pairs=base_pairs,
                                                                   library_type=library_type,
                                                                   library_construction_protocol='Illumina Sequencing Protocol')
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
        wheat_organism, _ = Organism.objects.get_or_create(genus='Triticum', species='Aestivum')
        sample, created = CultivarSample.objects.get_or_create(bpa_id__bpa_id=bpa_id, organism=wheat_organism)
        if created:
            logger.info("New sample with ID {0}".format(bpa_id))
        return sample

    def add_run(entry):
        """
        The run produced several files
        """
        flow_cell_id = entry.flow_cell_id.strip()
        bpa_id = get_bpa_id(e)
        run_number = entry.run_number
        sample = get_sample(bpa_id)

        cultivar_run, _ = CultivarRun.objects.get_or_create(
            flow_cell_id=flow_cell_id,
            run_number=run_number,
            sample=sample)

        # just update
        cultivar_run.flow_cell_id = flow_cell_id
        cultivar_run.run_number = run_number
        cultivar_run.index_number = ingest_utils.get_clean_number(entry.index)
        cultivar_run.sequencer = get_sequencer(entry.sequencer)
        cultivar_run.lane_number = ingest_utils.get_clean_number(entry.lane_number)
        cultivar_run.protocol = get_protocol(e)
        cultivar_run.save()

        # FIXME, I'm sure this is wrong
        cultivar_run.protocol.run = cultivar_run
        cultivar_run.protocol.save()

        return cultivar_run

    def add_file(entry, run):
        """
        Add each sequence file produced by a run
        """

        # Use the corrected sequence filename, as for this project (Wheat Cultivars),
        # that's what the user wants to see
        file_name = entry.corrected_sequence_filename.strip()
        if file_name != "":
            f = CultivarSequenceFile()
            f.sample = CultivarSample.objects.get(bpa_id__bpa_id=entry.bpa_id)
            f.run = run
            f.index_number = ingest_utils.get_clean_number(entry.index)
            f.lane_number = ingest_utils.get_clean_number(entry.lane_number)
            f.filename = file_name
            f.original_sequence_filename = entry.sequence_filename
            f.md5 = entry.md5_checksum
            f.note = ingest_utils.pretty_print_namedtuple(entry)
            f.save()

    for e in sample_data:
        run = add_run(e)
        add_file(e, run)


def truncate():
    from django.db import connection

    cursor = connection.cursor()
    cursor.execute('TRUNCATE TABLE "{0}" CASCADE'.format(CultivarSample._meta.db_table))
    cursor.execute('TRUNCATE TABLE "{0}" CASCADE'.format(CultivarRun._meta.db_table))
    cursor.execute('TRUNCATE TABLE "{0}" CASCADE'.format(CultivarProtocol._meta.db_table))
    cursor.execute('TRUNCATE TABLE "{0}" CASCADE'.format(CultivarSequenceFile._meta.db_table))


def ingest(file_name):
    logger.info('Starting Wheat Cultivar metadata import')
    sample_data = list(get_cultivar_sample_data(file_name))
    bpa_id_utils.ingest_bpa_ids(sample_data, 'WHEAT_CULTIVAR', 'Wheat Cultivars')
    ingest_samples(sample_data)
    ingest_runs(sample_data)
    logger.info('Wheat Cultivar metadata import complete')


def run(file_name=SOURCE_FILE):
    """
    Pass parameters like below:
    vpython-bpam manage.py runscript ingest_wheat_pathogens_transcript --script-args current.xlsx
    """
    truncate()
    ingest_utils.fetch_metadata(METADATA_URL, file_name)
    ingest(file_name)

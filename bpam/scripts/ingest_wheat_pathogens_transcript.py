# -*- coding: utf-8 -*-

import os
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

BPA_ID = "102.100.100"
DESCRIPTION = 'Wheat Pathogens Transcript'
METADATA_URL = "https://downloads.bioplatforms.com/wheat_pathogens_transcript/metadata/Wheat_Pathogen_Transcript_data.xlsx"
SOURCE_FILE = os.path.join(ingest_utils.METADATA_ROOT, 'wheat_pathogens_transcript/wheat_pathogens_transcript.xlsx')


def ingest_samples(samples):
    def get_dna_source(description):
        """
        Get a DNA source if it exists, if it doesn't make it.
        """
        source, _ = DNASource.objects.get_or_create(description=description.capitalize())
        return source

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
        pathogen_sample.contact_scientist = user_helper.get_user(
            e.contact_name,
            e.email,
            (DESCRIPTION, e.institution))

        pathogen_sample.dna_source = get_dna_source(e.rna_source)
        pathogen_sample.institution = e.institution
        pathogen_sample.species = e.species
        pathogen_sample.sample_type = e.sample_type
        pathogen_sample.extraction_method = e.extraction_method
        pathogen_sample.growth_protocol = e.growth_protocol
        pathogen_sample.note = e.additional_information
        pathogen_sample.save()

        logger.info("Ingested Wheat Pathogens Transcript sample {0}".format(pathogen_sample.name))

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

    def add_run(entry):
        """
        The run produced several files
        """
        flow_cell_id = entry.flow_cell_id.strip()

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
            run_number=entry.run_number,
            sample=pathogen_sample,
            sequencer=get_sequencer(entry.sequencer))

        # always update
        pathogen_run.flow_cell_id = flow_cell_id
        pathogen_run.run_number = entry.run_number
        pathogen_run.sample = get_sample(bpa_id)
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
            f.lane_number = entry.lane_number
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
                  ('index_sequence', 'Index', None),
                  ('library', 'Library', None),
                  ('library_construction', 'Library Construction (insert size bp)', None),
                  ('library_construction_protocol', 'Library construction protocol', None),
                  ('sequencer', 'Sequencer', None),
                  ('run_number', 'Run number', ingest_utils.get_clean_number),
                  ('flow_cell_id', 'Run #:Flow Cell ID', None),
                  ('lane_number', 'Lane number', ingest_utils.get_clean_number),
                  ('sequence_filename', 'File name', None),
                  ('md5_checksum', 'MD5 checksum', None),
                  ('contact_name', 'Name', None),
                  ('email', 'Email', None),
                  ('institution', 'Institution / Organisation', None),
                  ('species', 'Organism / Species', None),
                  ('sample_type', 'Sample type', None),
                  ('rna_source', 'Part of organism RNA/RNA extracted from', None),
                  ('extraction_method', 'Extraction method', None),
                  ('growth_protocol', 'Growth protocol of fungus and/or plant (medium, soil, water regimen, light/day, fertilisers etc)', None),
                  ('additional_information', 'Additional Information.', None),
    ]

    wrapper = ExcelWrapper(
        field_spec,
        file_name,
        sheet_name='Sheet2',
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


def run(file_name=SOURCE_FILE):
    """
    Pass parameters like below:
    vpython-bpam manage.py runscript ingest_gbr --script-args Wheat_pathogens_genomic_metadata.xlsx
    """
    truncate()
    ingest_utils.fetch_metadata(METADATA_URL, file_name)
    ingest(file_name)

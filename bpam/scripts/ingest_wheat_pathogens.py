# -*- coding: utf-8 -*-
import os
from apps.common.models import DNASource, Sequencer, Facility
from apps.wheat_pathogens.models import (
    Organism,
    PathogenSample,
    PathogenProtocol,
    PathogenRun,
    PathogenSequenceFile)
from libs import ingest_utils, user_helper, bpa_id_utils
from libs.logger_utils import get_logger
from libs.excel_wrapper import ExcelWrapper
from libs.fetch_data import Fetcher
from unipath import Path


logger = get_logger(__name__)

BPA_ID = "102.100.100"
DESCRIPTION = "Wheat Pathogens"

METADATA_URL = "https://downloads.bioplatforms.com/wheat_pathogens/metadata/"
METADATA_FILE = "current.xlsx"
DATA_DIR = Path(ingest_utils.METADATA_ROOT, "wheat_pathogens")


def _get_bpa_id(entry):
    """ Get or make BPA ID """

    bpa_id, report = bpa_id_utils.get_bpa_id(entry.bpa_id, "WHEAT_PATHOGEN", "Wheat Pathogens")
    if bpa_id is None:
        logger.warning("Could not add entry in {}, row {}, BPA ID Invalid: {}".format(entry.file_name, entry.row, report))
        return None
    return bpa_id


def get_dna_source(description):
    """ Get a DNA source if it exists, if it doesn't make it.  """

    description = description.strip().capitalize()
    if description == "":
        logger.debug("Set blank description to unknown")
        description = "Unknown"

    source, created = DNASource.objects.get_or_create(description=description)
    if created:
        source.note = "Added by Pathogens Project"
        source.save()

    return source


def ingest_samples(samples):
    def get_facility(name):
        """ Return the sequencing facility with this name, or a new facility.  """

        if name.strip() == "":
            name = "Unknown"

        facility, created = Facility.objects.get_or_create(name=name)

        return facility

    def get_organism(kingdom, phylum, species):
        """ Set the organism """

        genus = ""
        organism, created = Organism.objects.get_or_create(kingdom=kingdom, phylum=phylum, genus=genus, species=species)
        if created:
            logger.debug("Adding Organism {0} {1} {2} {3}".format(kingdom, phylum, genus, species))
            organism.kingdom = kingdom
            organism.phylum = phylum
            organism.genus = genus
            organism.species = species
            organism.note = "Wheat Pathogens Related Organism"
            organism.save()
        return organism

    def add_sample(e):
        """ Adds new sample or updates existing sample """

        bpa_id = _get_bpa_id(e)
        if bpa_id is None:
            return

        organism = get_organism(e.kingdom, e.phylum, e.species)
        pathogen_sample, created = PathogenSample.objects.get_or_create(bpa_id=bpa_id, organism=organism)

        pathogen_sample.name = e.sample_id
        pathogen_sample.sample_label = e.other_id
        pathogen_sample.dna_source = get_dna_source(e.sample_dna_source)
        pathogen_sample.official_variety_name = e.official_variety
        pathogen_sample.original_source_host_species = e.original_source_host_species
        pathogen_sample.wheat_pathogenicity = e.wheat_pathogenicity

        pathogen_sample.index = e.index_sequence
        pathogen_sample.library_id = e.library_id

        # scientist
        pathogen_sample.contact_scientist = user_helper.get_user(
            e.contact_scientist,
            "",
            (DESCRIPTION, ""))

        # collection
        pathogen_sample.collection_date = ingest_utils.get_date(e.collection_date)
        pathogen_sample.collection_location = e.collection_location
        pathogen_sample.dna_extraction_protocol = e.dna_extraction_protocol

        # facilities
        pathogen_sample.sequencing_facility = get_facility("AGRF")
        pathogen_sample.debug_note = ingest_utils.INGEST_NOTE + ingest_utils.pretty_print_namedtuple(e)
        pathogen_sample.save()
        logger.info("Ingested Pathogens sample {0}".format(pathogen_sample.name))

    for sample in samples:
        add_sample(sample)


def ingest_runs(sample_data):
    def get_protocol(entry):
        base_pairs = ingest_utils.get_clean_number(entry.library_construction)
        library_type = entry.library
        library_construction_protocol = entry.library_construction_protocol.replace(",", "").capitalize()

        protocol, created = PathogenProtocol.objects.get_or_create(
            base_pairs=base_pairs,
            library_type=library_type,
            library_construction_protocol=library_construction_protocol)

        if created:
            logger.debug("Created Protocol {0}".format(protocol))

        return protocol

    def get_sequencer(name):
        if name == "":
            name = u"Unknown"

        sequencer, created = Sequencer.objects.get_or_create(name=name)
        return sequencer

    def get_sample(bpa_id):
        sample, created = PathogenSample.objects.get_or_create(bpa_id=bpa_id)
        if created:
            logger.debug("Created sample ID {0}".format(bpa_id))
        return sample

    def get_run_number(entry):
        run_number = ingest_utils.get_clean_number(entry.run_number)
        return run_number

    def get_lane_number(entry):
        lane_number = ingest_utils.get_clean_number(entry.lane_number)
        return lane_number

    def add_run(entry):
        """ The run produced several files """

        flow_cell_id = entry.flow_cell_id.strip()
        run_number = get_run_number(entry)

        bpa_id = _get_bpa_id(entry)
        if bpa_id is None:
            return
        try:
            pathogen_sample = PathogenSample.objects.get(bpa_id=bpa_id)
        except PathogenSample.DoesNotExist:
            logger.error("Pathogen sample with BPA ID {0} does not exist".format(bpa_id))
            return

        pathogen_run, created = PathogenRun.objects.get_or_create(
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

        # FIXME, I"m sure this is wrong
        pathogen_run.protocol.run = pathogen_run
        pathogen_run.protocol.save()

        return pathogen_run

    def add_file(entry, pathogen_run):
        """ Add each sequence file produced by a run """
        bpa_id = _get_bpa_id(entry)
        if bpa_id is None:
            return

        def get_file_name(_fname):
            """ The filenames in the spreadsheet has paths prepended, strip them out """
            head, tail = os.path.split(_fname.strip())
            return tail

        file_name = get_file_name(entry.sequence_filename)
        if file_name != "":
            f = PathogenSequenceFile()
            f.sample = PathogenSample.objects.get(bpa_id=bpa_id)
            f.run = pathogen_run
            f.index_number = ingest_utils.get_clean_number(entry.index_number)
            f.lane_number = get_lane_number(entry)
            f.filename = file_name
            f.md5 = entry.md5_checksum
            f.file_size = entry.file_size
            f.note = ingest_utils.pretty_print_namedtuple(entry)
            f.save()

    for e in sample_data:
        sequence_run = add_run(e)
        add_file(e, sequence_run)


def ingest(file_name):
    sample_data = list(get_pathogen_sample_data(file_name))
    bpa_id_utils.ingest_bpa_ids(sample_data, "WHEAT_PATHOGEN", "Wheat Pathogens")
    ingest_samples(sample_data)
    ingest_runs(sample_data)


def get_pathogen_sample_data(file_name):
    """
    The data sets is relatively small, so make a in-memory copy to simplify some operations.
    """

    field_spec = [("bpa_id", "BPA ID", lambda s: s.replace("/", ".")),
                  ("official_variety", "Isolate name", None),
                  ("kingdom", "Kingdom", None),
                  ("phylum", "Phylum", None),
                  ("species", "Species", None),
                  ("sample_id", "Researcher Sample ID", None),
                  ("other_id", "Other IDs", None),
                  ("original_source_host_species", "Original source host species", None),
                  ("collection_date", "Isolate collection date", None),
                  ("collection_location", "Isolate collection location", None),
                  ("wheat_pathogenicity", "Pathogenicity towards wheat", None),
                  ("contact_scientist", "Contact scientist", None),
                  ("sample_dna_source", "DNA Source", None),
                  ("dna_extraction_protocol", "DNA extraction protocol", None),
                  ("library", "Library ", None),
                  ("library_construction", "Library Construction", None),
                  ("library_construction_protocol", "Library construction protocol", None),
                  ("sequencer", "Sequencer", None),
                  ("sample_label", "Sample (AGRF Labelling)", None),
                  ("library_id", "Library ID", None),
                  ("index_number", "Index #", None),
                  ("index_sequence", "Index", None),
                  ("run_number", "Run number", None),
                  ("flow_cell_id", "Run #:Flow Cell ID", None),
                  ("lane_number", "Lane number", None),
                  ("qc_software", "AGRF DATA QC software (please include version)", None),  # empty
                  ("sequence_filename", "FILE NAME", None),
                  ("sequence_filetype", "file type", None),
                  ("md5_checksum", "MD5 checksum", None),
                  ("file_size", "Size", None),
                  ("analysis_performed", "analysis performed (to date)", None),
                  ("genbank_project", "GenBank Project", None),
                  ("locus_tag", "Locus tag", None),
                  ("genome_analysis", "Genome-Analysis", None),
                  ("metdata_file", "Metadata file", None)
                  ]

    wrapper = ExcelWrapper(
        field_spec,
        file_name,
        sheet_name="Metadata",
        header_length=1,
        column_name_row_index=0)
    return wrapper.get_all()


def truncate():
    from django.db import connection

    cursor = connection.cursor()
    cursor.execute("TRUNCATE TABLE {0} CASCADE".format(PathogenSample._meta.db_table))
    cursor.execute("TRUNCATE TABLE {0} CASCADE".format(PathogenRun._meta.db_table))
    cursor.execute("TRUNCATE TABLE {0} CASCADE".format(PathogenProtocol._meta.db_table))
    cursor.execute("TRUNCATE TABLE {0} CASCADE".format(PathogenSequenceFile._meta.db_table))


def run():
    truncate()

    # fetch the old data file
    fetcher = Fetcher(DATA_DIR, METADATA_URL)
    fetcher.fetch(METADATA_FILE)

    ingest(Path(DATA_DIR, METADATA_FILE))

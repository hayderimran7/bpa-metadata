# -*- coding: utf-8 -*-

import djqscsv
from .models import GBRSample
from .models import GBRSequenceFile

# samples
sample_values = (
    "bpa_id",
    "name",
    "dna_source__description",
    "organism__genus",
    "organism__species",
    "dataset",
    "dna_extraction_protocol",
    "requested_read_length",
    "sequencing_facility__name",
    "collection_event__site__site_name",
    "collection_event__site__lat",
    "collection_event__site__lon",
    "collection_event__collection_date",
    "collection_event__water_temp",
    "collection_event__water_ph",
    "collection_event__depth",
    "collection_event__note",
    "sequencing_notes",
    "collection_event__collector__first_name",
    "collection_event__collector__last_name",
    "collection_event__collector__email",
)

sample_headers = {
    "name": "Sample Name",
    "dna_source__description": "DNA/RNA Source",
    "organism__genus": "Genus",
    "organism__species": "Species",
    "sequencing_facility__name": "Facility",
    "collection_event__site__site_name": "Site Name",
    "collection_event__site__lat": "Latitude",
    "collection_event__site__lon": "Longitude",
    "collection_event__collection_date": "Collection Date",
    "collection_event__water_temp": "Water Temperature",
    "collection_event__water_ph": "Water pH",
    "collection_event__depth": "Water Depth (m)",
    "collection_event__note": "Note",
    "collection_event__collector__first_name": "Collector Name",
    "collection_event__collector__last_name": "Collector Last Name",
    "collection_event__collector__email": "Collector email"
}


def get_samples(response):
    qs = GBRSample.objects.values(*sample_values)
    return djqscsv.render_to_csv_response(qs, field_header_map=sample_headers)


# metagenomic sequence files
sequence_file_headers = {
    "sample__organism__genus": "Genus",
    "sample__organism__species": "Species",
    "sample__collection_event__site__site_name": "Collection Site Name",
    "sample__collection_event__site__lat": "Latitude",
    "sample__collection_event__site__lon": "Longitue",
    "sample__collection_event__collection_date": "Collection date",
    "sample__name": "Sample Name",
}

sequence_file_values = (
    "filename",
    "md5",
    "sample__organism__genus",
    "sample__organism__species",
    "sample__collection_event__site__site_name",
    "sample__collection_event__site__lat",
    "sample__collection_event__site__lon",
    "sample__collection_event__collection_date",
    "sample__name",
)


def get_sequencefiles(response):
    qs = GBRSequenceFile.objects.values(*sequence_file_values)
    return djqscsv.render_to_csv_response(qs, field_header_map=sequence_file_headers)

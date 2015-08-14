# -*- coding: utf-8 -*-

import djqscsv
from cStringIO import StringIO
from .models import MelanomaSample
from .models import MelanomaSequenceFile


sequence_file_headers = {
    'sample__organism__genus': 'Genus',
    'sample__organism__species': 'Species',
    'sample__collection_event__site__site_name': 'Collection Site Name',
    'sample__collection_event__site__lat': 'Latitude',
    'sample__collection_event__site__lon': 'Longitue',
    'sample__collection_date': 'Collection date',
    'sample__name': 'Sample Name',
    }

sequence_file_values = (
    'sample__organism__genus',
    'sample__organism__species',
    'sample__collection_event__site__site_name',
    'sample__collection_event__site__lat',
    'sample__collection_event__site__lon',
    'sample__collection_date',
    'sample__name',
    'filename',
    'md5',
    )

def get_sequencefiles(response):
    qs = MelanomaSequenceFile.objects.values(*sequence_file_values)
    return djqscsv.render_to_csv_response(qs, field_header_map=sequence_file_headers)


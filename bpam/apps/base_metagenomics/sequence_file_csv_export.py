# -*- coding: utf-8 -*-
import djqscsv
from .models import MetagenomicsSequenceFile

field_header_map = {
    'sample_id': 'BPA Sample ID',
    'extraction__extraction_id': 'Extraction',
    'run__sequencing_facility__name': 'Facility',
    'protocol__library_type': 'Library',
    'protocol__base_pairs': 'Insert Size',
    'run__flow_cell_id': 'Flowcell',
    'index': 'Index',
    'lane_number': 'Lane',
    'filename': 'File Name',
    'md5': 'MD5'
}

values = (
    'sample_id',
    'extraction__extraction_id',
    'run__sequencing_facility__name',
    'protocol__library_type',
    'protocol__base_pairs',
    'run__flow_cell_id',
    'index',
    'lane_number',
    'filename',
    'md5'
)


def get_csv():
    qs = MetagenomicsSequenceFile.objects.values(*values)
    return djqscsv.render_to_csv_response(qs, field_header_map=field_header_map)

# -*- coding: utf-8 -*-

import djqscsv
from .models import CultivarSequenceFile

sequence_file_headers = {
    "sample__bpa_id": "BPA ID",
    "sample__name": "Sample Name",
    "sample__cultivar_code": "Code",
    "sample__characteristics": "Characteristics",
    "sample__organism__species": "Species",
    "sample__organism_part": "Part",
    "sample__dev_stage": "Development Stage",
    "sample__yield_properties": "Yield",
    "sample__morphology": "Morphology",
    "sample__pedigree": "Pedigree",
    "sample__maturity": "Maturity",
    "sample__pathogen_tolerance": "Pathogen Tolerance",
    "sample__drought_tolerance": "Drought Tolerance",
    "sample__soil_tolerance": "Soil Tolerance",
    "sample__classification": "Classification",
    "sample__url": "Link",
    "barcode": "Barcode",
    "flowcell": "Flowcell",
    "run_number": "Run",
    "casava_version": "Casava",
    "filename": "File Name",
    "md5": "MD5 Checksum",
}

sequence_file_values = ("sample__bpa_id",
                        "sample__name",
                        "sample__cultivar_code",
                        "sample__characteristics",
                        "sample__organism__species",
                        "sample__organism_part",
                        "sample__dev_stage",
                        "sample__yield_properties",
                        "sample__morphology",
                        "sample__pedigree",
                        "sample__maturity",
                        "sample__pathogen_tolerance",
                        "sample__drought_tolerance",
                        "sample__soil_tolerance",
                        "sample__classification",
                        "sample__url",
                        "barcode",
                        "flowcell",
                        "run_number",
                        "casava_version",
                        "filename",
                        "md5", )


def get_sequencefiles(response):
    qs = CultivarSequenceFile.objects.values(*sequence_file_values)
    return djqscsv.render_to_csv_response(qs, field_header_map=sequence_file_headers)

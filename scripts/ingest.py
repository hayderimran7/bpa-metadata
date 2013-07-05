import csv

from common.models import *


def add_projects():
    
    projects = (('Melanoma', 'Human Melanoma'),
                ('Coral', 'Great Barrier Reef Coral'),
                ('BASE Soil Agricultural', 'BASE Soil project agricultural sites'),
                ('BASE Soil Environmental', 'BASE Soil project environmental sites'),
                ('Wheat Cultivars', 'Wheat Cultivars'),
                ('Wheat Fungal pathogens', 'Wheat fungal pathogens'))
    
    for name, descr in projects: 
        project = BPAProject()
        project.name = name
        project.description = descr
        project.save()

def ingest_melanoma():
    
    with open('./scripts/melanoma_sheet3.csv', 'rb') as melanoma_files:
        fieldnames = ['BPA_ID', 
                      'sample_name', 
                      'sequence_coverage',
                      'sequencing_facility',
                      'species',
                      'contact_scientist',
                      'contact_affiliation',
                      'contact_email',
                      'sample_sex',
                      'sample_dna_source',
                      'sample_tumor_stage',
                      'histological_subtype',
                      'passage_number',
                      'dna_extraction_protocol',
                      'array_analysis_facility',
                      'date_sent_for_sequencing',
                      'whole_genome_sequencing_facility',
                      'date_received',
                      'library',
                      'library_construction',
                      'library_construction_protocol',
                      'index_number',
                      'sequencer',
                      'run_number',
                      'flow_Cell_id',
                      'lane_number',
                      'sequence_filename',
                      'md5_cheksum']
                  
        melanoma_files_reader = csv.DictReader(melanoma_files, fieldnames=fieldnames)
        for sample in melanoma_files_reader:
            pass
                        
        
def run():
    add_projects()
    ingest_melanoma()
    

import csv
from datetime import date

from common.models import *

def add_organism(genus="", species=""):
    organism = Organism(genus=genus, species=species)
    organism.save() 



def add_projects():
    
    projects = (('Melanoma', 'Human Melanoma'),
                ('Coral', 'Great Barrier Reef Coral'),
                ('BASE Soil Agricultural', 'BASE Soil project agricultural sites'),
                ('BASE Soil Environmental', 'BASE Soil project environmental sites'),
                ('Wheat Cultivars', 'Wheat Cultivars'),
                ('Wheat Fungal pathogens', 'Wheat fungal pathogens'))
    
    for name, descr in projects: 
        project = BPAProject(name=name, description=descr)
        project.save()
        print("Ingested project " + str(project))

def add_BPA_label(label):
    lbl = BPASampleLabel(label=label)
    lbl.project = BPAProject.objects.get(name='Melanoma')
    lbl.note = "Ingested from GoogleDocs on {}".format(date.today()) 
    lbl.save()
    print("Ingested BPA label " + str(lbl))


def add_sample(vals):
    sample = Sample()
    sample.label = BPASampleLabel.objects.get(label=vals['BPA_label'])
    sample.project = BPAProject.objects.get(name='Melanoma')
    sample.name = vals['sample_name']
    sample.organism = Organism.objects.get(genus="Homo", species="Sapient")
    sample.save()

def ingest_melanoma():
    
    with open('./scripts/melanoma_sheet3.csv', 'rb') as melanoma_files:
        fieldnames = ['BPA_label', 
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
            add_BPA_label(sample['BPA_label'])
            add_sample(sample)
                        
        
def run():
    add_organism(genus="Homo", species="Sapient")
    add_projects()
    ingest_melanoma()
    

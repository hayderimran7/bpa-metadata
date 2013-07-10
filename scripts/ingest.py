import csv
from datetime import date

from common.models import *
from melanoma.models import *

MELANOMA_SAMPLE_FILE='./scripts/melanoma_sheet3.csv'

INGEST_NOTE = "Ingested from GoogleDocs on {}".format(date.today()) 


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


def ingest_bpa_ids(data):
    """
    The BPA ID's are unique
    """
    def add_BPA_ID(id):
        lbl = BPAUniqueID(bpa_id=id)
        lbl.project = BPAProject.objects.get(name='Melanoma')
        lbl.note = INGEST_NOTE
        lbl.save()
        print("Ingested BPA Unique ID: " + str(lbl))    
    
    id_set = set()
    for e in data:
        id_set.add(e['BPA_ID']) 
    for id in id_set:
        add_BPA_ID(id)

def ingest_samples(samples):
    
    def add_sample(vals):
        sample = MelanomaSample()
        sample.bpa_id = BPAUniqueID.objects.get(bpa_id=vals['BPA_ID'])
        sample.name = vals['sample_name']
        sample.organism = Organism.objects.get(genus="Homo", species="Sapient")
        sample.note = INGEST_NOTE
        sample.save()
        print("Ingested Melanoma sample {}".format(sample.name))

    for sample in samples:
        add_sample(sample)

def ingest_contacts(data):
    """
    Contacts associated with the Melanoma BPA poject
    """
    pass
    

def get_melanoma_sample_data():
    """
    The datasets is relatively small, so make a in-memory copy to simplify some operations. 
    """
    with open(MELANOMA_SAMPLE_FILE, 'rb') as melanoma_files:
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
        return list(melanoma_files_reader)


def ingest_melanoma():    
        sample_data = get_melanoma_sample_data()
        
        ingest_contacts(sample_data)
        ingest_bpa_ids(sample_data)
        ingest_contacts(sample_data)
        ingest_samples(sample_data)
                        
        
def run():
    add_organism(genus="Homo", species="Sapient")
    add_projects()
    ingest_melanoma()
    

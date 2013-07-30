import csv
from datetime import date
from bpaauth.models import BPAUser
from common.models import *
from melanoma.models import *

MELANOMA_SAMPLE_FILE='./scripts/data/melanoma_samples.csv'
MELANOMA_ARRAY_FILE='./scripts/data/melanoma_arrays.csv'
MELANOMA_CONTACT_DATA='./scripts/data/melanoma_contacts.csv'

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
        id_set.add(e['bpa_id']) 
    for id in id_set:
        add_BPA_ID(id)

def ingest_samples(samples):
    
    def add_sample(vals):
        sample = MelanomaSample()
        sample.bpa_id = BPAUniqueID.objects.get(bpa_id=vals['bpa_id'])
        sample.name = vals['sample_name']
        sample.organism = Organism.objects.get(genus="Homo", species="Sapient")
        sample.note = INGEST_NOTE
        sample.save()
        print("Ingested Melanoma sample {}".format(sample.name))

    for sample in samples:
        add_sample(sample)

def ingest_contacts():
    """
    Contacts associated with the Melanoma BPA poject
    """
    
    from django.contrib.auth.models import Group
    from django.contrib.auth import get_user_model
    
    def get_group(name):        
        def get_group_name(raw_group):
            if raw_group != "":
                return raw_group.strip().split()[0]
            else:
                return "Ungrouped"
                        
        try:
            group = Group.objects.get(name=get_group_name(name))
        except Group.DoesNotExist:
            print("Group {} does not exit, adding it".format(name))
            group = Group(name=name)            
            group.save()
            
        return group      
    
    def is_active(active_str):
        active = active_str.strip().lower()
        return active == 'x'
        
    def get_data():
        with open(MELANOMA_CONTACT_DATA, 'rb') as contacts:
            # Location, Job Title, Department, Surname, First Name, Direct Line, Email, Username, Enabled   
            reader = csv.DictReader(contacts)
            return list(reader)
    
    contacts = get_data()
    
    for contact in contacts:
        User = get_user_model()
        user = User()
        user.username = contact['Username'].strip()
        user.email = contact['Email'].strip()
        user.first_name = contact['First Name'].strip()
        user.last_name = contact['Surname'].strip()        
        user.telephone = contact['Direct Line']
        user.is_staff = is_active(contact['Enabled'])
        user.title = contact['Job Title'].strip()
        user.department = contact['Department']
        user.note = contact['Location']
        # user.is_superuser = True
        user.save()
        
        group = get_group(contact['Location'])
        user.groups.add(group)
        
        user.save()
        


        
        
def ingest_arrays(arrays):
    
    def get_bpa_id(bpa_id):
        try:
            id = BPAUniqueID.objects.get(bpa_id=bpa_id)
        except BPAUniqueID.DoesNotExist:
            print("BPA ID {} does not exit, adding it".format(bpa_id))
            id = BPAUniqueID(bpa_id=bpa_id)
            id.project = BPAProject.objects.get(name='Melanoma')
            id.note = "Created during array ingestion on {}".format(date.today())
            id.save()      
                  
        return id
        
    
    def get_gender(str):
        str = str.strip().lower()
        if str == "male": return 'M'
        if str == "female": return 'F'
        return 'U'
    
    for e in arrays:
        array = Array()        
        array.batch_number = int(e['batch_no'])        
        array.bpa_id = get_bpa_id(e['bpa_id'])
        array.mia_id = e['mia_id']
        array.array_id = e['array_id']
        array.call_rate = float(e['call_rate'])
        array.gender = get_gender(e['gender'])
        array.well_id = e['well_id']
        
        array.save()
                

def get_melanoma_sample_data():
    """
    The datasets is relatively small, so make a in-memory copy to simplify some operations. 
    """
    with open(MELANOMA_SAMPLE_FILE, 'rb') as melanoma_files:
        fieldnames = ['bpa_id', 
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
                  
        reader = csv.DictReader(melanoma_files, fieldnames=fieldnames)
        return list(reader)


def get_array_data():
    """
    Copy if the 'Array Data' Tab from the Melanoma_study_metadata document
    """
    
    with open(MELANOMA_ARRAY_FILE, 'rb') as array_data:
        fieldnames = ['batch_no',
                      'well_id',
                      'bpa_id',
                      'mia_id',
                      'array_id',
                      'call_rate',
                      'gender',                      
                      ]
        reader = csv.DictReader(array_data, fieldnames=fieldnames)
        return list(reader)


def ingest_melanoma():    
        sample_data = get_melanoma_sample_data()
        
        ingest_bpa_ids(sample_data)
        ingest_samples(sample_data)
        ingest_arrays(get_array_data())
                        
        
def run():
    ingest_contacts()
    add_organism(genus="Homo", species="Sapient")
    add_projects()
    ingest_melanoma()
    
def run2():
    ingest_contacts()
    
    

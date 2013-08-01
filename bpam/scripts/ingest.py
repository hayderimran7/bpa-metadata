import csv
from datetime import date
from bpaauth.models import BPAUser
from common.models import *
from melanoma.models import *

MELANOMA_SAMPLE_FILE='./scripts/data/melanoma_samples.csv'
MELANOMA_ARRAY_FILE='./scripts/data/melanoma_arrays.csv'
MELANOMA_CONTACT_DATA='./scripts/data/melanoma_contacts.csv'

INGEST_NOTE = "Ingested from GoogleDocs on {}".format(date.today()) 

MELANOMA_SEQUENCER = "Illumina Hi Seq 2000"


def get_date(date_str):
    """
    Because dates in he spreadsheets comes in all forms, dateutil is used to figure it out.  
    """
    from dateutil import parser
    return parser.parse(date_str)
 
def strip_all(reader):
    """
    Scrub extra whitespace from values in the reader dicts as read from the csv files 
    """
    
    entries = []
    for entry in reader:
        new_e = {}
        for k, v in entry.items():
            new_e[k] = v.strip()
        entries.append(new_e)
    
    return entries
        
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
        id_set.add(e['bpa_id'].strip()) 
    for id in id_set:
        add_BPA_ID(id)

def ingest_samples(samples):
    
    def add_sample(vals):
        bpa_id = vals['bpa_id']
        try:
            # Test if sample already exists
            # First come fist serve            
            MelanomaSample.objects.get(bpa_id__bpa_id=bpa_id)
        except MelanomaSample.DoesNotExist:
            sample = MelanomaSample()
            sample.bpa_id = BPAUniqueID.objects.get(bpa_id=bpa_id)
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
            return strip_all(reader)
    
    contacts = get_data()
    
    for contact in contacts:
        User = get_user_model()
        user = User()
        user.username = contact['Username']
        user.email = contact['Email']
        user.first_name = contact['First Name']
        user.last_name = contact['Surname']
        user.telephone = contact['Direct Line']
        user.is_staff = is_active(contact['Enabled'])
        user.title = contact['Job Title']
        user.department = contact['Department']        
        user.location = contact['Location']
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
                      'flow_cell_id',
                      'lane_number',
                      'sequence_filename',
                      'md5_cheksum',
                      'file_path',
                      'file_url',
                      'analysed',
                      'analysed_url']
                  
        reader = csv.DictReader(melanoma_files, fieldnames=fieldnames)
        return strip_all(reader)
      

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
        return strip_all(reader)


def ingest_runs(sample_data):
        
    def get_sequencer(name):
        if name == "":
            name = "Unknown"
        try:
            sequencer = Sequencer.objects.get(name=name)
        except Sequencer.DoesNotExist:
            sequencer = Sequencer(name=name)
            sequencer.save()
        return sequencer      
    
    def get_sample(bpa_id):
        sample = MelanomaSample.objects.get(bpa_id__bpa_id=bpa_id)
        print("Found sample {}".format(sample))
        return sample
        
    def get_clean_number(str, default=None):
        try:
            return int(str.lower().replace('run', '').strip())
        except ValueError:
            return default
        
    def get_run_number(e):
        """
        ANU does not have their run numbers entered.
        """
        
        run_number = get_clean_number(e['run_number'])
        if run_number == None:
            # see if its ANU and parse the run_number from the filename
            if e['whole_genome_sequencing_facility'].strip() == 'ANU':
                filename = e['sequence_filename'].strip()
                if filename != "":
                    try:
                        run_number = int(filename.split('_')[6])
                        print("ANU run_number {} parsed from filename".format(run_number))               
                    except IndexError:
                        print("Filename {} wrong format".format(filename))                

        return run_number
                
        
        
    def add_run(e):
        """
        The run produced several files
        """
        flow_cell_id = e['flow_cell_id'].strip()
        bpa_id = e['bpa_id'].strip()
        run_number = get_run_number(e)
        
        try:
            run = MelanomaRun.objects.get(flow_cell_id=flow_cell_id, run_number=run_number, sample__bpa_id__bpa_id=bpa_id)
        except MelanomaRun.DoesNotExist:
            run = MelanomaRun()
            run.flow_cell_id = flow_cell_id
            run.run_number = run_number 
            run.sample = get_sample(bpa_id)
            run.passage_number = get_clean_number(e['passage_number']) 
            run.index_number = get_clean_number(e['index_number'])
            run.sequencer = get_sequencer(MELANOMA_SEQUENCER) # Ignore the empty column
            run.lane_number = get_clean_number(e['lane_number'])
            run.save()  
            
        return run                     



    

    def add_file(e, run):
        """
        Add each sequence file produced by a run
        """
        fname = e['sequence_filename'].strip()
        if fname != "":
            f = MelanomaSequenceFile()
            f.date_received_from_sequencing_facility = get_date(e['date_received'].strip())
            f.run = run
            f.filename = fname
            f.md5 = e['md5_cheksum'].strip()
            f.save()

    for e in sample_data:
        run = add_run(e)
        add_file(e, run)
        

def ingest_files(sample_data):
    """
    The melanoma study metadata sheet is a list of files.
    Each row represents a file.
    """
    
    for file in sample_data:
        pass
        

def ingest_melanoma():    
        sample_data = get_melanoma_sample_data()
        
        ingest_bpa_ids(sample_data)
        ingest_samples(sample_data)
        ingest_arrays(get_array_data())
        ingest_runs(sample_data)
        ingest_files(sample_data)

        
def run():
    ingest_contacts()
    add_organism(genus="Homo", species="Sapient")
    add_projects()
    ingest_melanoma()
    
def runx():
    sample_data = get_melanoma_sample_data()
    ingest_runs(sample_data)
    
    

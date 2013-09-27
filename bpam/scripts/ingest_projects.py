from apps.common.models import *


def add_projects():
    """ The set of projects is set"""
    
    projects = (('Melanoma', 'Human Melanoma'),
                ('GBR', 'Great Barrier Reef Coral'),
                ('BASE', 'BASE, Agricultural and Environmental Soil'),
                ('Wheat 7A', 'Wheat Gene 7A'),
                ('Wheat Cultivars', 'Wheat Cultivars'),
                ('Wheat Fungal pathogens', 'Wheat fungal pathogens'))
    
    for name, descr in projects: 
        project = BPAProject(name=name, description=descr)
        project.save()
        print("Ingested project " + str(project))
        
        
def run():
    add_projects()

from django.contrib import admin
from melanoma.models import (TumorStage,
                             Array,
                             MelanomaSample,
                             MelanomaRun,
                             MelanomaSequenceFile,
                             )


class MelanomaSequenceFileAdmin(admin.ModelAdmin):
    fieldsets = [             
        (None, {'fields' : [('filename', 'md5'),
                            ('lane_number', 'index_number'),
                            'BPA_archive_url',
                            ('analysed', 'analysed_url'),
                            'ftp_url',
                            'date_received_from_sequencing_facility',
                            'note'
                            ]
                }
        ),
       
    ]

    list_display = ('filename', 'date_received_from_sequencing_facility', 'run')

class MelanomaRunAdmin(admin.ModelAdmin):
    fieldsets = [       
       ('Facilities', {'fields': [('sequencing_faciltiy', 'array_analysis_faciltiy', 'whole_genome_sequencing_faciltiy')]}),
       ('Sequencing', {'fields': [('protocol'),
                                  ('sequencer', 'run_number', 'flow_cell_id'),
                                  'DNA_extraction_protocol',
                                  'passage_number'                        
                                  ]
                       }
        ),
    ]
    
    list_display = ('sample', 'sequencer', 'flow_cell_id', 'run_number', 'passage_number')

class SampleAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Sample Identification', {'fields': [('bpa_id', 'name')]}),
        ('Source', {'fields':['organism', 'dna_source', 'sex', 'tumor_stage', 'histological_subtype']}),
        (None, {'fields': ['date_sent_to_sequencing_facility', 'contact_scientist', 'note']}),
    ]
    
    list_display = ('bpa_id', 'name', 'note')
    
class ArrayAdmin(admin.ModelAdmin):
    list_display = ('bpa_id', 'array_id', 'mia_id')

admin.site.register(TumorStage)
admin.site.register(Array, ArrayAdmin)
admin.site.register(MelanomaSample, SampleAdmin)
admin.site.register(MelanomaRun, MelanomaRunAdmin)
admin.site.register(MelanomaSequenceFile, MelanomaSequenceFileAdmin)
    
    


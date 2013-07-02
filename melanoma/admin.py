from django.contrib import admin
from melanoma.models import *


admin.site.register(DNASource)
admin.site.register(LibraryProtocol)
admin.site.register(Library)
admin.site.register(Array)
admin.site.register(TumorStage)
admin.site.register(Sequencer)

class SampleAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Sample Identification', {'fields': ['bpa_id', 'sample_name']}),
        ('Facilities', {'fields': ['sequencing_faciltiy',
                                   'array_analysis_faciltiy',
                                   'whole_genome_sequencing_faciltiy'
                                   ]
                        }
        ),
        ('Sequencing', {'fields': ['dna_source',
                                   'library',
                                   'index_number',
                                   'sequencer',
                                   'run_number',
                                   'flow_cell_id',
                                   'lane_number',
                                   'DNA_extraction_protocol',
                                   'passage_number'
                                   ]
                        }
         ),
        ('Sample Type', {'fields' : ['sex',
                                     'tumor_stage',
                                     'histological_subtype'
                                     ]
                         }
         ),
        ('Data', {'fields' : ['sequence_facility_filename',
                              'md5cheksum',
                              'BPA_archive_url',
                              'analysed',
                              'analysed_url',
                              'ftp_url',
                              'date_sent_to_sequencing_facility',
                              'date_recieved_from_sequencing_facility'
                              ]
                  }
         ),
        (None, {'fields': ['contact', 'note']}),
    ]
    
admin.site.register(Sample, SampleAdmin)

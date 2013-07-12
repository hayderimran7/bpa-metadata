from django.contrib import admin

from .models import (BPAProject,
                     BPAUniqueID,
                     Facility,
                     Organism,
                     Library,
                     Run,
                     SequenceFile,
                     DNASource,
                     LibraryProtocol,
                     Sequencer,
                     )

    
class LibraryAdmin(admin.ModelAdmin):
    list_display = ('base_pairs', 'type', 'protocol')

    
class RunAdmin(admin.ModelAdmin):
     fieldsets = [       
        ('Facilities', {'fields': [('sequencing_faciltiy', 'array_analysis_faciltiy', 'whole_genome_sequencing_faciltiy')
                                   ]
                        }
        ),
        ('Sequencing', {'fields': [('library', 'index_number'),
                                   ('sequencer', 'run_number', 'flow_cell_id', 'lane_number'),
                                   'DNA_extraction_protocol',
                                   'passage_number'                        
                                   ]
                        }
         ),
    ]
        
class SequenceFileAdmin(admin.ModelAdmin):
     fieldsets = [       
      
        (None, {'fields' : [('filename', 'md5cheksum'),
                              'BPA_archive_url',
                              ('analysed', 'analysed_url'),
                              'ftp_url',
                              'date_received_from_sequencing_facility'
                              ]
                  }
         ),
    ]
    
class AffiliationAdmin(admin.ModelAdmin):
    fields = (('name', 'description'),)
    list_display = ('name', 'description')
    
    
class BPAProjectAdmin(admin.ModelAdmin):
    fields = (('name', 'description'),)
    list_display = ('name', 'description')
    
    
class BPAUniqueIDAdmin(admin.ModelAdmin):
    fields = (('bpa_id', 'project'), 'note')
    list_display = ('bpa_id', 'project', 'note')



admin.site.register(BPAProject, BPAProjectAdmin)
admin.site.register(BPAUniqueID, BPAUniqueIDAdmin)
admin.site.register(Facility)
admin.site.register(Organism)
admin.site.register(Library, LibraryAdmin)
admin.site.register(Run, RunAdmin)
admin.site.register(SequenceFile, SequenceFileAdmin)
admin.site.register(DNASource)
admin.site.register(LibraryProtocol)
admin.site.register(Sequencer)

    
    
    


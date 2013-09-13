from django.contrib import admin

from .models import (BPAProject,
                     BPAUniqueID,
                     Facility,
                     Protocol,
                     Organism,                     
                     SequenceFile,
                     DNASource,
                     Sequencer,
                     )

    
class ProtocolAdmin(admin.ModelAdmin):
    fields = (('library_type', 'base_pairs', 'library_construction_protocol'), 'note')
    list_display = ('library_type', 'base_pairs', 'library_construction_protocol')

    
class AffiliationAdmin(admin.ModelAdmin):
    fields = (('name', 'description'),)
    list_display = ('name', 'description')
    
    
class BPAProjectAdmin(admin.ModelAdmin):
    fields = (('name', 'description'),'note')
    list_display = ('name', 'description')
    
    
class BPAUniqueIDAdmin(admin.ModelAdmin):
    fields = (('bpa_id', 'project'), 'note')
    list_display = ('bpa_id', 'project', 'note')

class FacilityAdmin(admin.ModelAdmin):
    fields = (('name', 'service'), 'note')
    list_display = ('name', 'service', 'note')

admin.site.register(BPAProject, BPAProjectAdmin)
admin.site.register(BPAUniqueID, BPAUniqueIDAdmin)
admin.site.register(Facility, FacilityAdmin)
admin.site.register(Organism)
admin.site.register(Protocol, ProtocolAdmin)
admin.site.register(DNASource)
admin.site.register(Sequencer)

    
    
    

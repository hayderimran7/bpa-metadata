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


class AffiliationAdmin(admin.ModelAdmin):
    fields = (('name', 'description'),)
    list_display = ('name', 'description')
    
    
class BPAProjectAdmin(admin.ModelAdmin):
    fields = (('name', 'description'), 'note')
    list_display = ('name', 'description')
    
    
class BPAUniqueIDAdmin(admin.ModelAdmin):
    fields = (('bpa_id', 'project'), 'note')
    list_display = ('bpa_id', 'project', 'note')
    search_fields = ('bpa_id', 'project__name', 'note')


class FacilityAdmin(admin.ModelAdmin):
    fields = ('name', 'note')
    list_display = ('name',)

admin.site.register(BPAProject, BPAProjectAdmin)
admin.site.register(BPAUniqueID, BPAUniqueIDAdmin)
admin.site.register(Facility, FacilityAdmin)
admin.site.register(Organism)
admin.site.register(DNASource)
admin.site.register(Sequencer)

    
    
    


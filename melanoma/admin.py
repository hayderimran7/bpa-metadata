from django.contrib import admin
from melanoma.models import (TumorStage,
                             Array,
                             MelanomaSample
                             )

class SampleAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Sample Identification', {'fields': [('bpa_id', 'name')]}),
        ('Source', {'fields':['organism', 'dna_source']}),
        (None, {'fields': ['date_sent_to_sequencing_facility', 'contact_scientist', 'note']}),
    ]
    
    list_display = ('bpa_id', 'name', 'note')

admin.site.register(TumorStage)
admin.site.register(Array)
admin.site.register(MelanomaSample, SampleAdmin)
    
    


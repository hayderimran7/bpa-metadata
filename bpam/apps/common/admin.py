from django.contrib import admin
from django import forms

from .models import (BPAProject,
                     BPAUniqueID,
                     Facility,
                     Protocol,
                     Organism,                     
                     SequenceFile,
                     DNASource,
                     Sequencer,
                     )


class SequenceFileForm(forms.ModelForm):
    class Meta:
        model = SequenceFile
        widgets = {
            'filename': forms.TextInput(attrs={'size': 100}),
        }


class SequenceFileAdmin(admin.ModelAdmin):
    form = SequenceFileForm

    fieldsets = [
        (None,
         {'fields': (
             ('filename', 'md5'), ('lane_number', 'index_number'), 'analysed', 'date_received_from_sequencing_facility',
             'note'), }),
    ]

    search_fields = ('sample__bpa_id__bpa_id', 'sample__name')

    def download_field(self, obj):
        if obj.link_ok():
            return '<a href="%s">%s</a>' % (obj.url, obj.filename)
        else:
            return '<a style="color:grey">%s</a>' % obj.filename

    download_field.allow_tags = True
    download_field.short_description = 'Filename'

    list_display = ('get_sample_id', 'download_field', 'get_sample_name', 'date_received_from_sequencing_facility', 'run')
    list_filter = ('date_received_from_sequencing_facility',)

    def get_sample_id(self, obj):
        return obj.sample.bpa_id

    get_sample_id.short_description = 'BPA ID'
    get_sample_id.admin_order_field = 'sample__bpa_id'

    def get_sample_name(self, obj):
        return obj.sample.name

    get_sample_name.short_description = 'Sample Name'
    get_sample_name.admin_order_field = 'sample__name'


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


class OrganismAdmin(admin.ModelAdmin):
    list_display = ('genus', 'species')

admin.site.register(BPAProject, BPAProjectAdmin)
admin.site.register(BPAUniqueID, BPAUniqueIDAdmin)
admin.site.register(Facility, FacilityAdmin)
admin.site.register(Organism, OrganismAdmin)
admin.site.register(DNASource)
admin.site.register(Sequencer)

    
    
    


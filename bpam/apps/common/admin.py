from django.contrib import admin
from django import forms
from suit.widgets import AutosizedTextarea

from .models import (BPAProject,
                     BPAUniqueID,
                     Facility,
                     Organism,
                     SequenceFile,
                     DNASource,
                     Sequencer,
                     )


class SampleAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Sample Identification',
         {'fields': (('bpa_id', 'name'))}),
        ('DNA Source',
         {'fields': (
             'organism', 'dna_source', 'dna_extraction_protocol', 'gender', 'tumor_stage', 'histological_subtype')}),
        ('Sample Management',
         {'fields': (
             'requested_sequence_coverage', 'date_sent_to_sequencing_facility', 'contact_scientist',
             'note')}),
    ]

    list_display = ('bpa_id', 'name', 'dna_source', 'dna_extraction_protocol', 'tumor_stage')
    search_fields = ('bpa_id__bpa_id', 'name', 'tumor_stage__description')
    list_filter = ('dna_source', 'gender', 'requested_sequence_coverage',)


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

    def download_field(self, obj):
        if obj.link_ok():
            return '<a href="%s">%s</a>' % (obj.url, obj.filename)
        else:
            return '<a style="color:grey">%s</a>' % obj.filename
    download_field.allow_tags = True
    download_field.short_description = 'Filename'

    # Sample ID
    def get_sample_id(self, obj):
        return obj.sample.bpa_id
    get_sample_id.short_description = 'BPA ID'
    get_sample_id.admin_order_field = 'sample__bpa_id'

    # Sample Name
    def get_sample_name(self, obj):
        return obj.sample.name
    get_sample_name.short_description = 'Sample Name'
    get_sample_name.admin_order_field = 'sample__name'

    search_fields = ('sample__bpa_id__bpa_id', 'sample__name')
    list_display = ('get_sample_id', 'download_field', 'get_sample_name',
                    'date_received_from_sequencing_facility', 'run')
    list_filter = ('date_received_from_sequencing_facility',)


class AffiliationAdmin(admin.ModelAdmin):
    fields = (('name', 'description'),)
    list_display = ('name', 'description')


class BPAProjectForm(forms.ModelForm):
    class Meta:
        model = BPAProject
        widgets = {
            'note': AutosizedTextarea(attrs={'rows': 20, 'class': 'input-large'})
        }


class BPAProjectAdmin(admin.ModelAdmin):
    form = BPAProjectForm
    fields = ('name', 'description', 'note')
    list_display = ('name', 'key', 'description')


class BPAIDForm(forms.ModelForm):
    class Meta:
        model = BPAUniqueID
        widgets = {
            'note': AutosizedTextarea(attrs={'rows': 20, 'class': 'input-large'})
        }


class BPAUniqueIDAdmin(admin.ModelAdmin):
    form = BPAIDForm
    fields = ('bpa_id', 'project', 'note')
    list_display = ('bpa_id', 'project', 'note')
    search_fields = ('bpa_id', 'project__name', 'note')


class FacilityAdmin(admin.ModelAdmin):
    fields = ('name', 'note')
    list_display = ('name',)


class OrganismAdmin(admin.ModelAdmin):
    def get_organism_name(self, obj):
        return obj.name

    get_organism_name.short_description = 'Name'
    get_organism_name.admin_order_field = 'species'

    list_display = ('get_organism_name', 'kingdom', 'phylum', 'genus')


admin.site.register(BPAProject, BPAProjectAdmin)
admin.site.register(BPAUniqueID, BPAUniqueIDAdmin)
admin.site.register(Facility, FacilityAdmin)
admin.site.register(Organism, OrganismAdmin)
admin.site.register(DNASource)
admin.site.register(Sequencer)

    
    
    


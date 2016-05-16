from django.contrib import admin
from django import forms
from suit.widgets import AutosizedTextarea, SuitDateWidget, LinkedSelect

from .models import (BPAProject,
                     BPAUniqueID,
                     Facility,
                     Organism,
                     SequenceFile,
                     DNASource,
                     Sequencer,
                     Sample)


class SampleAdmin(admin.ModelAdmin):
    class SampleForm(forms.ModelForm):
        class Meta:
            fields = "__all__"
            model = Sample
            widgets = {
                'bpa_id': LinkedSelect(
                    attrs={'class': 'input-medium',
                           'style': 'width:50%'}),
                'name': forms.TextInput(
                    attrs={'class': 'input-large',
                           'style': 'width:95%'})
            }

    form = SampleForm
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


class SequenceFileAdmin(admin.ModelAdmin):
    class SequenceFileForm(forms.ModelForm):
        class Meta:
            fields = "__all__"
            model = SequenceFile
            widgets = {
                'date_received_from_sequencing_facility': SuitDateWidget,
                'filename': forms.TextInput(
                    attrs={'class': 'input-medium',
                           'style': 'width:50%'}),
                'md5': forms.TextInput(
                    attrs={'class': 'input-medium',
                           'style': 'width:50%'}),
                'sample': LinkedSelect(
                    attrs={'class': 'input-medium',
                           'style': 'width:40%'}),
                'run': LinkedSelect(
                    attrs={'class': 'input-medium',
                           'style': 'width:40%'}),
                'note': AutosizedTextarea(
                    attrs={'class': 'input-large',
                           'style': 'width:95%'})
            }

    form = SequenceFileForm

    fieldsets = [
        ('Sequence File',
         {'fields': (
             'filename', 'md5', 'sample', 'run', 'lane_number', 'index_number', 'analysed',
             'date_received_from_sequencing_facility',
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
    list_filter = ('sample__bpa_id', 'sample__name', 'date_received_from_sequencing_facility',)


class BPAProjectAdmin(admin.ModelAdmin):
    class BPAProjectForm(forms.ModelForm):
        class Meta:
            fields = ('key', 'name', 'description', 'note')
            model = BPAProject
            widgets = {
                'note': AutosizedTextarea(attrs={'class': 'input-large',
                                                 'style': 'width:95%'})
            }

    form = BPAProjectForm
    fields = ('name', 'description', 'note')
    list_display = ('name', 'description')


admin.site.register(BPAProject, BPAProjectAdmin)


class BPAUniqueIDAdmin(admin.ModelAdmin):
    class BPAIDForm(forms.ModelForm):
        class Meta:
            fields = "__all__"
            model = BPAUniqueID
            widgets = {
                'project': LinkedSelect,
                'note': AutosizedTextarea(attrs={'class': 'input-large',
                                                 'style': 'width:95%'})
            }

    form = BPAIDForm
    fields = ('bpa_id', 'project', 'note')
    list_display = ('bpa_id', 'project', 'note')
    search_fields = ('bpa_id', 'project__name', 'note')


admin.site.register(BPAUniqueID, BPAUniqueIDAdmin)


class FacilityAdmin(admin.ModelAdmin):
    class Form(forms.ModelForm):
        class Meta:
            fields = "__all__"
            model = Facility
            widgets = {
                'project': LinkedSelect,
                'note': AutosizedTextarea(attrs={'class': 'input-large',
                                                 'style': 'width:95%'})
            }

    form = Form
    fields = ('name', 'note')
    list_display = ('name',)


admin.site.register(Facility, FacilityAdmin)


class OrganismAdmin(admin.ModelAdmin):
    class Form(forms.ModelForm):
        class Meta:
            fields = "__all__"
            model = Organism
            widgets = {
                'note': AutosizedTextarea(attrs={'class': 'input-large',
                                                 'style': 'width:95%'})
            }

    form = Form

    def get_organism_name(self, obj):
        return obj.name

    get_organism_name.short_description = 'Name'
    get_organism_name.admin_order_field = 'species'
    list_display = ('get_organism_name', 'kingdom', 'phylum', 'genus')


admin.site.register(Organism, OrganismAdmin)


class DNASourceFormAdmin(admin.ModelAdmin):
    class DNASourceForm(forms.ModelForm):
        class Meta:
            fields = "__all__"
            model = DNASource
            widgets = {
                'description': forms.TextInput(attrs={'class': 'input-large',
                                                      'style': 'width:95%'}),
                'note': AutosizedTextarea(attrs={'class': 'input-large',
                                                 'style': 'width:95%'})
            }

    form = DNASourceForm


admin.site.register(DNASource, DNASourceFormAdmin)
admin.site.register(Sequencer)

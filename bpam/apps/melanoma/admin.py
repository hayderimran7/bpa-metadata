from django.contrib import admin
from django import forms
from suit.widgets import LinkedSelect, SuitDateWidget, AutosizedTextarea

from apps.common.admin import SequenceFileAdmin
from models import (TumorStage,
                    Array,
                    MelanomaSample,
                    MelanomaRun,
                    MelanomaSequenceFile,
                    MelanomaProtocol,
)


class SampleAdmin(admin.ModelAdmin):
    class SampleForm(forms.ModelForm):
        class Meta:
            model = MelanomaSample
            widgets = {
                'bpa_id': LinkedSelect(attrs={'class': 'input-medium'}),
                'name': forms.TextInput(attrs={'class': 'input-medium', 'style': 'width:50%'}),
                'organism': LinkedSelect,
                'dna_source': LinkedSelect,
                'tumor_stage': LinkedSelect,
                'contact_scientist': LinkedSelect,
                'debug_note': AutosizedTextarea(attrs={'class': 'input-large',
                                                       'style': 'width:95%'}, ),
                'note': AutosizedTextarea(attrs={'class': 'input-large',
                                                 'style': 'width:95%'}),
                'date_sent_to_sequencing_facility': SuitDateWidget,
            }

    form = SampleForm
    radio_fields = {'gender': admin.HORIZONTAL}

    suit_form_tabs = (
        ('id', 'Sample ID and Sequence Files'),
        ('dna', 'DNA Source'),
        ('management', 'Sample Management',),
        ('notes', 'Source Data Note')
    )

    fieldsets = [
        ('Sample Identification',
         {'classes': ('suit-tab suit-tab-id',),
          'fields': (
              ('bpa_id',
               'name'))}),
        ('DNA Source',
         {'classes': ('suit-tab suit-tab-dna',),
          'fields': (
              'organism',
              'dna_source',
              'dna_extraction_protocol',
              'gender',
              'tumor_stage',
              'histological_subtype')}),
        ('Sample Management',
         {'classes': ('suit-tab suit-tab-management',),
          'fields': (
              'requested_sequence_coverage',
              'date_sent_to_sequencing_facility',
              'contact_scientist',
              'note')}),
        ('Source Data Note',
         {'classes': ('suit-tab suit-tab-notes',),
          'fields': ('debug_note',)}),
    ]

    list_display = ('bpa_id', 'name', 'dna_source', 'dna_extraction_protocol', 'tumor_stage')
    search_fields = ('bpa_id__bpa_id', 'name', 'tumor_stage__description')
    list_filter = ('dna_source', 'gender', 'requested_sequence_coverage',)


admin.site.register(MelanomaSample, SampleAdmin)


class ArrayAdmin(admin.ModelAdmin):
    class ArrayForm(forms.ModelForm):
        class Meta:
            model = Array
            widgets = {
                'bpa_id': LinkedSelect
            }

    form = ArrayForm
    radio_fields = {'gender': admin.HORIZONTAL}
    list_display = ('bpa_id', 'array_id', 'mia_id')
    search_fields = ('bpa_id__bpa_id', 'array_id', 'mia_id')
    list_filter = ('bpa_id', 'array_id', 'mia_id')


admin.site.register(Array, ArrayAdmin)


class ProtocolForm(forms.ModelForm):
    class Meta:
        model = MelanomaProtocol
        widgets = {
            'library_construction_protocol': LinkedSelect,
            'note': AutosizedTextarea(attrs={'class': 'input-large',
                                             'style': 'width:95%'})
        }


class ProtocolAdmin(admin.ModelAdmin):
    form = ProtocolForm
    radio_fields = {'library_type': admin.HORIZONTAL}
    fields = ('library_type', 'base_pairs', 'library_construction_protocol', 'note')
    search_fields = (
        'library_type', 'library_construction_protocol', 'note', 'run__sample__bpa_id__bpa_id', 'run__sample__name')
    list_display = ('run', 'library_type', 'base_pairs', 'library_construction_protocol',)
    list_filter = ('library_type', 'base_pairs')


admin.site.register(MelanomaProtocol, ProtocolAdmin)


class MelanomaRunAdmin(admin.ModelAdmin):
    class ProtocolInline(admin.StackedInline):
        form = ProtocolForm
        model = MelanomaProtocol
        extra = 1
        radio_fields = {'library_type': admin.HORIZONTAL}

    inlines = (ProtocolInline, )

    class RunForm(forms.ModelForm):
        class Meta:
            model = MelanomaRun
            widgets = {
                'sample': LinkedSelect(attrs={'class': 'input-xxlarge'}),
                'sequencing_facility': LinkedSelect,
                'array_analysis_facility': LinkedSelect,
                'whole_genome_sequencing_facility': LinkedSelect,
                'sequencer': LinkedSelect
            }

    form = RunForm

    fieldsets = [
        ('Sample',
         {'fields': ('sample',)}),
        ('Sequencing Facilities',
         {'fields': ('sequencing_facility', 'array_analysis_facility', 'whole_genome_sequencing_facility')}),
        ('Sequencing',
         {'fields': ('sequencer', 'run_number', 'flow_cell_id', 'DNA_extraction_protocol', 'passage_number')}),
    ]

    list_display = ('sample', 'sequencer', 'flow_cell_id', 'run_number', 'passage_number')
    search_fields = ('sample__bpa_id__bpa_id', 'sample__name', 'flow_cell_id', 'run_number')
    list_filter = ('sequencing_facility',)


admin.site.register(MelanomaRun, MelanomaRunAdmin)


class TumorStageAdmin(admin.ModelAdmin):
    class Form(forms.ModelForm):
        class Meta:
            model = TumorStage
            widgets = {
                'note': AutosizedTextarea(attrs={'class': 'input-large',
                                                 'style': 'width:95%'})
            }

    form = Form


admin.site.register(TumorStage, TumorStageAdmin)

admin.site.register(MelanomaSequenceFile, SequenceFileAdmin)
    
    


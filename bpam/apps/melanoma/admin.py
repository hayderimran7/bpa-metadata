from django.contrib import admin
from django import forms
from apps.common.admin import SequenceFileAdmin

from models import (TumorStage,
                    Array,
                    MelanomaSample,
                    MelanomaRun,
                    MelanomaSequenceFile,
                    MelanomaProtocol,
                    )


class ProtocolInline(admin.StackedInline):
    model = MelanomaProtocol
    extra = 0


class MelanomaRunAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Sample',
         {'fields': ('sample',)}),
        ('Sequencing Facilities',
         {'fields': (('sequencing_facility', 'array_analysis_facility', 'whole_genome_sequencing_facility'))}),
        ('Sequencing',
         {'fields': (('sequencer', 'run_number', 'flow_cell_id'), 'DNA_extraction_protocol', 'passage_number')}),
    ]

    inlines = (ProtocolInline, )
    list_display = ('sample', 'sequencer', 'flow_cell_id', 'run_number', 'passage_number')
    search_fields = ('sample__bpa_id__bpa_id', 'sample__name', 'flow_cell_id', 'run_number')
    list_filter = ('sequencing_facility',)


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
        ('Source Data Note',
         {'fields': ('debug_note',)}),
    ]

    list_display = ('bpa_id', 'name', 'dna_source', 'dna_extraction_protocol', 'tumor_stage')
    search_fields = ('bpa_id__bpa_id', 'name', 'tumor_stage__description')
    list_filter = ('dna_source', 'gender', 'requested_sequence_coverage',)


class ArrayAdmin(admin.ModelAdmin):
    list_display = ('bpa_id', 'array_id', 'mia_id')
    search_fields = ('bpa_id__bpa_id', 'array_id', 'mia_id')


class ProtocolAdmin(admin.ModelAdmin):
    fields = (('library_type', 'base_pairs', 'library_construction_protocol'), 'note')
    search_fields = ('library_type', 'library_construction_protocol', 'note', 'run__sample__bpa_id__bpa_id', 'run__sample__name')
    list_display = ('run', 'library_type', 'base_pairs', 'library_construction_protocol',)
    list_filter = ('library_type',)

admin.site.register(MelanomaProtocol, ProtocolAdmin)
admin.site.register(TumorStage)
admin.site.register(Array, ArrayAdmin)
admin.site.register(MelanomaSample, SampleAdmin)
admin.site.register(MelanomaRun, MelanomaRunAdmin)
admin.site.register(MelanomaSequenceFile, SequenceFileAdmin)
    
    


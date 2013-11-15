from django.contrib import admin
from django import forms
from apps.common.admin import SequenceFileAdmin

from .models import PathogenSample
from .models import PathogenRun
from .models import PathogenProtocol
from .models import PathogenSequenceFile


class ProtocolForm(forms.ModelForm):
    class Meta:
        model = PathogenProtocol
        widgets = {
            'library_construction_protocol': forms.TextInput(attrs={'size': 100}),
        }


class ProtocolAdmin(admin.ModelAdmin):
    form = ProtocolForm
    fields = (('library_type', 'base_pairs', 'library_construction_protocol'), 'note')
    search_fields = (
    'library_type', 'library_construction_protocol', 'note', 'run__sample__bpa_id__bpa_id', 'run__sample__name')
    list_display = ('run', 'library_type', 'base_pairs', 'library_construction_protocol',)
    list_filter = ('library_type',)


class ProtocolInline(admin.StackedInline):
    model = PathogenProtocol
    extra = 0


class RunAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Sample',
         {'fields': ('sample',)}),
        ('Sequencing Facilities',
         {'fields': (('sequencing_facility', 'array_analysis_facility', 'whole_genome_sequencing_facility'))}),
        ('Sequencing',
         {'fields': (('sequencer', 'run_number', 'flow_cell_id'), 'DNA_extraction_protocol')}),
    ]

    inlines = (ProtocolInline, )
    list_display = ('sample', 'sequencer', 'flow_cell_id', 'run_number',)
    search_fields = ('sample__bpa_id__bpa_id', 'sample__name', 'flow_cell_id', 'run_number')
    list_filter = ('sequencing_facility',)


class SampleAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Sample Identification',
         {'fields': (('bpa_id', 'name'), 'original_source_host_species')}),
        ('DNA/RNA Source',
         {'fields': (
             ('organism', 'official_variety_name', 'label'),
             'dna_source',
             'dna_extraction_protocol',
         )}),
        ('Contacts',
         {'fields': ('contact_scientist',)}),
        ('',
         {'fields': ('note',)}),
        ('Debug',
         {'fields': ('debug_note',)}),

    ]

    list_display = ('bpa_id', 'name', 'dna_source', 'dna_extraction_protocol')
    search_fields = ('bpa_id__bpa_id', 'name', 'tumor_stage__description')
    list_filter = ('dna_source', 'requested_sequence_coverage',)


class PathogenSequenceFileAdmin(SequenceFileAdmin):
    def get_organism(self, obj):
        return obj.sample.organism
    get_organism.short_description = 'Organism'
    get_organism.admin_order_field = 'sample__organism'

    list_display = ('get_sample_id', 'get_organism', 'download_field', 'get_sample_name', 'run')
    list_filter = ('sample__organism', 'analysed')

admin.site.register(PathogenSample, SampleAdmin)
admin.site.register(PathogenProtocol, ProtocolAdmin)
admin.site.register(PathogenSequenceFile, PathogenSequenceFileAdmin)
admin.site.register(PathogenRun, RunAdmin)

    
    
    


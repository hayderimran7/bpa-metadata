from django.contrib import admin
from django import forms
from apps.common.admin import SequenceFileAdmin

from .models import CollectionEvent
from .models import GBRSample
from .models import GBRRun
from .models import GBRProtocol
from .models import GBRSequenceFile


class ProtocolForm(forms.ModelForm):
    class Meta:
        model = GBRProtocol
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
    model = GBRProtocol
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
         {'fields': (('bpa_id', 'name'),)}),
        ('DNA/RNA Source',
         {'fields': (
             'organism',
             'dna_source',
             'dna_extraction_protocol',
             ('dna_concentration', 'total_dna', 'dna_rna_concentration', 'total_dna_rna_shipped'),
         )}),
        ('Sample Management',
         {'fields': (
             'dataset',
             'requested_sequence_coverage',
             'requested_read_length',
             'date_sent_to_sequencing_facility',
             'date_sequenced',
             # 'date_data_sent',
             # 'date_data_received',
             'sequencing_data_eta',
             'comments_by_facility',
             'sequencing_notes')}),
        ('Contacts',
         {'fields': ('contact_scientist', 'contact_bioinformatician')}),
        ('',
         {'fields': ('note',)}),
        ('Debug',
         {'fields': ('debug_note',)}),

    ]

    list_display = ('bpa_id', 'name', 'dna_source', 'dna_extraction_protocol')
    search_fields = ('bpa_id__bpa_id', 'name', 'tumor_stage__description')
    list_filter = ('dna_source', 'requested_sequence_coverage',)


class CollectionEventAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Collection',
         {'fields': ('name', 'collection_date', 'collector', 'gps_location')}),
        ('Site Data',
         {'fields': ('water_temp', 'water_ph', 'depth')}),
        ('Note',
         {'fields': ('note',)}),

    ]

    list_display = ('name', 'collection_date', 'collector', 'gps_location', 'water_temp', 'water_ph', 'depth')
    search_fields = ('name', 'collector', 'note')
    list_filter = ('name', )

admin.site.register(CollectionEvent, CollectionEventAdmin)
admin.site.register(GBRSample, SampleAdmin)
admin.site.register(GBRProtocol, ProtocolAdmin)
admin.site.register(GBRSequenceFile, SequenceFileAdmin)
admin.site.register(GBRRun, RunAdmin)

    
    
    


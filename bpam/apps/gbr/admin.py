from django.contrib import admin
from django import forms
from apps.common.admin import SequenceFileAdmin

from models import Collection, GBRSample, GBRRun, GBRProtocol, GBRSequenceFile


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
         {'fields': (('sequencer', 'run_number', 'flow_cell_id'), 'DNA_extraction_protocol', 'passage_number')}),
    ]
    inlines = (ProtocolInline, )
    list_display = ('sample', 'sequencer', 'flow_cell_id', 'run_number', 'passage_number')
    search_fields = ('sample__bpa_id__bpa_id', 'sample__name', 'flow_cell_id', 'run_number')
    list_filter = ('sequencing_facility', 'flow_cell_id', )


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
         {'fields': ('contact_scientist', 'contact_bioinformatician',)}),
        ('',
         {'fields': ('note',)}),
        ('Debug',
         {'fields': ('debug_note',)})

    ]

    list_display = ('bpa_id', 'name', 'dna_source', 'dna_extraction_protocol')
    search_fields = ('bpa_id__bpa_id', 'name', 'tumor_stage__description')
    list_filter = ('dna_source', 'requested_sequence_coverage',)


admin.site.register(Collection)
admin.site.register(GBRSample, SampleAdmin)
admin.site.register(GBRProtocol, ProtocolAdmin)
admin.site.register(GBRSequenceFile, SequenceFileAdmin)
admin.site.register(GBRRun, RunAdmin)

    
    
    


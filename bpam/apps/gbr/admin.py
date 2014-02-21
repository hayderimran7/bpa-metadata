from django.contrib import admin
from django import forms
from suit.widgets import LinkedSelect, AutosizedTextarea

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
            'run': LinkedSelect,
            'library_construction_protocol': forms.TextInput(attrs={'class': 'input-large', 'style': 'width:95%'}),
            'note': AutosizedTextarea(attrs={'class': 'input-large', 'style': 'width:95%'}),
        }


class ProtocolAdmin(admin.ModelAdmin):
    form = ProtocolForm
    radio_fields = {'library_type': admin.HORIZONTAL}
    fieldsets = [
        ('Protocol', {'fields': ('run', 'library_type', 'base_pairs', 'library_construction_protocol', 'note')})
    ]

    search_fields = (
        'library_type', 'library_construction_protocol', 'note', 'run__sample__bpa_id__bpa_id', 'run__sample__name')
    list_display = ('run', 'library_type', 'base_pairs', 'library_construction_protocol',)
    list_filter = ('library_type',)


class RunAdmin(admin.ModelAdmin):
    class RunForm(forms.ModelForm):
        class Meta:
            model = GBRRun
            widgets = {
                'sample': LinkedSelect(attrs={'style': 'width:50%'}),
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
         {'fields': ('sequencer', 'run_number', 'flow_cell_id', 'DNA_extraction_protocol')}),
    ]

    class ProtocolInline(admin.StackedInline):
        model = GBRProtocol
        form = ProtocolForm
        radio_fields = {'library_type': admin.HORIZONTAL}
        extra = 0
    inlines = (ProtocolInline, )

    list_display = ('sample', 'sequencer', 'flow_cell_id', 'run_number',)
    search_fields = ('sample__bpa_id__bpa_id', 'sample__name', 'flow_cell_id', 'run_number')
    list_filter = ('sequencing_facility',)


class SequenceFileInlineForm(forms.ModelForm):
    class Meta:
        model = GBRSequenceFile
        widgets = {
            'filename': forms.TextInput(attrs={'class': 'input-large',
                                               'style': 'width:100%'}),
            'md5': forms.TextInput(attrs={'class': 'input-large',
                                          'style': 'width:70%'}),
        }


class SampleAdmin(admin.ModelAdmin):
    class SampleForm(forms.ModelForm):
        class Meta:
            model = GBRSample
            widgets = {
                'bpa_id': LinkedSelect(
                    attrs={'class': 'input-medium',
                           'style': 'width:50%'}),
                'name': forms.TextInput(
                    attrs={'class': 'input-medium',
                           'style': 'width:50%'}),
                'organism': LinkedSelect,
                'dna_source': LinkedSelect,
                'sequencing_facility': LinkedSelect,
                'contact_scientist': LinkedSelect,
                'contact_bioinformatician': LinkedSelect,
                'comments_by_facility': AutosizedTextarea(
                    attrs={'class': 'input-large',
                           'style': 'width:95%'}),
                'sequencing_notes': AutosizedTextarea(
                    attrs={'class': 'input-large',
                           'style': 'width:95%'}),
                'note': AutosizedTextarea(
                    attrs={'class': 'input-large',
                           'style': 'width:95%'}),
                'debug_note': AutosizedTextarea(
                    attrs={'class': 'input-large',
                           'style': 'width:95%'})
            }

    form = SampleForm

    class SequenceFileInline(admin.TabularInline):
        model = GBRSequenceFile
        form = SequenceFileInlineForm
        sortable = 'filename'
        fields = ('filename', 'md5', 'date_received_from_sequencing_facility', 'analysed')
        extra = 1

    inlines = (SequenceFileInline, )

    fieldsets = [
        ('Sample Identification',
         {'fields': ('bpa_id', 'name',)}),
        ('DNA/RNA Source',
         {'fields': (
             'organism',
             'dna_source',
             'dna_extraction_protocol',
             'dna_concentration', 'total_dna', 'dna_rna_concentration', 'total_dna_rna_shipped',)}),
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
        ('Notes',
         {'fields': ('note', 'debug_note')}),
    ]

    list_display = ('bpa_id', 'name', 'dna_source', 'dna_extraction_protocol')
    search_fields = ('bpa_id__bpa_id', 'name',)
    list_filter = ('dna_source', 'requested_sequence_coverage',)


admin.site.register(GBRSample, SampleAdmin)


class CollectionEventAdmin(admin.ModelAdmin):
    class CollectionForm(forms.ModelForm):
        class Meta:
            model = CollectionEvent
            widgets = {
                'collector': LinkedSelect,
                'note': AutosizedTextarea(
                    attrs={'class': 'input-large',
                           'style': 'width:95%'}),
            }

    form = CollectionForm

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
admin.site.register(GBRProtocol, ProtocolAdmin)
admin.site.register(GBRSequenceFile, SequenceFileAdmin)
admin.site.register(GBRRun, RunAdmin)

    
    
    


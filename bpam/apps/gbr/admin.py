# -*- coding: utf-8 -*-

from django.contrib import admin
from django import forms
from suit.widgets import LinkedSelect, AutosizedTextarea, SuitDateWidget, EnclosedInput
from apps.common.admin import SequenceFileAdmin

from .models import CollectionSite
from .models import CollectionEvent
from .models import GBRSample
from .models import GBRRun
from .models import GBRProtocol
from .models import GBRSequenceFile


class ProtocolForm(forms.ModelForm):
    class Meta:
        fields = "__all__"
        model = GBRProtocol
        widgets = {
            'library_construction_protocol': forms.TextInput(attrs={'class': 'input-large', 'style': 'width:95%'}),
            'note': AutosizedTextarea(attrs={'class': 'input-large', 'style': 'width:95%'}),
        }


class ProtocolAdmin(admin.ModelAdmin):
    form = ProtocolForm
    radio_fields = {'library_type': admin.HORIZONTAL}
    fieldsets = [
        ('Protocol', {'fields': ('library_type', 'base_pairs_string', 'library_construction_protocol', 'note')})
    ]

    search_fields = ('library_type', 'library_construction_protocol', 'note',)
    list_display = ('library_type', 'base_pairs_string', 'library_construction_protocol',)
    list_filter = ('library_type',)


class RunAdmin(admin.ModelAdmin):
    class RunForm(forms.ModelForm):
        class Meta:
            fields = "__all__"
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
        fields = "__all__"
        model = GBRSequenceFile
        widgets = {
            'filename': forms.TextInput(attrs={'class': 'input-xxlarge'}),
            'md5': forms.TextInput(attrs={'class': 'input-xlarge'}),
            'date_received_from_sequencing_facility': SuitDateWidget,
        }


class SampleAdmin(admin.ModelAdmin):
    class SampleForm(forms.ModelForm):
        class Meta:
            fields = "__all__"
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
                           'style': 'width:95%'}),
                'dna_rna_concentration': EnclosedInput(append=u'ng/µL'),
                'date_sequenced': SuitDateWidget,
                'sequencing_data_eta': SuitDateWidget,
                'date_sent_to_sequencing_facility': SuitDateWidget

            }

    form = SampleForm

    class SequenceFileInline(admin.TabularInline):
        model = GBRSequenceFile
        form = SequenceFileInlineForm
        suit_classes = 'suit-tab suit-tab-id'
        sortable = 'filename'
        fields = ('filename', 'md5', 'date_received_from_sequencing_facility', )
        extra = 0

    inlines = (SequenceFileInline, )

    suit_form_tabs = (
        ('id', 'Sample ID and Sequence Files'),
        ('dna', 'DNA'),
        ('management', 'Sample Management',),
        ('contacts', 'Contacts',),
        ('notes', 'Source Data Note')
    )

    fieldsets = [
        ('ID',
         {'classes': ('suit-tab suit-tab-id',),
          'fields': (
              'bpa_id',
              'name',)}),
        (None,  # 'DNA/RNA Source',
         {'classes': ('suit-tab suit-tab-dna',),
          'fields': (
              'organism',
              'dna_source',
              'dna_extraction_protocol',
              'dna_rna_concentration',
              'total_dna_rna_shipped',)}),
        (None,  # 'Sample Management',
         {'classes': ('suit-tab suit-tab-management',),
          'fields': (
              'dataset',
              'requested_sequence_coverage',
              'requested_read_length',
              'date_sent_to_sequencing_facility',
              'date_sequenced',
              'sequencing_data_eta',
              'comments_by_facility',
              'sequencing_notes')}),
        (None,  # 'Contacts',
         {'classes': ('suit-tab suit-tab-contacts',),
          'fields': (
              'contact_scientist',
              'contact_bioinformatician')}),
        (None,  # 'Notes',
         {'classes': ('suit-tab suit-tab-notes',),
          'fields': (
              'note',
              'debug_note')}),
    ]

    list_display = ('bpa_id', 'name', 'dna_source', 'dna_extraction_protocol')
    search_fields = ('bpa_id__bpa_id', 'name',)
    list_filter = ('dna_source', 'requested_sequence_coverage',)


admin.site.register(GBRSample, SampleAdmin)


class CollectionEventAdmin(admin.ModelAdmin):
    class CollectionForm(forms.ModelForm):
        class Meta:
            fields = "__all__"
            model = CollectionEvent
            widgets = {
                'site': LinkedSelect,
                'water_temp': EnclosedInput(append=u'°C'),
                'water_ph': EnclosedInput(append='pH'),
                'depth': EnclosedInput(append='m'),
                'collection_date': SuitDateWidget,
                'collector': LinkedSelect,
                'note': AutosizedTextarea(
                    attrs={'class': 'input-large',
                           'style': 'width:95%'}),
            }

    form = CollectionForm
    fieldsets = [
        ('Collection',
         {'fields': (
             'collection_date',
             'collector',
         ),
         }),
        ('Site Data',
         {'fields': (
             'water_temp',
             'water_ph',
             'depth')}),
        ('Note',
         {'fields': ('note',)}),

    ]

    list_display = ('site', 'collection_date', 'collector', 'water_temp', 'water_ph', 'depth')
    search_fields = ('site', 'collector', 'note')
    list_filter = ('site', 'collector', 'note')


class SiteAdmin(admin.ModelAdmin):
    class CollectionForm(forms.ModelForm):
        class Meta:
            fields = "__all__"
            model = CollectionSite
            widgets = {
                'site_name': AutosizedTextarea(
                    attrs={'class': 'input-large',
                           'style': 'width:95%'}),
                'lat': EnclosedInput(prepend='icon-map-marker'),
                'lon': EnclosedInput(prepend='icon-map-marker'),
                'note': AutosizedTextarea(
                    attrs={'class': 'input-large',
                           'style': 'width:95%'}),
            }

    form = CollectionForm
    fieldsets = [
        ('Collection',
         {'fields': (
             'site_name',
             'lat',
             'lon'), }),
        ('Note',
         {'fields': ('note',)}),

    ]

    list_display = ('site_name', 'lat', 'lon', 'note')
    search_fields = ('site_name', 'lat', 'lon', 'note')
    list_filter = ('site_name', 'lat', 'lon',)

admin.site.register(CollectionSite, SiteAdmin)
admin.site.register(CollectionEvent, CollectionEventAdmin)
admin.site.register(GBRProtocol, ProtocolAdmin)
admin.site.register(GBRSequenceFile, SequenceFileAdmin)
admin.site.register(GBRRun, RunAdmin)

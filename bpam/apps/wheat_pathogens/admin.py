from django.contrib import admin
from django import forms
from suit.widgets import LinkedSelect, AutosizedTextarea, SuitDateWidget

from apps.common.admin import SequenceFileAdmin
from .models import PathogenSample
from .models import PathogenRun
from .models import PathogenProtocol
from .models import PathogenSequenceFile


class ProtocolForm(forms.ModelForm):
    class Meta:
        model = PathogenProtocol
        widgets = {
            'run': LinkedSelect,
            'library_construction_protocol': LinkedSelect,
            'note': AutosizedTextarea(attrs={'class': 'input-large',
                                             'style': 'width:95%'})
        }


class ProtocolAdmin(admin.ModelAdmin):
    form = ProtocolForm
    radio_fields = {'library_type': admin.HORIZONTAL}
    fields = ('run', 'library_type', 'base_pairs', 'library_construction_protocol', 'note')
    search_fields = ('library_type', 'library_construction_protocol', 'note', 'run__sample__bpa_id__bpa_id',
                     'run__sample__name')
    list_display = ('run', 'library_type', 'base_pairs', 'library_construction_protocol',)
    list_filter = ('library_type',)


class RunAdmin(admin.ModelAdmin):
    class RunForm(forms.ModelForm):
        class Meta:
            model = PathogenRun
            widgets = {
                'sample': LinkedSelect,
                'sequencing_facility': LinkedSelect,
                'array_analysis_facility': LinkedSelect,
                'whole_genome_sequencing_facility': LinkedSelect,
                'sequencer': LinkedSelect
            }

    form = RunForm

    class ProtocolInline(admin.StackedInline):
        form = ProtocolForm
        model = PathogenProtocol
        radio_fields = {'library_type': admin.HORIZONTAL}
        extra = 0

    inlines = (ProtocolInline, )

    fieldsets = [
        ('Sample',
         {'fields': ('sample',)}),
        ('Sequencing Facilities',
         {'fields': ('sequencing_facility', 'array_analysis_facility', 'whole_genome_sequencing_facility')}),
        ('Sequencing',
         {'fields': ('sequencer', 'run_number', 'flow_cell_id', 'DNA_extraction_protocol')}),
    ]

    list_display = ('sample', 'sequencer', 'flow_cell_id', 'run_number',)
    search_fields = ('sample__bpa_id__bpa_id', 'sample__name', 'flow_cell_id', 'run_number')
    list_filter = ('run_number', )


class SequenceFileInlineForm(forms.ModelForm):
    class Meta:
        model = PathogenSequenceFile
        widgets = {
            'filename': forms.TextInput(attrs={'class': 'input-xxlarge'}),
            'md5': forms.TextInput(attrs={'class': 'input-xlarge'}),
            'date_received_from_sequencing_facility': SuitDateWidget,
        }


class SampleAdmin(admin.ModelAdmin):
    class SequenceFileInline(admin.TabularInline):
        model = PathogenSequenceFile
        form = SequenceFileInlineForm
        suit_classes = 'suit-tab suit-tab-id'
        sortable = 'filename'
        fields = ('filename', 'md5', 'date_received_from_sequencing_facility',)
        extra = 0

    inlines = (SequenceFileInline, )

    class SampleForm(forms.ModelForm):
        class Meta:
            model = PathogenSample
            widgets = {
                'bpa_id': LinkedSelect(attrs={'style': 'width:50%'}),
                'organism': LinkedSelect,
                'dna_source': LinkedSelect,
                'sequencing_facility': LinkedSelect,
                'contact_scientist': LinkedSelect,
                'collection_date': SuitDateWidget,
                'contact_bioinformatician': LinkedSelect,
                'note': AutosizedTextarea(attrs={'class': 'input-large', 'style': 'width:95%'}),
                'collection_location': AutosizedTextarea(attrs={'class': 'input-large', 'style': 'width:95%'}),
                'debug_note': AutosizedTextarea(attrs={'class': 'input-large', 'style': 'width:95%'})
            }

    form = SampleForm

    suit_form_tabs = (
        ('id', 'Sample ID and Sequence Files'),
        ('dna', 'DNA/RNA'),
        ('collection', 'Collection'),
        ('contacts', 'Contacts'),
        ('notes', 'Notes')
    )

    fieldsets = [
        (None,  # 'Sample Identification',
         {'classes': ('suit-tab suit-tab-id',),
          'fields': (
              'bpa_id',
              'name',
              'sample_label',
              'original_source_host_species',
              'wheat_pathogenicity')}),
        (None,  # 'DNA/RNA Source',
         {'classes': ('suit-tab suit-tab-dna',),
          'fields': (
              'organism',
              'official_variety_name',
              'dna_source',
              'dna_extraction_protocol',)}),
        (None,  # 'Collection',
         {'classes': ('suit-tab suit-tab-collection',),
          'fields': (
              'collection_location',
              'collection_date',)}),
        (None,  # 'Contacts',
         {'classes': ('suit-tab suit-tab-contacts',),
          'fields': ('contact_scientist',)}),
        (None,  # 'Notes',
         {'classes': ('suit-tab suit-tab-notes',),
          'fields': (
              'note',
              'debug_note',)}),

    ]

    list_display = ('bpa_id', 'name', 'official_variety_name', 'dna_source', 'dna_extraction_protocol')
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

    
    
    


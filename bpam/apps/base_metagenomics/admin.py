from django.contrib import admin
from django import forms
from suit.widgets import LinkedSelect, AutosizedTextarea, SuitDateWidget

from apps.common.admin import SequenceFileAdmin
from models import (MetagenomicsSequenceFile,
                    MetagenomicsSample,
                    MetagenomicsRun, )

admin.site.register(MetagenomicsSequenceFile, SequenceFileAdmin)


class SequenceFileInlineForm(forms.ModelForm):
    class Meta:
        fields = "__all__"
        model = MetagenomicsSequenceFile
        widgets = {
            'filename': forms.TextInput(attrs={'class': 'input-xxlarge'}),
            'md5': forms.TextInput(attrs={'class': 'input-xlarge'}),
            'date_received_from_sequencing_facility': SuitDateWidget,
        }


class SampleAdmin(admin.ModelAdmin):
    class SampleForm(forms.ModelForm):
        class Meta:
            fields = "__all__"
            model = MetagenomicsSample
            widgets = {
                'bpa_id': LinkedSelect(attrs={'class': 'input-medium',
                                              'style': 'width:50%'}),
                'name': forms.TextInput(attrs={'class': 'input-medium',
                                               'style': 'width:50%'}),
                'sequencing_facility': LinkedSelect,
                'note': AutosizedTextarea(attrs={'class': 'input-large',
                                                 'style': 'width:95%'}),
                'debug_note': AutosizedTextarea(attrs={'class': 'input-large',
                                                       'style': 'width:95%'}),
                'date_sent_to_sequencing_facility': SuitDateWidget
            }

    form = SampleForm

    class SequenceFileInline(admin.TabularInline):
        model = MetagenomicsSequenceFile
        form = SequenceFileInlineForm
        suit_classes = 'suit-tab suit-tab-id'
        sortable = 'filename'
        fields = ('filename', 'md5', 'date_received_from_sequencing_facility')
        extra = 0

    inlines = (SequenceFileInline, )

    suit_form_tabs = (('id', 'Sample ID and Sequence Files'), ('management', 'Management'), ('contacts', 'Contacts'),
                      ('notes', 'Notes'))

    fieldsets = [
        (None,  # 'Sample Identification',
         {'classes': ('suit-tab suit-tab-id', ),
          'description': 'Sample Identification Detail',
          'fields': ('bpa_id',
                     'name', )}),
        (None,  # 'Sample Management',
         {'classes': ('suit-tab suit-tab-management', ),
          'description': 'Sample Management Detail',
          'fields': ('requested_sequence_coverage',
                     'date_sent_to_sequencing_facility', )}),
        (None,  # 'Contacts',
         {'classes': ('suit-tab suit-tab-contacts', ),
          'description': 'Contacts associated with this sample',
          'fields': ('contact_scientist', )}),
        (None,  # 'Notes',
         {'classes': ('suit-tab suit-tab-notes', ),
          'description': 'Motes',
          'fields': ('note', 'debug_note')}),
    ]

    list_display = ('bpa_id', 'name', 'dna_extraction_protocol')
    search_fields = ('bpa_id__bpa_id', 'name')
    list_filter = ('bpa_id', 'name', 'dna_extraction_protocol')


admin.site.register(MetagenomicsSample, SampleAdmin)


class MetagenomicsRunAdmin(admin.ModelAdmin):
    class RunForm(forms.ModelForm):
        class Meta:
            fields = "__all__"
            model = MetagenomicsRun
            widgets = {
                'sample': LinkedSelect(attrs={'style': 'width:50%'}),
                'sequencing_facility': LinkedSelect,
                'array_analysis_facility': LinkedSelect,
                'whole_genome_sequencing_facility': LinkedSelect,
                'sequencer': LinkedSelect
            }

    form = RunForm
    fieldsets = [
        ('Sample', {'fields': ('sample', )}),
        ('Sequencing Facilities',
         {'fields': ('sequencing_facility', 'array_analysis_facility', 'whole_genome_sequencing_facility')}),
        ('Sequencing', {'fields': ('sequencer', 'run_number', 'flow_cell_id', 'DNA_extraction_protocol')}),
    ]

    list_display = ('sample',
                    'sequencer',
                    'flow_cell_id',
                    'run_number', )
    search_fields = ('sample__bpa_id__bpa_id', 'sample__name', 'flow_cell_id', 'run_number')
    list_filter = ('sequencing_facility', )


admin.site.register(MetagenomicsRun, MetagenomicsRunAdmin)

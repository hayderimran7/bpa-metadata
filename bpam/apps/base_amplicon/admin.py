from django.contrib import admin
from django import forms
from suit.widgets import LinkedSelect, AutosizedTextarea, SuitDateWidget

from apps.common.admin import SequenceFileAdmin
from models import *


admin.site.register(AmpliconSequenceFile, SequenceFileAdmin)


class SequenceFileInlineForm(forms.ModelForm):
    class Meta:
        model = AmpliconSequenceFile
        widgets = {
            'filename': forms.TextInput(attrs={'class': 'input-xxlarge'}),
            'md5': forms.TextInput(attrs={'class': 'input-xlarge'}),
            'date_received_from_sequencing_facility': SuitDateWidget,
        }


class SampleAdmin(admin.ModelAdmin):
    class SampleForm(forms.ModelForm):
        class Meta:
            model = AmpliconSequencingMetadata
            widgets = {
                'bpa_id': LinkedSelect(
                    attrs={'class': 'input-medium',
                           'style': 'width:50%'}),
                'name': forms.TextInput(
                    attrs={'class': 'input-medium',
                           'style': 'width:50%'}),
                'note': AutosizedTextarea(
                    attrs={'class': 'input-large',
                           'style': 'width:95%'}),
                'debug_note': AutosizedTextarea(
                    attrs={'class': 'input-large',
                           'style': 'width:95%'}),
                'sequencing_facility': LinkedSelect,
                'date_sent_to_sequencing_facility': SuitDateWidget
            }

    form = SampleForm

    class SequenceFileInline(admin.TabularInline):
        model = AmpliconSequenceFile
        form = SequenceFileInlineForm
        sortable = 'filename'
        fields = ('filename', 'md5', 'date_received_from_sequencing_facility')
        suit_classes = 'suit-tab suit-tab-id'
        extra = 1

    inlines = (SequenceFileInline, )

    suit_form_tabs = (
        ('id', 'Sample ID and Sequence Files'),
        ('management', 'Sample Management',),
        ('notes', 'Source Data Note')
    )

    fieldsets = [
        (None,  #  'Sample Identification',
         {'classes': ('suit-tab suit-tab-id',),
          'fields': (
              'bpa_id',
              'name',
              'sample_extraction_id')}),
        (None,  # 'Sample Management',
         {'classes': ('suit-tab suit-tab-management',),
          'fields': (
              'sequencing_facility',
              'date_sent_to_sequencing_facility',
              'target',
              'index',
              'reads',
              'pcr_1_to_10',
              'pcr_1_to_100',
              'pcr_neat',
              'dilution',
              'analysis_software_version')}),
        (None,  # 'Notes',
         {'classes': ('suit-tab suit-tab-notes',),
          'fields': (
              'note',
              'debug_note')}),
    ]

    list_display = ('bpa_id', 'name', 'target', 'sequencing_facility')
    search_fields = ('bpa_id', 'sequencing_facility')
    list_filter = ('bpa_id', 'sequencing_facility', )


admin.site.register(AmpliconSequencingMetadata, SampleAdmin)


class AmpliconRunAdmin(admin.ModelAdmin):
    class RunForm(forms.ModelForm):
        class Meta:
            model = AmpliconRun
            widgets = {
                'sample': LinkedSelect(attrs={'style': 'width:50%'}),
                'sequencing_facility': LinkedSelect,
                'sequencer': LinkedSelect
            }

    form = RunForm

    fieldsets = [
        ('Sample',
         {'fields': ('sample',)}),
        ('Sequencing',
         {'fields': (
             'sequencing_facility',
             'sequencer',
             'run_number',
             'flow_cell_id',
         )}),
    ]

    list_display = ('sample', 'sequencer', 'flow_cell_id', 'run_number',)
    search_fields = ('sample__bpa_id__bpa_id', 'sample__name', 'flow_cell_id', 'run_number')
    list_filter = ('sequencing_facility',)


admin.site.register(AmpliconRun, AmpliconRunAdmin)


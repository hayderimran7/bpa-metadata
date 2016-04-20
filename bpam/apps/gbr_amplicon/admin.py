from django.contrib import admin
from django import forms
from suit.widgets import LinkedSelect, AutosizedTextarea, SuitDateWidget
from apps.common.admin import SequenceFileAdmin

from models import AmpliconSequenceFile, AmpliconSequencingMetadata


class AmpliconSequenceFileAdmin(SequenceFileAdmin):
    # removed run
    fieldsets = [
        ('Sequence File',
         {'fields': (
             'filename', 'md5', 'sample', 'lane_number', 'index_number', 'analysed',
             'date_received_from_sequencing_facility', 'note'), }),
    ]

    list_display = ('get_sample_id', 'download_field', 'get_sample_name', 'date_received_from_sequencing_facility',)


admin.site.register(AmpliconSequenceFile, AmpliconSequenceFileAdmin)


class SequenceFileInlineForm(forms.ModelForm):

    class Meta:
        fields = "__all__"
        model = AmpliconSequenceFile
        widgets = {
            'filename': forms.TextInput(attrs={'class': 'input-xxlarge'}),
            'md5': forms.TextInput(attrs={'class': 'input-xlarge'}),
            'date_received_from_sequencing_facility': SuitDateWidget,
        }


class AmpliconMetadaAdmin(admin.ModelAdmin):

    class SampleForm(forms.ModelForm):

        class Meta:
            fields = "__all__"
            model = AmpliconSequencingMetadata
            widgets = {
                'bpa_id': LinkedSelect(
                    attrs={'class': 'input-medium',
                           'style': 'width:50%'}),
                'sample_extraction_id': forms.TextInput(
                    attrs={'class': 'input-medium',
                           'style': 'width:50%'}),
                'debug_note': AutosizedTextarea(
                    attrs={'class': 'input-large',
                           'style': 'width:95%'}),
                'comments': AutosizedTextarea(
                    attrs={'class': 'input-large',
                           'style': 'width:95%'}),
                'sequencing_facility': LinkedSelect,
            }

    form = SampleForm

    class SequenceFileInline(admin.TabularInline):
        model = AmpliconSequenceFile
        form = SequenceFileInlineForm
        sortable = 'filename'
        fields = ('filename', 'md5',)
        suit_classes = 'suit-tab suit-tab-id'
        extra = 1

    inlines = (SequenceFileInline, )

    suit_form_tabs = (
        ('id', 'Sample ID and Sequence Files'),
        ('management', 'Sample Management',),
        ('notes', 'Source Data Note'),
    )

    fieldsets = [
        (None,  # 'Sample Identification',
         {'classes': ('suit-tab suit-tab-id',),
          'fields': (
              'bpa_id',
              'sample_extraction_id')}),
        (None,  # 'Sample Management',
         {'classes': ('suit-tab suit-tab-management',),
          'fields': (
              'sequencing_facility',
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
              'debug_note',
              'comments')}),
    ]

    list_display = ('bpa_id', 'target', 'sequencing_facility')
    search_fields = ('bpa_id', 'sequencing_facility')
    list_filter = ('bpa_id', 'sequencing_facility', )

admin.site.register(AmpliconSequencingMetadata, AmpliconMetadaAdmin)

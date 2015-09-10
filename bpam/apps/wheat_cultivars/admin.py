from django.contrib import admin
from django import forms
from suit.widgets import LinkedSelect, AutosizedTextarea, SuitDateWidget

from apps.common.admin import SequenceFileAdmin
from .models import CultivarSample
from .models import Protocol
from .models import CultivarSequenceFile


class ProtocolForm(forms.ModelForm):
    class Meta:
        fields = "__all__"
        model = Protocol
        widgets = {
            'library_construction_protocol': LinkedSelect,
            'note': AutosizedTextarea(attrs={'class': 'input-large',
                                             'style': 'width:95%'})
        }


class ProtocolAdmin(admin.ModelAdmin):
    form = ProtocolForm
    radio_fields = {'library_type': admin.HORIZONTAL}
    fields = ('library_type', 'base_pairs', 'library_construction_protocol', 'note')
    search_fields = ('library_type', 'library_construction_protocol', 'note',)
    list_display = ('library_type', 'base_pairs', 'library_construction_protocol',)
    list_filter = ('library_type',)




class SequenceFileInlineForm(forms.ModelForm):
    class Meta:
        fields = "__all__"
        model = CultivarSequenceFile
        widgets = {
            'filename': forms.TextInput(attrs={'class': 'input-xxlarge'}),
            'md5': forms.TextInput(attrs={'class': 'input-xlarge'}),
            'date_received_from_sequencing_facility': SuitDateWidget,
        }


class SampleAdmin(admin.ModelAdmin):
    class SampleForm(forms.ModelForm):
        class Meta:
            fields = "__all__"
            model = CultivarSample
            widgets = {
                'bpa_id': LinkedSelect,
                'organism': LinkedSelect,
                'dna_source': LinkedSelect,
                'sequencing_facility': LinkedSelect,
                'contact_scientist': LinkedSelect,
                'contact_bioinformatician': LinkedSelect,
                'note': AutosizedTextarea(attrs={'class': 'input-large',
                                                 'style': 'width:95%'}),
                'debug_note': AutosizedTextarea(attrs={'class': 'input-large',
                                                       'style': 'width:95%'})
            }

    form = SampleForm

    class SequenceFileInline(admin.TabularInline):
        model = CultivarSequenceFile
        form = SequenceFileInlineForm
        suit_classes = 'suit-tab suit-tab-id'
        sortable = 'filename'
        fields = ('filename', 'md5', 'date_received_from_sequencing_facility',)
        extra = 0

    inlines = (SequenceFileInline, )

    suit_form_tabs = (
        ('id', 'Sample ID and Sequence Files'),
        ('dna', 'DNA'),
        ('notes', 'Source Data Note')
    )

    fieldsets = [
        (None,  # 'Sample Identification',
         {'classes': ('suit-tab suit-tab-id',),
          'fields': (
              'bpa_id',
              'name',
              'cultivar_code',
              'extract_name',
              'casava_version',)}),
        (None,  # 'DNA/RNA Source',
         {'classes': ('suit-tab suit-tab-dna',),
          'fields': (
              'dna_extraction_protocol',
              'protocol_reference',)}),
        (None,  # 'Notes',
         {'classes': ('suit-tab suit-tab-notes',),
          'fields': (
              'note',
              'debug_note')}),
    ]

    list_display = ('bpa_id', 'name', 'dna_extraction_protocol')
    search_fields = ('bpa_id__bpa_id', 'cultivar_code', 'name', )
    list_filter = ('cultivar_code',)


class CultivarsSequenceFileAdmin(SequenceFileAdmin):
    search_fields = ('sample__bpa_id__bpa_id', 'sample__name')
    list_display = ('get_sample_id', 'download_field', 'get_sample_name',)
    list_filter = SequenceFileAdmin.list_filter + ('sample__cultivar_code',)


admin.site.register(CultivarSample, SampleAdmin)
admin.site.register(Protocol, ProtocolAdmin)
admin.site.register(CultivarSequenceFile, CultivarsSequenceFileAdmin)

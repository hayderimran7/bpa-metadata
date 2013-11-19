from django.contrib import admin
from django import forms
from apps.common.admin import SequenceFileAdmin

from .models import CultivarSample
from .models import CultivarRun
from .models import CultivarProtocol
from .models import CultivarSequenceFile


class ProtocolForm(forms.ModelForm):
    class Meta:
        model = CultivarProtocol
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
    model = CultivarProtocol
    extra = 0


class RunAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Sample',
         {'fields': ('sample',)}),
        ('Sequencing',
         {'fields': (('sequencer', 'run_number', 'flow_cell_id'), 'DNA_extraction_protocol')}),
    ]

    inlines = (ProtocolInline, )
    list_display = ('sample', 'sequencer', 'flow_cell_id', 'run_number',)
    search_fields = ('sample__bpa_id__bpa_id', 'sample__name', 'flow_cell_id', 'run_number')


class SampleAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Sample Identification',
         {'fields': (('bpa_id', 'name', 'cultivar_code', 'extract_name', 'casava_version'),)}),
        ('DNA/RNA Source',
         {'fields': (
             'dna_extraction_protocol', 'protocol_reference',
         )}),
        ('',
         {'fields': ('note',)}),
        ('Debug',
         {'fields': ('debug_note',)}),

    ]

    list_display = ('bpa_id', 'name', 'dna_source', 'dna_extraction_protocol')
    search_fields = ('bpa_id__bpa_id', 'cultivar_code')


class CultivarsSequenceFileAdmin(SequenceFileAdmin):
    fieldsets = [
        (None,
         {'fields': (
             'sample',
             ('filename', 'md5'), ('lane_number', 'index_number'), 'analysed',
             'note'), }),
    ]

    search_fields = ('sample__bpa_id__bpa_id', 'sample__name')

    list_display = ('get_sample_id', 'download_field', 'get_sample_name', 'run')
    list_filter = ('sample__cultivar_code',)



admin.site.register(CultivarSample, SampleAdmin)
admin.site.register(CultivarProtocol, ProtocolAdmin)
admin.site.register(CultivarSequenceFile, CultivarsSequenceFileAdmin)
admin.site.register(CultivarRun, RunAdmin)

    
    
    


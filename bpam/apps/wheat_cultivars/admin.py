from django.contrib import admin
from django import forms
from suit.widgets import LinkedSelect, AutosizedTextarea

from apps.common.admin import SequenceFileAdmin
from .models import CultivarSample
from .models import CultivarRun
from .models import CultivarProtocol
from .models import CultivarSequenceFile


class ProtocolForm(forms.ModelForm):
    class Meta:
        model = CultivarProtocol
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


class RunForm(forms.ModelForm):
    class Meta:
        model = CultivarRun
        widgets = {
            'sample': LinkedSelect,
            'sequencing_facility': LinkedSelect,
            'array_analysis_facility': LinkedSelect,
            'whole_genome_sequencing_facility': LinkedSelect,
            'sequencer': LinkedSelect
        }


class RunAdmin(admin.ModelAdmin):
    form = RunForm
    fieldsets = [
        ('Sample',
         {'fields': ('sample',)}),
        ('Sequencing',
         {'fields': ('sequencer', 'run_number', 'flow_cell_id', 'DNA_extraction_protocol')}),
    ]

    class ProtocolInline(admin.StackedInline):
        form = ProtocolForm
        model = CultivarProtocol
        radio_fields = {'library_type': admin.HORIZONTAL}
        extra = 0

    inlines = (ProtocolInline, )
    list_display = ('sample', 'sequencer', 'flow_cell_id', 'run_number',)
    search_fields = ('sample__bpa_id__bpa_id', 'sample__name', 'flow_cell_id', 'run_number')


class SampleAdmin(admin.ModelAdmin):
    class SampleForm(forms.ModelForm):
        class Meta:
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

    fieldsets = [
        ('Sample Identification',
         {'fields': ('bpa_id', 'name', 'cultivar_code', 'extract_name', 'casava_version',)}),
        ('DNA/RNA Source',
         {'fields': (
             'dna_extraction_protocol', 'protocol_reference',
         )}),
        ('Notes',
         {'fields': ('note', 'debug_note')}),
    ]

    list_display = ('bpa_id', 'name', 'dna_source', 'dna_extraction_protocol')
    search_fields = ('bpa_id__bpa_id', 'cultivar_code')
    list_filter = ('cultivar_code', 'note')


class CultivarsSequenceFileAdmin(SequenceFileAdmin):
    search_fields = ('sample__bpa_id__bpa_id', 'sample__name')
    list_display = ('get_sample_id', 'download_field', 'get_sample_name', 'run')
    list_filter = SequenceFileAdmin.list_filter + ('sample__cultivar_code',)


admin.site.register(CultivarSample, SampleAdmin)
admin.site.register(CultivarProtocol, ProtocolAdmin)
admin.site.register(CultivarSequenceFile, CultivarsSequenceFileAdmin)
admin.site.register(CultivarRun, RunAdmin)

    
    
    


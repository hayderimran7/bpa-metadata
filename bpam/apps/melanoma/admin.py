from django.contrib import admin
from django import forms

from models import (TumorStage,
                    Array,
                    MelanomaSample,
                    MelanomaRun,
                    MelanomaSequenceFile,
                    MelanomaProtocol,
                    )


class SequenceFileForm(forms.ModelForm):
    class Meta:
        model = MelanomaSequenceFile
        widgets = {
            'filename': forms.TextInput(attrs={'size': 100}),
        }


class MelanomaSequenceFileAdmin(admin.ModelAdmin):
    form = SequenceFileForm

    fieldsets = [
        (None,
         {'fields': (
             ('filename', 'md5'), ('lane_number', 'index_number'), 'analysed', 'date_received_from_sequencing_facility',
             'note'), }),
    ]

    search_fields = ('sample__bpa_id__bpa_id', 'sample__name')

    def download_field(self, obj):
        if obj.link_ok():
            return '<a href="%s">%s</a>' % (obj.url, obj.filename)
        else:
            return '<a style="color:grey">%s</a>' % obj.filename

    download_field.allow_tags = True
    download_field.short_description = 'Filename'

    list_display = (
        'get_sample_id', 'download_field', 'get_sample_name', 'date_received_from_sequencing_facility', 'run')

    def get_sample_id(self, obj):
        return obj.sample.bpa_id

    get_sample_id.short_description = 'BPA ID'
    get_sample_id.admin_order_field = 'sample__bpa_id'

    def get_sample_name(self, obj):
        return obj.sample.name

    get_sample_name.short_description = 'Sample Name'
    get_sample_name.admin_order_field = 'sample__name'


class ProtocolInline(admin.StackedInline):
    model = MelanomaProtocol
    extra = 0


class MelanomaRunAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Sequencing Facilities',
         {'fields': (('sequencing_facility', 'array_analysis_facility', 'whole_genome_sequencing_facility'))}),
        ('Sequencing',
         {'fields': (('sequencer', 'run_number', 'flow_cell_id'), 'DNA_extraction_protocol', 'passage_number')}),
    ]
    inlines = (ProtocolInline, )
    list_display = ('sample', 'sequencer', 'flow_cell_id', 'run_number', 'passage_number')
    search_fields = ('sample__bpa_id__bpa_id', 'sample__name', 'flow_cell_id', 'run_number')


class SampleAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Sample Identification',
         {'fields': (('bpa_id', 'name'))}),
        ('DNA Source',
         {'fields': (
             'organism', 'dna_source', 'dna_extraction_protocol', 'gender', 'tumor_stage', 'histological_subtype')}),
        ('Sample Management',
         {'fields': (
             'requested_sequence_coverage', 'date_sent_to_sequencing_facility', 'contact_scientist',
             'note')}),
    ]

    list_display = ('bpa_id', 'name', 'dna_source', 'dna_extraction_protocol', 'tumor_stage')
    search_fields = ('bpa_id__bpa_id', 'name', 'tumor_stage__description')


class ArrayAdmin(admin.ModelAdmin):
    list_display = ('bpa_id', 'array_id', 'mia_id')
    search_fields = ('bpa_id__bpa_id', 'array_id', 'mia_id')


class ProtocolAdmin(admin.ModelAdmin):
    fields = (('library_type', 'base_pairs', 'library_construction_protocol'), 'note')
    list_display = ('run', 'library_type', 'base_pairs', 'library_construction_protocol',)

admin.site.register(MelanomaProtocol, ProtocolAdmin)
admin.site.register(TumorStage)
admin.site.register(Array, ArrayAdmin)
admin.site.register(MelanomaSample, SampleAdmin)
admin.site.register(MelanomaRun, MelanomaRunAdmin)
admin.site.register(MelanomaSequenceFile, MelanomaSequenceFileAdmin)
    
    


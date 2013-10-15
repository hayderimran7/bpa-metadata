from django.contrib import admin
from models import (TumorStage,
                    Array,
                    MelanomaSample,
                    MelanomaRun,
                    MelanomaSequenceFile,
                    )


class MelanomaSequenceFileAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,
         {'fields': [('filename', 'md5'), ('lane_number', 'index_number'), 'analysed', 'date_received_from_sequencing_facility', 'note']}),
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


class MelanomaRunAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Facilities',
         {'fields': [('sequencing_facility', 'array_analysis_facility', 'whole_genome_sequencing_facility')]}),
        ('Sequencing',
         {'fields': ['protocol', ('sequencer', 'run_number', 'flow_cell_id'), 'DNA_extraction_protocol', 'passage_number']}),
    ]

    list_display = ('sample', 'sequencer', 'flow_cell_id', 'run_number', 'passage_number')
    search_fields = ('sample__bpa_id__bpa_id', 'sample__name', 'flow_cell_id', 'run_number')


class SampleAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Sample Identification',
         {'fields': [('bpa_id', 'name')]}),
        ('Source',
         {'fields': ['organism', 'dna_source', 'dna_extraction_protocol', 'gender', 'tumor_stage', 'histological_subtype']}),
        ('Facilities',
         {'fields': ['sequencing_facility', 'array_analysis_facility', 'whole_genome_sequencing_facility']}),
        (None,
         {'fields': ['requested_sequence_coverage', 'protocol', 'date_sent_to_sequencing_facility', 'contact_scientist', 'note']}),
    ]

    list_display = ('bpa_id', 'name', 'dna_source', 'dna_extraction_protocol', 'tumor_stage')
    search_fields = ('bpa_id__bpa_id', 'name')


class ArrayAdmin(admin.ModelAdmin):
    list_display = ('bpa_id', 'array_id', 'mia_id')
    search_fields = ('bpa_id__bpa_id', 'array_id', 'mia_id')


admin.site.register(TumorStage)
admin.site.register(Array, ArrayAdmin)
admin.site.register(MelanomaSample, SampleAdmin)
admin.site.register(MelanomaRun, MelanomaRunAdmin)
admin.site.register(MelanomaSequenceFile, MelanomaSequenceFileAdmin)
    
    


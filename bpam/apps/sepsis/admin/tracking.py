# -*- coding: utf-8 -*-

from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields, widgets

# import export fields
from commonfields import DateField
from sample import SepsisSampleField

from ..models import SampleTrack
from ..models import SepsisSample

# 5 digit BPA ID
# Taxon_OR_organism
# Strain_OR_isolate
# Serovar
# Growth Media
# Replicate
# Omics
# Analytical platform
# Facility
# Work order
# Contextual Data Submission Date
# Sample submission FIXME, no need for flag if date is set, date is flag
# Sample submission date
# Data generated
# Archive ID
# Archive Ingestion Date

track_data = ('bpa_id',
              'taxon_or_organism',
              'strain_or_isolate',
              'serovar',
              'growth_media',
              'replicate',
              'omics',
              'analytical_platform',
              'facility',
              'work_order',
              'contextual_data_submission_date',
              'sample_submission_date',
              'data_generated',
              'archive_ingestion_date',
              'dataset_url',
)

class SampleTrackResource(resources.ModelResource):
    """Sample tracking mappings"""

    bpa_id = fields.Field(attribute='bpa_id', column_name='5 digit BPA ID')
    taxon_or_organism = fields.Field(attribute='taxon_or_organism', column_name='Taxon_OR_organism')
    strain_or_isolate = fields.Field(attribute='strain_or_isolate', column_name='Strain_OR_isolate')
    serovar = fields.Field(attribute='serovar', column_name='Serovar')
    growth_media = fields.Field(attribute='growth_media', column_name='Growth Media')
    replicate = fields.Field(attribute='replicate', column_name='Replicate')
    omics = fields.Field(attribute='omics', column_name='Omics')

    analytical_platform = fields.Field(attribute='analytical_platform', column_name='Analytical Platform')
    facility = fields.Field(attribute='facility', column_name='Facility')
    work_order = fields.Field(attribute='work_order', column_name='Work order')
    contextual_data_submission_date = DateField(attribute='contextual_data_submission_date', widget=widgets.DateWidget(format="%Y-%m-%d"), column_name='Contextual Data Submission Date')
    sample_submission_date = DateField(attribute='sample_submission_date', widget=widgets.DateWidget(format="%Y-%m-%d"), column_name='Sample submission Date')
    data_generated = fields.Field(attribute='data_generated',widget=widgets.BooleanWidget(), column_name='Data generated')
    archive_ingestion_date = DateField(attribute='archive_ingestion_date', widget=widgets.DateWidget(format="%Y-%m-%d") ,column_name='Sample submission Date')

    class Meta:
        import_id_fields = ('bpa_id', )
        export_order = track_data
        model = SampleTrack


class TrackAdmin(ImportExportModelAdmin):
    resource_class = SampleTrackResource
    date_hierarchy = 'sample_submission_date'
    list_display = track_data
    list_filter = ('bpa_id', 'taxon_or_organism', 'strain_or_isolate', 'omics')


admin.site.register(SampleTrack, TrackAdmin)

# -*- coding: utf-8 -*-

from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields, widgets

# import export fields
from commonfields import DateField
from sample import SepsisSampleField

from ..models import SampleTrack
from ..models import SepsisSample


class SampleTrackResource(resources.ModelResource):
    """Sample tracking mappings"""

    sample = SepsisSampleField(column_name='BPA ID',
                               attribute='sample',
                               widget=widgets.ForeignKeyWidget(SepsisSample), )

    given_to = fields.Field(attribute="given_to", column_name="Given to")
    allocation_date = DateField(widget=widgets.DateWidget(format="%d/%m/%y"),
                                attribute="allocation_date",
                                column_name="Date allocated", )

    class Meta:
        import_id_fields = ('sample', )
        model = SampleTrack


class TrackAdmin(ImportExportModelAdmin):
    resource_class = SampleTrackResource
    date_hierarchy = 'allocation_date'
    list_display = ('bpa_id',
                    'replicate',
                    'given_to',
                    'allocation_date',
                    'work_order',
                    'omics',
                    'analytical_platform',
                    'facility',
                    'sample_submission_date',
                    'contextual_data_submission_date',
                    'data_generated',
                    'archive_ingestion_date',
                    'dataset_url',
                    'curation_url', )

    list_filter = ('bpa_id',
                   'facility',
                   'replicate',
                   'data_generated',
                   'given_to',
                   'dataset_url', )


admin.site.register(SampleTrack, TrackAdmin)

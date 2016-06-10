# -*- coding: utf-8 -*-

from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields, widgets

# import export fields
from commonfields import DateField
from sample import SepsisSampleField

from ..models import (Host,
                      MiseqGenomicsMethod,
                      GenomicsMiseqFile,
                      ProteomicsMethod,
                      ProteomicsFile,
                      TranscriptomicsMethod,
                      TranscriptomicsFile,
                      SepsisSample,
                      SampleTrack,
                      GrowthMethod, )


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
    list_display = ("sample",
                    "replicate",
                    "given_to",
                    "allocation_date",
                    "work_order",
                    "omics",
                    "analytical_platform",
                    "facility",
                    "sample_submission_date",
                    "contextual_data_submission_date",
                    "data_generated",
                    "archive_ingestion_date",
                    "dataset_url",
                    "curation_url", )

    list_filter = ("sample",
                   "facility",
                   "replicate",
                   "data_generated",
                   "given_to",
                   "dataset_url", )


class SexWidget(object):
    """Sex allowed vocabulary"""

    rendermap = {"M": "Male", "F": "Female"}
    cleanmap = dict((v, k) for k, v in rendermap.iteritems())

    def clean(self, value):
        return self.cleanmap.get(value)

    def render(self, value):
        return self.rendermap.get(value)


class HostResource(resources.ModelResource):
    """Maps contextual file to host """

    strain_or_isolate = fields.Field(attribute="strain_or_isolate",
                                     column_name="Strain_OR_isolate")
    description = fields.Field(attribute="description",
                               column_name="Host_description")
    location = fields.Field(attribute="location",
                            column_name="Host_location (state, country)")
    sex = fields.Field(attribute="sex",
                       column_name="Host_sex (F/M)",
                       widget=SexWidget())
    age = fields.Field(attribute="age",
                       column_name="Host_age",
                       widget=widgets.IntegerWidget())
    disease_outcome = fields.Field(attribute="disease_outcome",
                                   column_name="Host_disease_outcome")
    dob = DateField(widget=widgets.DateWidget(format="%d/%m/%y"),
                    attribute="dob",
                    column_name="Host_DOB (DD/MM/YY)", )

    class Meta:
        model = Host
        import_id_fields = ('strain_or_isolate', )


class HostAdmin(ImportExportModelAdmin):
    resource_class = HostResource
    list_display = ("strain_or_isolate",
                    "location",
                    "sex",
                    "age",
                    "dob",
                    "description",
                    "disease_outcome", )

    list_filter = ("location",
                   "description",
                   "sex", )

admin.site.register(Host, HostAdmin)
admin.site.register(SampleTrack, TrackAdmin)
admin.site.register(MiseqGenomicsMethod)
admin.site.register(ProteomicsMethod)
admin.site.register(ProteomicsFile)
admin.site.register(TranscriptomicsMethod)
admin.site.register(TranscriptomicsFile)

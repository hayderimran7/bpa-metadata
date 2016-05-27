# -*- coding: utf-8 -*-

from django.contrib import admin
from django import forms
from suit.widgets import LinkedSelect, AutosizedTextarea, SuitDateWidget, EnclosedInput
from apps.common.admin import SequenceFileAdmin, BPAUniqueID, BPAProject
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields, widgets
from dateutil.parser import parse as date_parser
import ingest

from .models import (
    Host,
    GenomicsMethod,
    GenomicsFile,
    ProteomicsMethod,
    ProteomicsFile,
    TranscriptomicsMethod,
    TranscriptomicsFile,
    SepsisSample,
    SampleTrack,
)

# BPA_sample_ID	Gram_staining_(positive_or_negative)
# Taxon_OR_organism
# Strain_OR_isolate
# Serovar
# Key_virulence_genes
# Strain_description
# Isolation_source
# Publication_reference
# Contact_researcher
# #Growth_condition_time
# #Growth_condition_temperature
# #Growth_condition_media
# #Experimental_replicate
# #Analytical_facility
# #Analytical_platform
# # Experimental_sample_preparation_method
# Culture_collection_ID (alternative name[s])
# Culture_collection_date (DD/MM/YY)
# Host_location (state, country)
# Host_age
# Host_DOB (DD/MM/YY)
# Host_sex (F/M)
# Host_disease_outcome
# Isolation_source
# Host_description

class BPAIDField(fields.Field):
    def __init__(self, *args, **kwargs):
        super(BPAIDField, self).__init__(*args, **kwargs)

    def clean(self, data):
        return ingest.get_bpa_id(data[self.column_name])

class DateField(fields.Field):
    """
    This field automatically parses a number of known date formats and returns
    the standard python date
    """

    def __init__(self, *args, **kwargs):
        super(DateField, self).__init__(*args, **kwargs)

    def clean(self, data):
        try:
            return ingest.get_date(data[self.column_name])
        except ValueError:
            return None

class SepsisSampleResource(resources.ModelResource):
    """Import Export Resource mappings"""

    bpa_id = BPAIDField(attribute="bpa_id", column_name="BPA ID")
    taxon_or_organism = fields.Field(attribute="taxon_or_organism", column_name="Taxon_OR_organism")
    strain_or_isolate = fields.Field(attribute="strain_or_isolate", column_name="Strain_OR_isolate")
    serovar = fields.Field(attribute="serovar", column_name="Serovar")
    key_virulence_genes = fields.Field(attribute="key_virulence_genes", column_name="Key_virulence_genes")
    strain_description = fields.Field(attribute="strain_description", column_name="Strain_description")
    isolation_source = fields.Field(attribute="isolation_source", column_name="Isolation_source")
    publication_reference = fields.Field(attribute="publication_reference", column_name="Publication_reference")
    contact_researcher = fields.Field(attribute="contact_researcher", column_name="Contact_researcher")
    culture_collection_id = fields.Field(attribute="culture_collection_id", column_name="Culture_collection_ID (alternative name[s])")
    culture_collection_date = DateField(
        widget=widgets.DateWidget(format="%d/%m/%y"),
        attribute="culture_collection_date",
        column_name="Culture_collection_date (DD/MM/YY)",
    )

    # TODO
    # growth_condition_time =
    # growth_condition_temperature =
    # growth_condition_media =
    # experimental_replicate =
    # analytical_facility =
    # analytical_platform =
    # experimental_sample_preparation_method =

    def init_instance(self, row):
        obj = self._meta.model()
        obj.host = ingest.get_host(row)
        obj.bpa_id = ingest.get_bpa_id(row.get("BPA ID"))
        return obj

    class Meta:
        import_id_fields = ('bpa_id', )
        model = SepsisSample

class SepsisSampleAdmin(ImportExportModelAdmin):
    resource_class = SepsisSampleResource

    date_hierarchy = 'culture_collection_date'

    list_display = (
        "bpa_id",
        "taxon_or_organism",
        "strain_or_isolate",
        "gram_stain",
        "serovar",
        "key_virulence_genes",
        "strain_description",
        "isolation_source",
        "publication_reference",
        "contact_researcher",
        "culture_collection_id",
        "culture_collection_date",
    )

    list_filter = (
        "bpa_id__bpa_id",
        "taxon_or_organism",
        "strain_or_isolate",
        "gram_stain",
        "serovar",
        "key_virulence_genes",
        )

class SepsisSampleField(fields.Field):
    def __init__(self, *args, **kwargs):
        super(SepsisSampleField, self).__init__(*args, **kwargs)

    def clean(self, data):
        bpaid = data[self.column_name]
        bpaid = bpaid.replace("/", ".")
        project, _ = BPAProject.objects.get_or_create(key="SEPSIS")
        bpa_id, _ = BPAUniqueID.objects.get_or_create(bpa_id=bpaid, project=project)
        sample, _ = SepsisSample.objects.get_or_create(bpa_id=bpa_id)
        return sample

class SampleTrackResource(resources.ModelResource):
    """Sample tracking mappings"""

    sample = SepsisSampleField(
        column_name='BPA ID',
        attribute='sample',
        widget=widgets.ForeignKeyWidget(SepsisSample),
    )

    given_to = fields.Field(attribute="given_to", column_name="Given to")
    allocation_date = DateField(
        widget=widgets.DateWidget(format="%d/%m/%y"),
        attribute="allocation_date",
        column_name="Date allocated",
    )


    class Meta:
        import_id_fields = ('sample', )
        model = SampleTrack

class TrackAdmin(ImportExportModelAdmin):
    resource_class = SampleTrackResource
    date_hierarchy = 'allocation_date'
    list_display = (
        "sample",
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
        "curation_url",
        )

    list_filter = (
        "sample",
        "facility",
        "replicate",
        "data_generated",
        "given_to",
        "dataset_url",
    )

class SexWidget(object):
    """Sex allowed vocabulary"""

    rendermap = {"M": "Male", "F": "Female" }
    cleanmap = dict((v, k) for k, v in rendermap.iteritems())

    def clean(self, value):
        return self.cleanmap.get(value)

    def render(self, value):
        return self.rendermap.get(value)


class HostResource(resources.ModelResource):
    """Maps contextual file to host """

    strain_or_isolate = fields.Field(attribute="strain_or_isolate", column_name="Strain_OR_isolate")
    description = fields.Field(attribute="description", column_name="Host_description")
    location = fields.Field(attribute="location", column_name="Host_location (state, country)")
    sex = fields.Field(attribute="sex", column_name="Host_sex (F/M)", widget=SexWidget())
    age = fields.Field(attribute="age", column_name="Host_age", widget=widgets.IntegerWidget())
    disease_outcome = fields.Field(attribute="disease_outcome", column_name="Host_disease_outcome")
    dob = DateField(
        widget=widgets.DateWidget(format="%d/%m/%y"),
        attribute="dob",
        column_name="Host_DOB (DD/MM/YY)",
    )

    class Meta:
        model = Host
        import_id_fields = ('strain_or_isolate', )

class HostAdmin(ImportExportModelAdmin):
    resource_class = HostResource
    list_display = (
        "strain_or_isolate",
        "location",
        "sex",
        "age",
        "dob",
        "description",
        "disease_outcome",
        )

    list_filter = (
        "location",
        "description",
        "sex",
    )


admin.site.register(Host, HostAdmin)
admin.site.register(SampleTrack, TrackAdmin)
admin.site.register(SepsisSample, SepsisSampleAdmin)
admin.site.register(GenomicsMethod)
admin.site.register(GenomicsFile)
admin.site.register(ProteomicsMethod)
admin.site.register(ProteomicsFile)
admin.site.register(TranscriptomicsMethod)
admin.site.register(TranscriptomicsFile)

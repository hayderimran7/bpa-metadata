# -*- coding: utf-8 -*-

from django.contrib import admin
from django import forms
from suit.widgets import LinkedSelect, AutosizedTextarea, SuitDateWidget, EnclosedInput
from apps.common.admin import SequenceFileAdmin, BPAUniqueID, BPAProject
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields, widgets

from .models import (
    Host,
    GenomicsMethod,
    GenomicsFile,
    ProteomicsMethod,
    ProteomicsFile,
    TranscriptomicsMethod,
    TranscriptomicsFile,
    SepsisSample,
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
        bpaid = data[self.column_name]
        bpaid = bpaid.replace("/", ".")
        project, _ = BPAProject.objects.get_or_create(key="SEPSIS")
        bpa_id, _ = BPAUniqueID.objects.get_or_create(bpa_id=bpaid, project=project)
        return bpa_id


class SepsisSampleResource(resources.ModelResource):
    """Import Export Resource mappings"""

    bpa_id = BPAIDField(attribute="bpa_id", column_name="BPA_sample_ID")
    taxon_or_organism = fields.Field(attribute="taxon_or_organism", column_name="Taxon_OR_organism")
    strain_or_isolate = fields.Field(attribute="strain_or_isolate", column_name="Strain_OR_isolate")
    serovar = fields.Field(attribute="serovar", column_name="Serovar")
    key_virolence_genes = fields.Field(attribute="key_virolence_genes", column_name="Key_virolence_genes")
    strain_description = fields.Field(attribute="strain_description", column_name="Strain_description")
    isolation_source = fields.Field(attribute="isolation_source", column_name="Isolation_source")
    publication_reference = fields.Field(attribute="publication_reference", column_name="Publication_reference")
    contact_researcher = fields.Field(attribute="contact_researcher", column_name="Contact_researcher")
    culture_collection_id = fields.Field(attribute="culture_collection_id", column_name="Culture_collection_ID (alternative name[s])")
    culture_collection_date = fields.Field(
        widget=widgets.DateWidget(format="%d/%m/%y"),
        attribute="culture_collection_date",
        column_name="Culture_collection_date (DD/MM/YY)",
    )

    # # Host
    # host_description = fields.Field(
    #     column_name='Host_description',
    #     attribute='host_description',
    #     widget=widgets.ForeignKeyWidget(Host, 'description'))

    # host_location = fields.Field(
    #     column_name='Host_location (state, country)',
    #     attribute='host_location',
    #     widget=widgets.ForeignKeyWidget(Host, 'location'))

    # host_age = fields.Field(
    #     column_name='Host_age',
    #     attribute='host_location',
    #     widget=widgets.ForeignKeyWidget(Host, 'age'))

    # host_dob = fields.Field(
    #     column_name='Host_DOB (DD/MM/YY)',
    #     attribute='host_dob',
    #     widget=widgets.ForeignKeyWidget(Host, 'dob'))

    # host_sex = fields.Field(
    #     column_name='Host_sex (M/F))',
    #     attribute='host_sex',
    #     widget=widgets.ForeignKeyWidget(Host, 'sex'))

    # host_disease_outcome = fields.Field(
    #     column_name='Host_disease_outcome)',
    #     attribute='host_disease_outcome',
    #     widget=widgets.ForeignKeyWidget(Host, 'disease_outcome'))

    # growth_condition_time =
    # growth_condition_temperature =
    # growth_condition_media =
    # experimental_replicate =
    # analytical_facility =
    # analytical_platform =
    # experimental_sample_preparation_method =

    class Meta:
        import_id_fields = ('bpa_id', )
        model = SepsisSample

class SepsisSampleAdmin(ImportExportModelAdmin):
    resource_class = SepsisSampleResource

admin.site.register(Host)
admin.site.register(SepsisSample, SepsisSampleAdmin)
admin.site.register(GenomicsMethod)
admin.site.register(GenomicsFile)
admin.site.register(ProteomicsMethod)
admin.site.register(ProteomicsFile)
admin.site.register(TranscriptomicsMethod)
admin.site.register(TranscriptomicsFile)

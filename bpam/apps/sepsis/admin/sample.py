# -*- coding: utf-8 -*-

from django.contrib import admin
from django import forms
from suit.widgets import AutosizedTextarea
from suit.widgets import SuitDateWidget
from import_export import resources, fields, widgets

from apps.common.admin import BPAUniqueID
from apps.common.admin import BPAImportExportModelAdmin

from ..models import SepsisSample
from commonfields import DateField, BPAIDField

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


class SepsisSampleField(fields.Field):
    def __init__(self, *args, **kwargs):
        super(SepsisSampleField, self).__init__(*args, **kwargs)

    def clean(self, data):
        bpaid = data[self.column_name]
        bpaid = bpaid.replace('/', '.')
        project, _ = BPAProject.objects.get_or_create(key='SEPSIS')
        bpa_id, _ = BPAUniqueID.objects.get_or_create(bpa_id=bpaid, project=project)
        sample, _ = SepsisSample.objects.get_or_create(bpa_id=bpa_id)
        return sample


class SepsisSampleResource(resources.ModelResource):
    '''Import Export Resource mappings'''

    bpa_id = BPAIDField(attribute='bpa_id', column_name='BPA ID')
    taxon_or_organism = fields.Field(attribute='taxon_or_organism', column_name='Taxon_OR_organism')
    strain_or_isolate = fields.Field(attribute='strain_or_isolate', column_name='Strain_OR_isolate')
    serovar = fields.Field(attribute='serovar', column_name='Serovar')
    key_virulence_genes = fields.Field(attribute='key_virulence_genes', column_name='Key_virulence_genes')
    strain_description = fields.Field(attribute='strain_description', column_name='Strain_description')
    isolation_source = fields.Field(attribute='isolation_source', column_name='Isolation_source')
    publication_reference = fields.Field(attribute='publication_reference', column_name='Publication_reference')
    contact_researcher = fields.Field(attribute='contact_researcher', column_name='Contact_researcher')
    culture_collection_id = fields.Field(attribute='culture_collection_id',
                                         column_name='Culture_collection_ID (alternative name[s])')
    culture_collection_date = DateField(widget=widgets.DateWidget(format='%d/%m/%y'),
                                        attribute='culture_collection_date',
                                        column_name='Culture_collection_date (DD/MM/YY)', )

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
        obj.bpa_id = ingest.get_bpa_id(row.get('BPA ID'))
        return obj

    class Meta:
        import_id_fields = ('bpa_id', )
        model = SepsisSample


class SampleForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = SepsisSample
        widgets = {
            'date_received_from_sequencing_facility': SuitDateWidget,
            'strain_description':
            forms.TextInput(attrs={'class': 'input-medium',
                                   'style': 'width:50%'}),
            'serovar': forms.TextInput(attrs={'class': 'input-medium',
                                              'style': 'width:50%'}),
        }


class SepsisSampleAdmin(BPAImportExportModelAdmin):
    form = SampleForm
    resource_class = SepsisSampleResource

    date_hierarchy = 'culture_collection_date'

    list_display = ('bpa_id',
                    'gram_stain',
                    'taxon_or_organism',
                    'strain_or_isolate',
                    'serovar',
                    'strain_description',
                    'key_virulence_genes',
                    'isolation_source',
                    'publication_reference',
                    'contact_researcher',
                    'culture_collection_id',
                    'culture_collection_date', )

    list_filter = ('bpa_id__bpa_id',
                   'taxon_or_organism',
                   'strain_or_isolate',
                   'gram_stain',
                   'serovar',
                   'key_virulence_genes', )

    fields = ('bpa_id',
              'growth_method',
              'host',
              'taxon_or_organism',
              'strain_or_isolate',
              'gram_stain',
              'serovar',
              'strain_description',
              'key_virulence_genes',
              'isolation_source',
              'publication_reference',
              'contact_researcher',
              'culture_collection_id',
              'culture_collection_date',
              'study_title',
              'investigation_type',
              'project_name',
              'sample_title',
              'ploidy',
              'num_replicons',
              'estimated_size',
              'propagation',
              'collected_by', )


admin.site.register(SepsisSample, SepsisSampleAdmin)

# -*- coding: utf-8 -*-

from django.contrib import admin
from import_export import resources, fields, widgets

# import export fields
from commonfields import DateField

from apps.common.admin import BPAImportExportModelAdmin

from ..models import (Host,
                      MiseqGenomicsMethod,
                      HiseqGenomicsMethod,
                      PacBioGenomicsMethod,
                      ProteomicsMethod,
                      ProteomicsFile,
                      TranscriptomicsMethod,
                      TranscriptomicsFile, )


class SexWidget(object):
    '''Sex allowed vocabulary'''

    rendermap = {'M': 'Male', 'F': 'Female'}
    cleanmap = dict((v, k) for k, v in rendermap.iteritems())

    def clean(self, value):
        return self.cleanmap.get(value)

    def render(self, value):
        return self.rendermap.get(value)


class HostResource(resources.ModelResource):
    '''Maps contextual file to host'''

    strain_or_isolate = fields.Field(attribute='strain_or_isolate', column_name='Strain_OR_isolate')
    description = fields.Field(attribute='description', column_name='Host_description')
    location = fields.Field(attribute='location', column_name='Host_location (state, country)')
    sex = fields.Field(attribute='sex', column_name='Host_sex (F/M)', widget=SexWidget())
    age = fields.Field(attribute='age', column_name='Host_age', widget=widgets.IntegerWidget())
    disease_outcome = fields.Field(attribute='disease_outcome', column_name='Host_disease_outcome')
    dob = DateField(widget=widgets.DateWidget(format='%d/%m/%y'),
                    attribute='dob',
                    column_name='Host_DOB (DD/MM/YY)', )

    class Meta:
        model = Host
        import_id_fields = ('strain_or_isolate', )


class HostAdmin(BPAImportExportModelAdmin):
    # FIXME
    # resource_class = HostResource # Input sheet is split into 2 models, disable until we know
    # how to do that
    list_display = ('strain_or_isolate',
                    'location',
                    'sex',
                    'age',
                    'dob',
                    'description',
                    'associated',
                    'health_state',
                    'disease_status',
                    'disease_outcome', )

    list_filter = ('location',
                   'description',
                   'sex', )


admin.site.register(Host, HostAdmin)
admin.site.register(MiseqGenomicsMethod)
admin.site.register(HiseqGenomicsMethod)
admin.site.register(PacBioGenomicsMethod)
admin.site.register(ProteomicsMethod)
admin.site.register(ProteomicsFile)
admin.site.register(TranscriptomicsMethod)
admin.site.register(TranscriptomicsFile)

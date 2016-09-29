# -*- coding: utf-8 -*-

from django.contrib import admin
from import_export import resources, fields, widgets

from apps.common.admin import BPAImportExportModelAdmin
from apps.common.models import BPAUniqueID

# import export fields
from commonfields import DateField

from ..models import PacBioTrack, MiSeqTrack, RNAHiSeqTrack, MetabolomicsTrack, DeepLCMSTrack, SWATHMSTrack

# 5 digit BPA ID
# Taxon_OR_organism
# Strain_OR_isolate
# Serovar
# Growth Media
# Replicate
# Omics
# Analytical platform
# Facility
# Work order #
# Contextual Data Submission Date
# Sample submission FIXME, no need for flag if date is set, date is flag
# Sample submission date
# Data generated
# Archive ID
# Archive Ingestion Date

BPA_ID = '102.100.100'
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


class TrackBooleanField(fields.Field):

    def __init__(self, *args, **kwargs):
        super(TrackBooleanField, self).__init__(*args, **kwargs)

    def clean(self, data):
        val = data[self.column_name]
        if val.strip().lower() == 'x':
            return True
        return False


class BPAField(fields.Field):

    def __init__(self, *args, **kwargs):
        super(BPAField, self).__init__(*args, **kwargs)

    def clean(self, data):
        bpaid = data[self.column_name]
        bpaid = '{}.{}'.format(BPA_ID, bpaid)
        # project, _ = BPAProject.objects.get_or_create(name='SEPSIS')
        # bpa_id, _ = BPAUniqueID.objects.get_or_create(bpa_id=bpaid, project=project)
        bpa_id, _ = BPAUniqueID.objects.get_or_create(bpa_id=bpaid)
        return bpa_id


class CommonSampleTrackResource(resources.ModelResource):
    """Sample tracking mappings"""

    # bpa_id = fields.Field(attribute='bpa_id', column_name='5 digit BPA ID')
    bpa_id = BPAField(attribute='bpa_id', column_name='5 digit BPA ID')
    taxon_or_organism = fields.Field(attribute='taxon_or_organism', column_name='Taxon_OR_organism')
    strain_or_isolate = fields.Field(attribute='strain_or_isolate', column_name='Strain_OR_isolate')
    serovar = fields.Field(attribute='serovar', column_name='Serovar')
    growth_media = fields.Field(attribute='growth_media', column_name='Growth Media')
    replicate = fields.Field(attribute='replicate', widget=widgets.IntegerWidget(), column_name='Replicate')
    omics = fields.Field(attribute='omics', column_name='Omics')

    analytical_platform = fields.Field(attribute='analytical_platform', column_name='Analytical platform')
    facility = fields.Field(attribute='facility', column_name='Facility')
    work_order = fields.Field(attribute='work_order', column_name='Work order #')
    contextual_data_submission_date = DateField(attribute='contextual_data_submission_date', widget=widgets.DateWidget(format="%Y-%m-%d"), column_name='Contextual Data Submission Date')
    sample_submission_date = DateField(attribute='sample_submission_date', widget=widgets.DateWidget(format="%Y-%m-%d"), column_name='Sample submission date')
    # data_generated = fields.Field(attribute='data_generated', widget=widgets.BooleanWidget(), column_name='Data generated', default=False)
    data_generated = TrackBooleanField(attribute='data_generated', widget=widgets.BooleanWidget(), column_name='Data generated', default=False)
    archive_ingestion_date = DateField(attribute='archive_ingestion_date', widget=widgets.DateWidget(format="%Y-%m-%d"), column_name='Archive Ingestion Date')
    dataset_url = fields.Field(attribute='dataset_url', column_name='Archive ID')

    class Meta:
        import_id_fields = ('bpa_id', )
        export_order = track_data


class CommonTrackAdmin(BPAImportExportModelAdmin):
    date_hierarchy = 'sample_submission_date'
    list_display = track_data
    list_filter = ('bpa_id', 'taxon_or_organism', 'strain_or_isolate', 'omics')

# PacBio


class PacBioSampleTrackResource(CommonSampleTrackResource):

    class Meta(CommonSampleTrackResource.Meta):
        model = PacBioTrack


class PacBioTrackAdmin(CommonTrackAdmin):
    resource_class = PacBioSampleTrackResource

admin.site.register(PacBioTrack, PacBioTrackAdmin)

# MiSeq


class MiSeqSampleTrackResource(CommonSampleTrackResource):

    class Meta(CommonSampleTrackResource.Meta):
        model = MiSeqTrack


class MiSeqTrackAdmin(CommonTrackAdmin):
    resource_class = MiSeqSampleTrackResource

admin.site.register(MiSeqTrack, MiSeqTrackAdmin)


# RNAHiSeq
class RNAHiSeqSampleTrackResource(CommonSampleTrackResource):

    class Meta(CommonSampleTrackResource.Meta):
        model = RNAHiSeqTrack


class RNAHiSeqTrackAdmin(CommonTrackAdmin):
    resource_class = RNAHiSeqSampleTrackResource

admin.site.register(RNAHiSeqTrack, RNAHiSeqTrackAdmin)


# Metabolomics
class MetabolomicsSampleTrackResource(CommonSampleTrackResource):

    class Meta(CommonSampleTrackResource.Meta):
        model = MetabolomicsTrack


class MetabolomicsTrackAdmin(CommonTrackAdmin):
    resource_class = MetabolomicsSampleTrackResource

admin.site.register(MetabolomicsTrack, MetabolomicsTrackAdmin)


# DeepLCMS
class DeepLCMSSampleTrackResource(CommonSampleTrackResource):

    class Meta(CommonSampleTrackResource.Meta):
        model = DeepLCMSTrack


class DeepLCMSTrackAdmin(CommonTrackAdmin):
    resource_class = DeepLCMSSampleTrackResource

admin.site.register(DeepLCMSTrack, DeepLCMSTrackAdmin)


# SWATHMSTrack
class SWATHMSSampleTrackResource(CommonSampleTrackResource):

    class Meta(CommonSampleTrackResource.Meta):
        model = SWATHMSTrack


class SWATHMSMSTrackAdmin(CommonTrackAdmin):
    resource_class = SWATHMSSampleTrackResource

admin.site.register(SWATHMSTrack, SWATHMSMSTrackAdmin)

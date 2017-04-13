# -*- coding: utf-8 -*-

from django.contrib import admin
from import_export import resources, fields, widgets

from apps.common.admin import BPAImportExportModelAdmin
from apps.common.models import BPAUniqueID, BPAProject
from libs.ingest_utils import get_date

from .models import (
    MetabolomicTrack,
    ProteomicTrack,
    SingleCellRNASeqTrack,
    SmallRNATrack,
    SampleTrack,
    TranscriptomeTrack)


def get_bpa_id(bpaid):
    """get BPA ID"""

    if bpaid is None:
        return None

    bpaid = bpaid.replace("/", ".")
    project, _ = BPAProject.objects.get_or_create(key="STEMCELL")
    bpa_id, _ = BPAUniqueID.objects.get_or_create(bpa_id=bpaid, project=project)
    return bpa_id


class DateField(fields.Field):
    """
    This field automatically parses a number of known date formats and returns
    the standard python date
    """

    def __init__(self, *args, **kwargs):
        super(DateField, self).__init__(*args, **kwargs)

    def clean(self, data):
        try:
            val = data[self.column_name]
            return get_date(val)
        except ValueError:
            return None


class BPAIDField(fields.Field):
    def __init__(self, *args, **kwargs):
        super(BPAIDField, self).__init__(*args, **kwargs)

    def clean(self, data):
        return get_bpa_id(data[self.column_name])


BPA_ID = '102.100.100'
track_data = (
    'bpa_id',
    'data_type',
    'description',
    'omics',
    'analytical_platform',
    'facility',
    'work_order',
    'contextual_data_submission_date',
    'sample_submission_date',
    'dataset_url')


class TrackBooleanField(fields.Field):

    def __init__(self, *args, **kwargs):
        super(TrackBooleanField, self).__init__(*args, **kwargs)

    def clean(self, data):
        val = data[self.column_name]
        if val.strip().lower() == 'x':
            return True
        return False


class BPAField(fields.Field):
    def clean(self, data):
        bpaid = data[self.column_name]
        bpaid = '{}.{}'.format(BPA_ID, bpaid)
        # project, _ = BPAProject.objects.get_or_create(name='SEPSIS')
        # bpa_id, _ = BPAUniqueID.objects.get_or_create(bpa_id=bpaid, project=project)
        bpa_id, _ = BPAUniqueID.objects.get_or_create(bpa_id=bpaid)
        return bpa_id


class DataTypeField(fields.Field):
    def clean(self, data):
        name = data[self.column_name]
        matches = [choice_val for (choice_val, choice_name) in SampleTrack._DATA_TYPES if choice_name == name]
        if len(matches) != 1:
            raise Exception("Invalid data type: valid values are: %s" % [t[1] for t in SampleTrack._DATA_TYPES])
        return matches[0]

    def export(self, obj):
        return getattr(obj, "get_%s_display" % (self.attribute))()


class CommonSampleTrackResource(resources.ModelResource):
    """Sample tracking mappings"""

    # bpa_id = fields.Field(attribute='bpa_id', column_name='5 digit BPA ID')
    bpa_id = BPAField(attribute='bpa_id', column_name='5 digit BPA ID')
    data_type = DataTypeField(attribute='data_type', column_name='Data type')
    description = fields.Field(attribute='description', column_name='Description')
    omics = fields.Field(attribute='omics', column_name='Omics')

    analytical_platform = fields.Field(attribute='analytical_platform', column_name='Analytical platform')
    facility = fields.Field(attribute='facility', column_name='Facility')
    work_order = fields.Field(attribute='work_order', column_name='Work order #')
    contextual_data_submission_date = DateField(attribute='contextual_data_submission_date', widget=widgets.DateWidget(format="%Y-%m-%d"), column_name='Contextual Data Submission Date')
    sample_submission_date = DateField(attribute='sample_submission_date', widget=widgets.DateWidget(format="%Y-%m-%d"), column_name='Sample submission date')
    data_generated = TrackBooleanField(attribute='data_generated', widget=widgets.BooleanWidget(), column_name='Data Generated', default=False)
    in_data_archive = TrackBooleanField(attribute='in_data_archive', widget=widgets.BooleanWidget(), column_name='In Data Archive', default=False)

    class Meta:
        import_id_fields = ('bpa_id', )
        export_order = track_data


class CommonTrackAdmin(BPAImportExportModelAdmin):
    date_hierarchy = 'sample_submission_date'
    list_display = track_data
    list_filter = ('bpa_id', 'omics')


class MetabolomicTrackResource(CommonSampleTrackResource):

    class Meta(CommonSampleTrackResource.Meta):
        model = MetabolomicTrack


class MetabolomicTrackAdmin(CommonTrackAdmin):
    resource_class = MetabolomicTrackResource


class ProteomicTrackResource(CommonSampleTrackResource):

    class Meta(CommonSampleTrackResource.Meta):
            model = ProteomicTrack


class ProteomicTrackAdmin(CommonTrackAdmin):
        resource_class = ProteomicTrackResource


class SingleCellRNASeqTrackResource(CommonSampleTrackResource):

    class Meta(CommonSampleTrackResource.Meta):
            model = SingleCellRNASeqTrack


class SingleCellRNASeqTrackAdmin(CommonTrackAdmin):
        resource_class = SingleCellRNASeqTrackResource


class SmallRNATrackResource(CommonSampleTrackResource):

    class Meta(CommonSampleTrackResource.Meta):
            model = SmallRNATrack


class SmallRNATrackAdmin(CommonTrackAdmin):
        resource_class = SmallRNATrackResource


class TranscriptomeTrackResource(CommonSampleTrackResource):

    class Meta(CommonSampleTrackResource.Meta):
            model = TranscriptomeTrack


class TranscriptomeTrackAdmin(CommonTrackAdmin):
        resource_class = TranscriptomeTrackResource


admin.site.register(MetabolomicTrack, MetabolomicTrackAdmin)
admin.site.register(ProteomicTrack, ProteomicTrackAdmin)
admin.site.register(SingleCellRNASeqTrack, SingleCellRNASeqTrackAdmin)
admin.site.register(SmallRNATrack, SmallRNATrackAdmin)
admin.site.register(TranscriptomeTrack, TranscriptomeTrackAdmin)

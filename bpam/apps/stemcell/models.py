
from django.db import models
from apps.common.models import BPAUniqueID


class SampleTrack(models.Model):

    _DATA_TYPES = (
        (1, 'Pre-pilot'),
        (2, 'Pilot'),
        (3, 'Main dataset')
    )
    bpa_id = models.ForeignKey(BPAUniqueID,
                               null=True,
                               verbose_name='BPA ID',
                               help_text='Bioplatforms Australia Sample ID')
    data_type = models.IntegerField('Data Type', choices=_DATA_TYPES, blank=True, null=True)
    description = models.CharField('Description', max_length=1024, blank=True, null=True)
    omics = models.CharField('Omics Type', max_length=50, blank=True, null=True)
    analytical_platform = models.CharField('Analytical Platform', max_length=100, blank=True, null=True)
    facility = models.CharField('Facility', max_length=100, blank=True, null=True)
    work_order = models.CharField('Work Order', max_length=50, blank=True, null=True)
    contextual_data_submission_date = models.DateField('Contextual Data Submission Date', blank=True, null=True, help_text='YYYY-MM-DD')
    sample_submission_date = models.DateField('Sample Submission Date', blank=True, null=True, help_text='YYYY-MM-DD')
    data_generated = models.NullBooleanField('Data Generated', default=False)
    archive_ingestion_date = models.DateField('Archive Ingestion Date', blank=True, null=True, help_text='YYYY-MM-DD')
    dataset_url = models.URLField('Download URL', blank=True, null=True)
    in_data_portal = models.BooleanField('Data ingested into data portal')
    last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'{} {} {}'.format(self.bpa_id, self.taxon_or_organism, self.omics)

    class Meta:
        abstract = True


class MetabolomicTrack(SampleTrack):
    track_type = 'Metabolomic'

    class Meta:
        verbose_name = 'Track Metabolomic'
        verbose_name_plural = verbose_name


class ProteomicTrack(SampleTrack):
    track_type = 'Proteomic'

    class Meta:
        verbose_name = 'Track Proteomic'
        verbose_name_plural = verbose_name


class SingleCellRNASeqTrack(SampleTrack):
    track_type = 'Single Cell RNA'

    class Meta:
        verbose_name = 'Track SingleCellRNA'
        verbose_name_plural = verbose_name


class SmallRNATrack(SampleTrack):
    track_type = 'Small RNA'

    class Meta:
        verbose_name = 'Track SmallRNA'
        verbose_name_plural = verbose_name


class TranscriptomeTrack(SampleTrack):
    track_type = 'Transcriptome'

    class Meta:
        verbose_name = 'Track Transcriptome'
        verbose_name_plural = verbose_name

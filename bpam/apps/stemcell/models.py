from django.db import models

from apps.common.models import SampleTrack


class StemcellSampleTrack(SampleTrack):
    data_set = models.CharField('Data Set', max_length=100, blank=True, null=True)
    cell_type = models.CharField('Cell Type', max_length=100, blank=True, null=True)
    state = models.CharField('Stem Cell State', max_length=100, blank=True, null=True)

    class Meta:
        abstract = True


class MetabolomicTrack(StemcellSampleTrack):
    track_type = 'Metabolomic'

    class Meta:
        verbose_name = 'Track Metabolomic'
        verbose_name_plural = verbose_name


class ProteomicTrack(StemcellSampleTrack):
    track_type = 'Proteomic'

    class Meta:
        verbose_name = 'Track Proteomic'
        verbose_name_plural = verbose_name


class SingleCellRNASeqTrack(StemcellSampleTrack):
    track_type = 'Single Cell RNA'

    class Meta:
        verbose_name = 'Track SingleCellRNA'
        verbose_name_plural = verbose_name


class SmallRNATrack(StemcellSampleTrack):
    track_type = 'Small RNA'

    class Meta:
        verbose_name = 'Track SmallRNA'
        verbose_name_plural = verbose_name


class TranscriptomeTrack(StemcellSampleTrack):
    track_type = 'Transcriptome'

    class Meta:
        verbose_name = 'Track Transcriptome'
        verbose_name_plural = verbose_name


CKAN_RESOURCE_TYPE_TO_MODEL = {
    'stemcells-metabolomic': MetabolomicTrack,
    'stemcells-proteomic': ProteomicTrack,
    'stemcells-transcriptomics': TranscriptomeTrack,
    'stemcells-smallrna': SmallRNATrack,
    'stemcells-singlecellrnaseq': SingleCellRNASeqTrack,
}

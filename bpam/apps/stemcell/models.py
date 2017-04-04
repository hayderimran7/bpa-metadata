
from django.db import models
from apps.common.models import BPAUniqueID, SampleTrack


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


CKAN_RESOURCE_TYPE_TO_MODEL = {
    'stemcells-metabolomic': MetabolomicTrack,
    'stemcells-proteomic': ProteomicTrack,
    'stemcells-transcriptomics': TranscriptomeTrack,
    'stemcells-smallrna': SmallRNATrack,
    'stemcells-singlecellrnaseq': SingleCellRNASeqTrack,
}

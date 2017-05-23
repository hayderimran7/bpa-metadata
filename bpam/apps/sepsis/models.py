# -*- coding: utf-8 -*-

from django.db import models
from apps.common.models import BPAUniqueID


class NotInDataPortalManager(models.Manager):
    def get_queryset(self):
        return super(NotInDataPortalManager, self).get_queryset().filter(in_data_portal=False)


class SampleProcessingManager(NotInDataPortalManager):
    def get_queryset(self):
        return super(SampleProcessingManager, self).get_queryset().filter(data_generated=False)


class BPAArchiveIngestManager(NotInDataPortalManager):
    def get_queryset(self):
        return super(BPAArchiveIngestManager, self).get_queryset().filter(data_generated=True)


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

    # bpa_id = models.CharField('BPA ID', max_length=6)
    taxon_or_organism = models.CharField('Taxon or Organism', max_length=200, blank=True, null=True)
    data_type = models.IntegerField('Data Type', choices=_DATA_TYPES, blank=True, null=True)
    strain_or_isolate = models.CharField('Strain Or Isolate', max_length=200, blank=True, null=True)
    serovar = models.CharField('Serovar', max_length=500, blank=True, null=True)
    growth_media = models.CharField('Growth Media', max_length=500, blank=True, null=True)
    replicate = models.IntegerField('Replicate', blank=True, null=True)
    omics = models.CharField('Omics Type', max_length=50, blank=True, null=True)
    analytical_platform = models.CharField('Analytical Platform', max_length=100, blank=True, null=True)
    facility = models.CharField('Facility', max_length=100, blank=True, null=True)
    work_order = models.CharField('Work Order', max_length=50, blank=True, null=True)
    contextual_data_submission_date = models.DateField('Contextual Data Submission Date', blank=True, null=True, help_text='YYYY-MM-DD')
    sample_submission_date = models.DateField('Sample Submission Date', blank=True, null=True, help_text='YYYY-MM-DD')
    data_generated = models.NullBooleanField('Data Generated', default=False)
    archive_ingestion_date = models.DateField('Archive Ingestion Date', blank=True, null=True, help_text='YYYY-MM-DD')
    curation_url = models.URLField('Curation URL', blank=True, null=True)
    dataset_url = models.URLField('Download URL', blank=True, null=True)
    in_data_portal = models.BooleanField('Data ingested into data portal')

    last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'{} {} {}'.format(self.bpa_id, self.taxon_or_organism, self.omics)

    class Meta:
        abstract = True

    objects = models.Manager()
    uningested = NotInDataPortalManager()
    sample_processing = SampleProcessingManager()
    bpa_archive_ingest = BPAArchiveIngestManager()


class GenomicsSampleTrack(SampleTrack):
    growth_condition_notes = models.CharField('Growth condition notes', max_length=500, blank=True, null=True)

    class Meta:
        abstract = True


class GenomicsPacBioTrack(GenomicsSampleTrack):
    track_type = 'Genomics PacBio'

    class Meta:
        verbose_name = 'Track Genomics PacBio'
        verbose_name_plural = verbose_name


class GenomicsMiSeqTrack(GenomicsSampleTrack):
    track_type = 'Genomics MiSeq'

    class Meta:
        verbose_name = 'Track Genomics MiSeq'
        verbose_name_plural = verbose_name


class TranscriptomicsHiSeqTrack(SampleTrack):
    track_type = 'Transcriptomics HiSeq'

    class Meta:
        verbose_name = 'Track Transcriptomics HiSeq'
        verbose_name_plural = verbose_name


class MetabolomicsLCMSTrack(SampleTrack):
    track_type = 'Metabolomics LCMS'

    class Meta:
        verbose_name = 'Track Metabolomics LCMS'
        verbose_name_plural = verbose_name


class ProteomicsMS1QuantificationTrack(SampleTrack):
    track_type = 'Proteomics MS1-Quantification'

    class Meta:
        verbose_name = 'Track Proteomics MS1-Quantification'
        verbose_name_plural = verbose_name


class ProteomicsSwathMSTrack(SampleTrack):
    track_type = 'Proteomics Swath-MS'

    class Meta:
        verbose_name = 'Track Proteomics Swath-MS'
        verbose_name_plural = verbose_name

CKAN_RESOURCE_TYPE_TO_MODEL = {
    'arp-genomics-miseq': GenomicsMiSeqTrack,
    'arp-genomics-pacbio': GenomicsPacBioTrack,
    'arp-metabolomics-lcms': MetabolomicsLCMSTrack,
    'arp-proteomics-ms1quantification': ProteomicsMS1QuantificationTrack,
    'arp-proteomics-swathms': ProteomicsSwathMSTrack,
    'arp-transcriptomics-hiseq': TranscriptomicsHiSeqTrack,
}

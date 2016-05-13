# -*- coding: utf-8 -*-

from django.db import models

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from apps.common.models import SequenceFile, BPAUniqueID

class Host(models.Model):
    """ Host from who sepsis sample was collected"""

    description = models.CharField('Host Description', max_length=200, blank=True, null=True)
    location = models.CharField('Host Location', max_length=200, blank=True, null=True, help_text="State, Country")
    sex = models.CharField('Host Sex', max_length=1, blank=True, null=True, choices=(('M','Male'), ('F', 'Female')))
    age = models.IntegerField('Host Age', blank=True, null=True)
    dob = models.DateField('Host Day of Birth', blank=True, null=True, help_text="DD/MM/YY")
    disease_outcome = models.TextField('Host Disease Outcome', blank=True, null=True)

    class Meta:
        verbose_name = _('Host')

    def __unicode__(self):
        return "{} {} {} {}".format(self.description, self.location, self.sex, self.age)


class Method(models.Model):
    """Sample preparation method metadata"""

    note = models.TextField('Note', max_length=200, blank=True, null=True)
    growth_condition_temperature = models.IntegerField('Growth condition temperature', blank=True, null=True, help_text="Degrees Centigrade")
    growth_condition_time = models.IntegerField('Growth condition time', blank=True, null=True, help_text="Hours")
    growth_condition_media = models.CharField('Growth condition media', max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = 'Growth Method'
        abstract = True

    def __unicode__(self):
        return u'{} {} {}'.format(self.growth_condition_media, self.growth_condition_temperature, self.growth_condition_time)


class GenomicsMethod(Method):
    """Genomics Metadata"""

    library_construction_protocol = models.CharField('Library Construction Protocol', max_length=100, blank=True, null=True)
    insert_size_range = models.CharField('Insert Size Range', max_length=20, blank=True, null=True)
    sequencer = models.CharField('Sequencer', max_length=100, blank=True, null=True)
    sequencer_run_id = models.CharField('Sequencer run ID', max_length=20, blank=True, null=True)
    smrt_cell_id = models.CharField('SMRT Cell ID', max_length=60, blank=True, null=True)
    cell_position = models.CharField('Cell Position', max_length=60, blank=True, null=True)
    rs_version = models.CharField('RS Version', max_length=20, blank=True, null=True)

    class Meta:
        verbose_name = 'Genomics Method'

    def __unicode__(self):
        return u'{} {} {}'.format(self.library_construction_protocol, self.insert_size_range, self.sequencer)


class ProteomicsMethod(Method):
    """Proteomics Metadata"""

    sample_fractionation = models.IntegerField('Sample Fractionation', blank=True, null=True)
    lc_column_type = models.CharField('LC/column type', max_length=100, blank=True, null=True)
    gradient = models.CharField('Gradient time (min)  /  % ACN (start-finish main gradient) / flow', max_length=100, blank=True, null=True)
    column = models.CharField('Sample on column(µg) ', max_length=100, blank=True, null=True)
    mass_spectrometer = models.CharField('Mass Spectrometer', max_length=100, blank=True, null=True)
    aquisition_mode = models.CharField('Acquisition Mode / fragmentation', max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = 'Proteomics Method'

    def __unicode__(self):
        return u'{} {} {}'.format(self.library_construction_protocol, self.insert_size_range, self.sequencer)
# TODO
class TranscriptomicsMethod(Method):
    """Transcriptomics Metadata"""
    pass


# Little point in expanding the common Sample Type
class SepsisSample(models.Model):
    """ Sepsis Sample """

    bpa_id = models.OneToOneField(BPAUniqueID, primary_key=True, verbose_name='BPA ID')
    taxon_or_organism = models.TextField('Taxon or Organism', max_length=200, blank=True, null=True)
    strain_or_isolate = models.TextField('Strain Or Isolate', max_length=200, blank=True, null=True)
    strain_description = models.TextField('Strain Description', max_length=300, blank=True, null=True)
    gram_stain = models.CharField('Gram Staining', max_length=3, choices=(('POS', 'Positive'), ('NEG', 'Negative')))
    serovar = models.CharField('Serovar', max_length=30, blank=True, null=True)
    key_virulence_genes = models.CharField('Key Virulence Genes', max_length=100, blank=True, null=True)
    isolation_source = models.CharField('Isolation Source', max_length=100, blank=True, null=True)
    publication_reference = models.CharField('Publication Reference', max_length=200, blank=True, null=True)
    contact_researcher = models.CharField('Contact Researcher', max_length=200, blank=True, null=True)
    collection_date = models.DateField('Collection Date', blank=True, null=True, help_text="DD/MM/YY")
    culture_collection_id = models.CharField('Culture Collection ID', max_length=100, blank=True, null=True)

    host = models.ForeignKey(Host, blank=True, null=True, related_name="%(app_label)s_%(class)s_sample")

    def __unicode__(self):
        return u'{0}:{1}, {2}'.format(self.bpa_id, self.taxon_or_organism, self.strain_or_isolate)

    class Meta:
        verbose_name = _('Sepsis Sample')

class SepsisSequenceFile(SequenceFile):
    """ Sequence Files """

    project_name = 'sepsis'
    sample = models.ForeignKey(SepsisSample)

    def __unicode__(self):
        return u'{}'.format(self.filename)

    class Meta:
        abstract = True

class ProteomicsFile(SepsisSequenceFile):
    """Sequence file from the proteomics analysis process"""

    method = models.ForeignKey(ProteomicsMethod, related_name="%(app_label)s_%(class)s_proteomicsfile")

    def __unicode__(self):
        return u'{}'.format(self.filename)

class GenomicsFile(SepsisSequenceFile):
    """Sequence file from the genomics analysis process"""

    method = models.ForeignKey(GenomicsMethod, related_name="%(app_label)s_%(class)s_genomicsfile")

    def __unicode__(self):
        return u'{}'.format(self.filename)

class TranscriptomicsFile(SepsisSequenceFile):
    """Sequence file from the transcriptomics analysis process"""

    method = models.ForeignKey(TranscriptomicsMethod, related_name="%(app_label)s_%(class)s_transcriptomicsfile")

    def __unicode__(self):
        return u'{}'.format(self.filename)

from django.utils.translation import ugettext_lazy as _
from django.db import models

from apps.common.models import SequenceFile, Run, DebugNote
from apps.base.models import BASESample


class MetagenomicsSample(BASESample, DebugNote):
    """
    BASE Meta genomics Soil Sample
    """

    def __unicode__(self):
        return u"{0}".format(self.name)

    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in MetagenomicsSample._meta.fields]

    class Meta:
        verbose_name_plural = _("Metagenomics Sample")


class MetagenomicsRun(Run):
    """
    A Meta genomics sequence file generation Run
    """
    sample = models.ForeignKey(MetagenomicsSample)

    def __unicode__(self):
        return u'Run {0} for {1}'.format(self.run_number, self.sample.name)

    class Meta:
        verbose_name_plural = _("Metagenomics Run")


class MetagenomicsSequenceFile(SequenceFile):
    """
    Meta genomics Sequence File
    """

    sample = models.ForeignKey(MetagenomicsSample)
    run = models.ForeignKey(MetagenomicsRun, null=True)  # FIXME

    class Meta:
        verbose_name_plural = _("Metagenomics Sequence Files")


class PCRPrimer(models.Model):
    """
    PCR Primers
    """

    name = models.CharField(max_length=100, unique=True)
    note = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return u"{0}".format(self.name)

    class Meta:
        verbose_name_plural = _("PCR Primers")


class TargetGene(models.Model):
    """
    Target Gene
    """

    name = models.CharField(max_length=100, unique=True)
    note = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return u"{0}".format(self.name)

    class Meta:
        verbose_name_plural = _("Target Genes")


class TargetTaxon(models.Model):
    """
    Target Taxon
    """

    name = models.CharField(max_length=100, unique=True)
    note = models.TextField()

    def __unicode__(self):
        return u"{0}".format(self.name)

    class Meta:
        verbose_name_plural = _("Target Taxons")


class SequenceConstruct(models.Model):
    """
    The Sequence Construct
    """

    adapter_sequence = models.CharField(max_length=100, blank=True)
    barcode_sequence = models.CharField(max_length=100, blank=True)
    forward_primer = models.CharField(max_length=100, blank=True)
    primer_sequence = models.CharField(max_length=100, blank=True)
    target_region = models.CharField(max_length=100, blank=True)
    sequence = models.CharField(max_length=100, blank=True)
    reverse_primer = models.CharField(max_length=100, blank=True)

    note = models.TextField(blank=True)

    def __unicode__(self):
        return u"{0}".format(self.sequence)

    class Meta:
        verbose_name_plural = _("Sequence Constructs")


class SoilSampleDNA(models.Model):
    name = models.CharField(max_length=20)
    submitter = models.CharField(max_length=20)
    dna_conc = models.CharField(max_length=20, blank=True, null=True)
    protocol_ref = models.CharField(max_length=20, blank=True, null=True, choices=(('S', 'Single'), ('P', 'Paired')))
    library_selection = models.CharField(max_length=20, blank=True, null=True)
    library_layout = models.CharField(max_length=20, blank=True, null=True)
    target_taxon = models.ForeignKey(TargetTaxon)
    target_gene = models.ForeignKey(TargetGene, related_name='target')
    target_subfragment = models.ForeignKey(TargetGene, related_name='subfragment')
    pcr_primer = models.ForeignKey(PCRPrimer)
    pcr_primer_db_ref = models.CharField(max_length=20, blank=True, null=True)
    forward_primer_sequence = models.CharField(max_length=100, blank=True, null=True)
    reverse_primer_sequence = models.CharField(max_length=100, blank=True, null=True)
    pcr_reaction = models.CharField(max_length=100, blank=True, null=True)
    barcode_label = models.CharField(max_length=10, blank=True, null=True)
    barcode_sequence = models.CharField(max_length=20, blank=True, null=True)
    performer = models.CharField(max_length=10, blank=True, null=True)
    labeled_extract_name = models.CharField(max_length=10, blank=True, null=True)

    def __unicode__(self):
        return u"Soil DNA Library {0}".format(self.name)

    class Meta:
        verbose_name_plural = _("Soil Sample DNA")

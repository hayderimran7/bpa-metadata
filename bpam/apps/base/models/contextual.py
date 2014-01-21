from django.db import models
from django.utils.translation import ugettext_lazy as _
from apps.common.models import BPAUniqueID


class PCRPrimer(models.Model):
    """
    PCR Primers
    """

    name = models.CharField(max_length=100, unique=True)
    note = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return u"{0}".format(self.name)

    class Meta:
        app_label = 'base'
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
        app_label = 'base'
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
        app_label = 'base'
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
        app_label = 'base'
        verbose_name_plural = _("Sequence Constructs")


class ChemicalAnalysis(models.Model):
    """
    Chemical Analysis assay
    """

    # sample = models.ForeignKey(SoilSample)
    bpa_id = models.ForeignKey(BPAUniqueID)
    lab_name_id = models.CharField(_('Lab Name ID'), max_length=100, blank=True, null=True)
    customer = models.CharField(max_length=100, blank=True, null=True)
    depth = models.CharField(max_length=100, blank=True, null=True)
    colour = models.CharField(max_length=100, blank=True, null=True)
    gravel = models.CharField(max_length=100, blank=True, null=True)
    texture = models.CharField(max_length=100, blank=True, null=True)

    ammonium_nitrogen = models.FloatField(blank=True, null=True)
    nitrate_nitrogen = models.CharField(max_length=10, null=True)  # <>
    phosphorus_colwell = models.CharField(max_length=10, null=True)  # <>
    potassium_colwell = models.FloatField(blank=True, null=True)
    sulphur_colwell = models.FloatField(blank=True, null=True)
    organic_carbon = models.FloatField(blank=True, null=True)
    conductivity = models.FloatField(blank=True, null=True)
    cacl2_ph = models.FloatField(_('CaCl2 pH'), blank=True, null=True)
    h20_ph = models.FloatField(_('H20 pH'), blank=True, null=True)
    dtpa_copper = models.FloatField(_('DTPA Cu'), blank=True, null=True)
    dtpa_iron = models.FloatField(_('DTPA Fe'), blank=True, null=True)
    dtpa_manganese = models.FloatField(_('DTPA Mn'), blank=True, null=True)
    dtpa_zinc = models.FloatField(_('DTPA Zn'), blank=True, null=True)
    exc_aluminium = models.FloatField(_('Exc Al'), blank=True, null=True)
    exc_calcium = models.FloatField(_('Exc Ca'), blank=True, null=True)
    exc_magnesium = models.FloatField(_('Exc Mg'), blank=True, null=True)
    exc_potassium = models.FloatField(_('Exc K'), blank=True, null=True)
    exc_sodium = models.FloatField(_('Exc Na'), blank=True, null=True)
    boron_hot_cacl2 = models.FloatField(_('B Hot CaCl2'), blank=True, null=True)

    clay = models.FloatField(blank=True, null=True)
    course_sand = models.FloatField(blank=True, null=True)
    fine_sand = models.FloatField(blank=True, null=True)
    sand = models.FloatField(blank=True, null=True)
    silt = models.FloatField(blank=True, null=True)

    def __unicode__(self):
        return u"Chemical Analysis for {0}".format(self.bpa_id)

    class Meta:
        app_label = 'base'
        verbose_name_plural = _("Sample Chemical Essays")


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
        app_label = 'base'
        verbose_name_plural = _("Soil Sample DNA")

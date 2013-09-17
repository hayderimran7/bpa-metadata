from django.db import models
from apps.common.models import Sample, BPAUniqueID
from apps.geo.models import GPSPosition

from django.utils.translation import ugettext_lazy as _


class PCRPrimer(models.Model):
    """
    PCR Primers
    """

    name = models.CharField(max_length=100, unique=True)
    note = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return "{0}".format(self.name)

    class Meta:
        verbose_name_plural = _("PCR Primers")


class LandUse(models.Model):
    """
    Land use taxonomy
    http://lrm.nt.gov.au/soil/landuse/classification
    """

    classification = models.IntegerField(unique=True)
    description = models.CharField(max_length=300)
    note = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return "{0}".format(self.description)

    class Meta:
        verbose_name_plural = _("Land Uses")
        unique_together = ('classification', 'description')


class GeneralEcologicalZone(models.Model):
    """
    General ecological zone taxonomy
    """

    description = models.CharField(max_length=100, unique=True)
    note = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return "{0}".format(self.description)

    class Meta:
        verbose_name_plural = _("General Ecological Zones")


class BroadVegetationType(models.Model):
    """
    Broad Vegetation Type taxonomy
    """

    description = models.CharField(max_length=100, unique=True)
    note = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return "{0}".format(self.description)

    class Meta:
        verbose_name_plural = _("Broad Vegetation Types")


class TillageType(models.Model):
    """
    Note method(s) used for tilling; moldboard plow, chisel, no-till, etc.
    """

    tillage = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __unicode__(self):
        return "{0}".format(self.tillage)

    class Meta:
        verbose_name_plural = _("Tillage Types")


class HorizonType(models.Model):
    """
    Specific layer in the land area which measures parallel to the soil surface and possesses physical characteristics
    which differ from the layers above and beneath; master horizons (O, A, E,  B, C, R) are rather standard, but
    sub-designations (subordinate distinctions) will vary by country.
    """

    horizon = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __unicode__(self):
        return "{0}".format(self.horizon)

    class Meta:
        verbose_name_plural = _("Horizon Types")


class SoilClassification(models.Model):
    """
    Australian Soil Classification System (http://www.clw.csiro.au/aclep/asc_re_on_line/soilkey.htm)
    Soil classification from the FAO World Reference
    (http://www.fao.org/docrep/w8594e/w8594e05.htm#key%20to%20the%20reference%20soil%20groups%20of%20the%20world%20reference%20base%20for%20soil%20resources)
    """

    authority = models.CharField(max_length=10)
    classification = models.CharField(max_length=50)
    note = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return "{0} {1}".format(self.authority, self.classification)

    class Meta:
        verbose_name_plural = _("Soil Classification")


class TargetGene(models.Model):
    """
    Target Gene
    """

    name = models.CharField(max_length=100, unique=True)
    note = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return "{0}".format(self.name)

    class Meta:
        verbose_name_plural = _("Target Genes")


class TargetTaxon(models.Model):
    """
    Target Taxon
    """

    name = models.CharField(max_length=100, unique=True)
    note = models.TextField()

    def __unicode__(self):
        return "{0}".format(self.name)

    class Meta:
        verbose_name_plural = _("Target Taxons")


class SiteOwner(models.Model):
    """
    The Site Owner
    """

    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField()
    address = models.TextField(blank=True)
    note = models.TextField(blank=True)

    def __unicode__(self):
        return "{0} {1}".format(self.name, self.email)

    class Meta:
        verbose_name_plural = _("Site Owners")


class CollectionSiteHistory(models.Model):
    """
    Background history for the collection site
    """

    history_report_date = models.DateField(blank=True, null=True)  # the date this report was compiled
    current_vegetation = models.CharField(max_length=100, blank=True)

    previous_land_use = models.ForeignKey(LandUse, related_name='previous')
    current_land_use = models.ForeignKey(LandUse, related_name='current')
    crop_rotation = models.CharField(max_length=100, blank=True)
    tillage = models.CharField(max_length=100, blank=True)
    environment_event = models.CharField(max_length=100, blank=True)  # fire, flood, extreme, other

    note = models.TextField()

    def __unicode__(self):
        return "Site history on {0}".format(self.history_report_date)

    class Meta:
        verbose_name_plural = _("Site History")


class CollectionSite(models.Model):
    """
    Collection Site Information
    """

    country = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    location_name = models.CharField(max_length=100, blank=True)
    image_url = models.URLField(blank=True, null=True)

    positions = models.ManyToManyField(GPSPosition, null=True, blank=True)

    horizon = models.CharField(max_length=100, blank=True)
    plot_description = models.TextField(blank=True)
    collection_depth = models.CharField(max_length=20, blank=True)

    slope_gradient = models.CharField(max_length=20, blank=True)
    slope_aspect = models.CharField(max_length=20, blank=True)
    profile_position = models.CharField(max_length=20, blank=True)
    drainage_classification = models.CharField(max_length=20, blank=True)
    australian_classification_soil_type = models.CharField(max_length=20, blank=True)

    history = models.ForeignKey(CollectionSiteHistory, null=True)
    owner = models.ForeignKey(SiteOwner, null=True)

    note = models.TextField(blank=True)

    def __unicode__(self):
        return "{0}, {1}, {2} {3}".format(self.country, self.state, self.location_name, self.plot_description)

    class Meta:
        verbose_name_plural = "Collection Sites"


class SoilSample(Sample):
    """
    BASE Soil Sample
    """

    collection_site = models.ForeignKey(CollectionSite)


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
        return "{0}".format(self.sequence)

    class Meta:
        verbose_name_plural = _("Sequence Constructs")


class ChemicalAnalysis(models.Model):
    """
    Chemical Analysis assay
    """

    # sample = models.ForeignKey(SoilSample)
    bpa_id = models.ForeignKey(BPAUniqueID)
    lab_name_id = models.CharField(max_length=100, blank=True, null=True)
    customer = models.CharField(max_length=100, blank=True, null=True)
    depth = models.CharField(max_length=100, blank=True, null=True)
    colour = models.CharField(max_length=100, blank=True, null=True)
    gravel = models.CharField(max_length=100, blank=True, null=True)
    texture = models.CharField(max_length=100, blank=True, null=True)

    ammonium_nitrogen = models.FloatField(blank=True, null=True)
    nitrate_nitrogen = models.CharField(max_length=10, null=True) # <>
    phosphorus_colwell = models.CharField(max_length=10, null=True) # <>
    potassium_colwell = models.FloatField(blank=True, null=True)
    sulphur_colwell = models.FloatField(blank=True, null=True)
    organic_carbon = models.FloatField(blank=True, null=True)
    conductivity = models.FloatField(blank=True, null=True)
    cacl2_ph = models.FloatField(blank=True, null=True)
    h20_ph = models.FloatField(blank=True, null=True)
    dtpa_copper = models.FloatField(blank=True, null=True)
    dtpa_iron = models.FloatField(blank=True, null=True)
    dtpa_manganese = models.FloatField(blank=True, null=True)
    dtpa_zinc = models.FloatField(blank=True, null=True)
    exc_aluminium = models.FloatField(blank=True, null=True)
    exc_calcium = models.FloatField(blank=True, null=True)
    exc_magnesium = models.FloatField(blank=True, null=True)
    exc_potassium = models.FloatField(blank=True, null=True)
    exc_sodium = models.FloatField(blank=True, null=True)
    boron_hot_cacl2 = models.FloatField(blank=True, null=True)

    clay = models.FloatField(blank=True, null=True)
    course_sand = models.FloatField(blank=True, null=True)
    fine_sand = models.FloatField(blank=True, null=True)
    sand = models.FloatField(blank=True, null=True)
    silt = models.FloatField(blank=True, null=True)

    def __unicode__(self):
        return "Chemical Analysis for {0}".format(self.bpa_id)

    class Meta:
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
    protocol_ref = models.CharField(max_length=10, blank=True, null=True)

    def __unicode__(self):
        return "Soil DNA Library {0}".format(self.name)

    class Meta:
        verbose_name_plural = _("Soil Sample DNA")

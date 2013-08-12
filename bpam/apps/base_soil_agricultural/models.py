from django.db import models
from apps.common.models import Sample, BPAUniqueID
from django.utils.translation import ugettext_lazy as _

class PCRPrimer(models.Model):
    """ PCR Primers """
        
    PRIMERS = ('27F-519R',
               'ITS1F-ITS4',
               '515F-806R',
               '1392F-1492R',)
    
    name = models.CharField(max_length=100, unique=True)
    note = models.TextField(null=True, blank=True)
    
    @classmethod
    def makeall(cls):
        """Create all Primers"""
        for name in cls.PRIMERS:
            TargetGene(name=name).save()
    
    def __unicode__(self):
        return "{}".format(self.name)
    
    class Meta:
        verbose_name_plural = _("PCR Primers")

class TargetGene(models.Model):
    """ Target Gene """
    
    GENES = ('V1-V3', 'V4', 'V9', 'ITS1-4')
    
    name = models.CharField(max_length=100, unique=True)
    note = models.TextField(null=True, blank=True)
    
    @classmethod
    def makeall(cls):
        """ Create all Target Genes"""
        for name in cls.GENES:
            TargetGene(name=name).save()
    
    def __unicode__(self):
        return "{}".format(self.name)
    
    class Meta:
        verbose_name_plural = _("Target Genes")


class TargetTaxon(models.Model):
    """ Target Taxon """
    
    TAXI = ('Eukarya',
            'Bacteria',
            'Prokaryota',
            'Fungi', 
            'Bacteria and archea')
    
    name = models.CharField(max_length=100, unique=True)
    note = models.TextField()
    
    @classmethod
    def makeall(cls):
        """ Create all Target Taxons"""
        for name in cls.TAXI:
            TargetTaxon(name=name).save()
    
    def __unicode__(self):
        return "{}".format(self.name)
    
    class Meta:
        verbose_name_plural = _("Target Taxons")


class LandUse(models.Model):
    """ Land use taxonomy 
    http://lrm.nt.gov.au/soil/landuse/classification
    """
        
    LAND_USES = ((1, 'Conservation and Natural Environments'),
                 (2, 'Production from relatively natural Environments'),
                 (3, 'Production from dry land agriculture and plantations'),
                 (4, 'Production from Irrigated agriculture and plantations'),
                 (5, 'Intensive uses'),
                 (6, 'Water'),)
        
    classification = models.IntegerField(unique=True)
    description = models.CharField(max_length=100, blank=True)
    
    @classmethod
    def makeall(cls):
        """ Create all Land Uses"""
        for c, d in cls.LAND_USES:
            LandUse(classification=c, description=d).save()
            
    
    def __unicode__(self):
        return "{}".format(self.description)
    
    class Meta:
        verbose_name_plural = _("Land Uses")
        unique_together = ('classification', 'description')        

class SiteOwner(models.Model):
    """ The Site Owner """
    
    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField()
    address = models.TextField(blank=True)
    note = models.TextField(blank=True)
            
    def __unicode__(self):
        return "{} {}".format(self.name, self.email)
    
    class Meta:
        verbose_name_plural = _("Site Owners")

class CollectionSiteHistory(models.Model):
    """ Background history for the collection site"""

    history_report_date = models.DateField(blank=True, null=True) # the date this report was compiled
    current_vegation = models.CharField(max_length=100, blank=True)
    
    previous_land_use = models.ForeignKey(LandUse, related_name='previous')
    current_land_use = models.ForeignKey(LandUse, related_name='current')
    crop_rotation = models.CharField(max_length=100, blank=True)
    tillage = models.CharField(max_length=100, blank=True)
    environment_event = models.CharField(max_length=100, blank=True) # fire, flood, extreme, other
        
    note = models.TextField()           
    
    def __unicode__(self):
        return "Site history on {}".format(self.history_report_date)
    
    class Meta:
        verbose_name_plural = _("Site History")
    
    
class CollectionSite(models.Model):
    """ Collection Site Information """
    
    country = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    location_name = models.CharField(max_length=100, blank=True)
    image_url = models.URLField(blank=True, null=True)
    horizon = models.CharField(max_length=100, blank=True)

    plot_description = models.TextField(blank=True)
    collection_depth = models.CharField(max_length=20, blank=True)
    lat = models.CharField(max_length=20, blank=True)
    long = models.CharField(max_length=20, blank=True)
    elevation = models.CharField(max_length=20, blank=True)
    slope_gradient = models.CharField(max_length=20, blank=True)
    slope_aspect = models.CharField(max_length=20, blank=True)
    profile_position = models.CharField(max_length=20, blank=True)
    drainage_classification = models.CharField(max_length=20, blank=True)
    australian_classification_soil_type = models.CharField(max_length=20, blank=True)
    
    history = models.ForeignKey(CollectionSiteHistory, null=True)
    owner = models.ForeignKey(SiteOwner, null=True)
    
    note = models.TextField(blank=True)

    def __unicode__(self):
        return "Collection site {} {} {}".format(self.country, self.state, self.location_name)
    
    class Meta:
        verbose_name_plural = "Collection Sites"

class SoilSample(Sample):
    """ Soil Sample """
        
    collection_site = models.ForeignKey(CollectionSite)    
    
    
class SequenceConstruct(models.Model):
    """ The Sequence Construct """
    
    adapter_sequence = models.CharField(max_length=100, blank=True)
    barcode_sequence = models.CharField(max_length=100, blank=True)
    forward_primer = models.CharField(max_length=100, blank=True)
    primer_sequence = models.CharField(max_length=100, blank=True)
    target_region = models.CharField(max_length=100, blank=True)
    sequence = models.CharField(max_length=100, blank=True)
    reverse_primer = models.CharField(max_length=100, blank=True)
    
    note = models.TextField(blank=True)

    def __unicode__(self):
        return "{}".format(self.sequence)
    
    class Meta:
        verbose_name_plural = _("Sequence Constructs")
        
class ChemicalAnalysis(models.Model):
    """ Chemical Analysis assay """
    
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
        return "Chemical Analysis for {}".format(self.bpa_id)
    
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
        return "Soil DNA Library {}".format(self.name)
    
    class Meta:
        verbose_name_plural = _("Soil Sample DNA")
    
    
    
    
    
    
    
    

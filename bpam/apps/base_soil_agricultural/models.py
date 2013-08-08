from django.db import models
from apps.common.models import Sample

class LandUse(models.Model):
    """ Land use taxonomy """
    
    description = models.CharField(max_length=100, blank=True)
    
    def __unicode__(self):
        return "{}".format(self.description)
    
    class Meta:
        verbose_name_plural = "Land Uses"

class SiteOwner(models.Model):
    """ The Site Owner """
    
    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField()
    address = models.TextField(blank=True)
    note = models.TextField(blank=True)
            
    def __unicode__(self):
        return "{} {}".format(self.name, self.email)
    
    class Meta:
        verbose_name_plural = "Site Owners"

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
        verbose_name_plural = "Site History"
    

class CollectionSite(models.Model):
    """ Collection Site Information"""
    
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
        return "Collection site {} {}".format(self.collection_depth, self.plot_description, self.note)
    
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
        verbose_name_plural = "Sequence Constructs"
        
class ChemicalAnalysis(models.Model):
    """ Chemical Analysis assay """
    
    sample = models.ForeignKey(SoilSample)
    lab_name_id = models.CharField(max_length=100, blank=True)
    customer = models.CharField(max_length=100, blank=True)
    collection_depth = models.CharField(max_length=100, blank=True)
    colour = models.CharField(max_length=100, blank=True)
    gravel_persent = models.CharField(max_length=100, blank=True)
    texture = models.CharField(max_length=100, blank=True)
    
    ammonium_nitrogen_mg_kg = models.FloatField()
    nitrate_nitrogen_mg_kg = models.FloatField()
    phosphorus_colwell_mg_kg = models.FloatField()
    potassium_colwell_mg_kg = models.FloatField()
    sulphur_colwell_mg_kg = models.FloatField()
    organic_carbon_persentage = models.FloatField()
    conductivity_ds_m = models.FloatField()
    cacl2_ph = models.FloatField()
    h20_ph = models.FloatField()
    dtpa_copper_mg_kg = models.FloatField()
    dtpa_iron_mg_kg = models.FloatField()
    dtpa_manganese_mg_kg = models.FloatField()
    dtpa_zinc_mg_kg = models.FloatField()
    exc_aluminium_meq_100g = models.FloatField()
    exc_calsium_meq_100g = models.FloatField()
    exc_magnesium_meq_100g = models.FloatField()
    exc_potasium_meq_100g = models.FloatField()
    exc_sodium_meq_100g = models.FloatField()
    boron_hot_cacl2_mg_kg = models.FloatField()
    
    clay_persentage = models.FloatField()
    course_sand_persentage = models.FloatField()
    fine_sand_persentage = models.FloatField()
    sand_persentage = models.FloatField()
    silt_persentage = models.FloatField()
    
    
    def __unicode__(self):
        return "Chemical Analysis for {}".format(self.sample)
    
    class Meta:
        verbose_name_plural = "Sample Chemical Essays"
    
        

    
    
    
    
    
    
    
    
    
    

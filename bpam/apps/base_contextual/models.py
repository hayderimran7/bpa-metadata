# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.gis.geos import Point

from apps.common.models import BPAUniqueID, DebugNote

from apps.base_vocabulary.models import LandUse
from apps.base_vocabulary.models import HorizonClassification
from apps.base_vocabulary.models import GeneralEcologicalZone
from apps.base_vocabulary.models import BroadVegetationType
from apps.base_vocabulary.models import AustralianSoilClassification
from apps.base_vocabulary.models import FAOSoilClassification
from apps.base_vocabulary.models import ProfilePosition
from apps.base_vocabulary.models import DrainageClassification
from apps.base_vocabulary.models import SoilColour
from apps.base_vocabulary.models import TillageType


class CollectionSite(DebugNote):
    """ Collection Site Information """

    country = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    location_name = models.CharField("Location Name", max_length=100, blank=True)
    image_url = models.URLField("Site Photo", blank=True, null=True)
    date_sampled = models.DateField("Date Sampled", null=True)
    lat = models.FloatField("Latitude", help_text="Degree decimal")
    lon = models.FloatField("Longitude", help_text="Degree decimal")
    elevation = models.IntegerField("Elevation", null=True)

    # controlled vocabularies
    current_land_use = models.ForeignKey(LandUse, related_name="current", null=True, verbose_name="Current Land Use")
    broad_land_use = models.ForeignKey(LandUse, related_name="broad", null=True, verbose_name="Broad Land Use")
    general_ecological_zone = models.ForeignKey(GeneralEcologicalZone,
                                                null=True,
                                                verbose_name="General Ecological Zone")
    vegetation_type = models.ForeignKey(BroadVegetationType, null=True, verbose_name="Vegetation Type")
    soil_type_australian_classification = models.ForeignKey(AustralianSoilClassification,
                                                            verbose_name="Australian Soil Type Classification",
                                                            null=True)
    soil_type_fao_classification = models.ForeignKey(FAOSoilClassification,
                                                     verbose_name="FAO Soil Type Classification",
                                                     null=True)

    vegetation_total_cover = models.CharField("Vegetation Total Cover",
                                              max_length=200, blank=True)  # free text in column
    vegetation_dominant_trees = models.CharField("Vegetation Dominant Trees", max_length=1000, blank=True)

    slope = models.CharField(max_length=20, blank=True)
    slope_aspect = models.CharField("Slope Aspect",
                                    max_length=100,
                                    blank=True,
                                    help_text=u"Direction or degrees; e.g., NW or 315°")

    profile_position = models.ForeignKey(ProfilePosition, verbose_name="Profile Position", null=True)
    drainage_classification = models.ForeignKey(DrainageClassification,
                                                verbose_name="Drainage Classification",
                                                null=True)

    # some history for this site
    environment_event = models.CharField(max_length=100, blank=True)  # fire, flood, extreme, other
    # fire
    fire_history = models.CharField("Fire History", max_length=500, blank=True)
    fire_intensity = models.CharField("Fire Intensity", max_length=500, blank=True)
    # land use
    date_since_change_in_land_use = models.CharField(
        "Date Since Land Use Change", max_length=100,
        blank=True, null=True)
    immediate_previous_land_use = models.ForeignKey(LandUse, related_name="previous", blank=True, null=True)

    crop_rotation_1 = models.TextField("Crop rotation 1 year ago", blank=True, null=True)
    crop_rotation_2 = models.TextField("Crop rotation 2 years ago", blank=True, null=True)
    crop_rotation_3 = models.TextField("Crop rotation 3 years ago", blank=True, null=True)
    crop_rotation_4 = models.TextField("Crop rotation 4 years ago", blank=True, null=True)
    crop_rotation_5 = models.TextField("Crop rotation 5 years ago", blank=True, null=True)

    agrochemical_additions = models.CharField("Agrochemical Additions", max_length=300, blank=True, null=True)
    tillage = models.ForeignKey(TillageType, blank=True, null=True)

    other_comments = models.TextField("Comments", blank=True, null=True)

    @property
    def get_location_name(self):
        """
        Get location name or lat, lon if no location name is available
        """
        if self.location_name:
            return u"{} ({:4.4f}, {:4.4f})".format(self.location_name, self.lat, self.lon)
        return u"{:4.4f}, {:4.4f}".format(self.lat, self.lon)

    @property
    def geom(self):
        return Point(self.lon, self.lat, srid=4326)

    def __unicode_self(self):
        return u",".join(str(s) for s in (self.location_name,
                                          self.lat,
                                          self.lon, ) if s)

    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in CollectionSite._meta.fields]

    class Meta:
        verbose_name_plural = "Collection Sites"
        unique_together = ("lat",
                           "lon", )


class ChemicalAnalysis(models.Model):
    """ Chemical Analysis assay """

    bpa_id = models.ForeignKey(BPAUniqueID, verbose_name="BPA ID")
    # structural
    depth = models.CharField(max_length=100, blank=True, null=True)
    moisture = models.FloatField("Soil Moisture", blank=True, null=True)
    colour = models.ForeignKey(SoilColour, verbose_name="Soil Colour", null=True)
    gravel = models.CharField("Gravel", max_length=100, blank=True, null=True, help_text=u">2.0mm")
    texture = models.FloatField(max_length=100, blank=True, null=True)
    course_sand = models.FloatField(blank=True, null=True, help_text=u"200-2000 µm")
    fine_sand = models.FloatField(blank=True, null=True, help_text=u"20-200 µm")
    sand = models.FloatField(blank=True, null=True)
    silt = models.FloatField(blank=True, null=True, help_text=u"2-20 µm")
    clay = models.FloatField(blank=True, null=True, help_text=u"<2 µm")

    # chemical
    ammonium_nitrogen = models.FloatField("Ammonium Nitrogen", blank=True, null=True)
    nitrate_nitrogen = models.FloatField("Nitrate Nitrogen", blank=True, null=True)
    phosphorus_colwell = models.FloatField("Phosphorus Colwell", blank=True, null=True)
    potassium_colwell = models.FloatField("Potassium Colwell", blank=True, null=True)
    sulphur = models.FloatField(blank=True, null=True)
    organic_carbon = models.FloatField(blank=True, null=True)
    conductivity = models.FloatField(blank=True, null=True)
    # pH
    cacl2_ph = models.FloatField("pH Level CaCl2", blank=True, null=True)
    h20_ph = models.FloatField("pH Level H20", blank=True, null=True)
    # DTPA
    dtpa_copper = models.FloatField("DTPA Copper", blank=True, null=True)
    dtpa_iron = models.FloatField("DTPA Iron", blank=True, null=True)
    dtpa_manganese = models.FloatField("DTPA Manganse", blank=True, null=True)
    dtpa_zinc = models.FloatField("DTPA Zinc", blank=True, null=True)
    # exc
    exc_aluminium = models.FloatField("Exc. Aluminium", blank=True, null=True)
    exc_calcium = models.FloatField("Exc. Calsium", blank=True, null=True)
    exc_magnesium = models.FloatField("Exc. Magnesium", blank=True, null=True)
    exc_potassium = models.FloatField("Exc. Potassium", blank=True, null=True)
    exc_sodium = models.FloatField("Exc. Sodium", blank=True, null=True)
    boron_hot_cacl2 = models.FloatField("Boron Hot CaCl2", blank=True, null=True)

    total_nitrogen = models.FloatField("Total Nitrogen", blank=True, null=True)
    total_carbon = models.FloatField("Total Carbon", blank=True, null=True)

    def __unicode_self(self):
        return u"Chemical Analysis for {0}".format(self.bpa_id)

    class Meta:
        # app_label = "base"
        verbose_name_plural = "Sample Chemical Essays"


class SampleContext(DebugNote):
    """ A model to collect sample specific info for contextual data. """

    bpa_id = models.OneToOneField(BPAUniqueID, verbose_name="BPA ID")
    site = models.ForeignKey(CollectionSite, null=True)  # there may be no site set
    analysis = models.ForeignKey(ChemicalAnalysis, null=True)  # there may be no site set

    horizon_classification1 = models.ForeignKey(HorizonClassification,
                                                null=True,
                                                related_name="one",
                                                verbose_name="Horizon Classification One")
    horizon_classification2 = models.ForeignKey(HorizonClassification,
                                                null=True,
                                                related_name="two",
                                                verbose_name="Horizon Classification Two")
    depth = models.CharField("Soil Depth", max_length=20, blank=True)

    storage = models.CharField("Storage", max_length=100, blank=True, null=True, help_text="Storage")
    methodological_notes = models.TextField("Methodological Notes", blank=True, null=True)

    def get_horizon_description(self):
        """ String combining horizon classifications """
        desc = []
        for c in (self.horizon_classification1, self.horizon_classification2):
            if c is not None:
                desc.append(c.horizon)
        return u",".join(desc)

    def __unicode_self(self):
        return u"{0} {1}".format(self.bpa_id, self.horizon_classification1, self.horizon_classification2, self.depth)

    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in SampleContext._meta.fields]

    class Meta:
        verbose_name_plural = "Sample Context"

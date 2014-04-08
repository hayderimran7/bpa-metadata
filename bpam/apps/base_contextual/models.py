# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.gis.geos import Point
from django.utils.translation import ugettext_lazy as _

from apps.common.models import BPAUniqueID, DebugNote
from apps.base_vocabulary.models import LandUse, HorizonClassification, GeneralEcologicalZone, BroadVegetationType, \
    AustralianSoilClassification, FAOSoilClassification, ProfilePosition, DrainageClassification, SoilColour, \
    TillageType


class CollectionSite(DebugNote):
    """
    Collection Site Information
    """

    country = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    location_name = models.CharField(_('Location Name'), max_length=100, blank=True)
    image_url = models.URLField(_('Site Photo'), blank=True, null=True)
    date_sampled = models.DateField(_('Date Sampled'), null=True)
    # positions = models.ManyToManyField(GPSPosition, null=True, blank=True)
    # TODO make use of geodjango
    lat = models.FloatField(_('Latitude'), help_text=_('Degree decimal'))
    lon = models.FloatField(_('Longitude'), help_text=_('Degree decimal'))
    elevation = models.IntegerField(_('Elevation'), null=True)

    # controlled vocabularies
    current_land_use = models.ForeignKey(LandUse, related_name='current', null=True, verbose_name=_('Current Land Use'))
    general_ecological_zone = models.ForeignKey(GeneralEcologicalZone, null=True,
                                                verbose_name=_('General Ecological Zone'))
    vegetation_type = models.ForeignKey(BroadVegetationType, null=True, verbose_name=_('Vegetation Type'))
    soil_type_australian_classification = models.ForeignKey(AustralianSoilClassification,
                                                            verbose_name=_('Australian Soil Type Classification'),
                                                            null=True)
    soil_type_fao_classification = models.ForeignKey(FAOSoilClassification,
                                                     verbose_name=_('FAO Soil Type Classification'),
                                                     null=True)

    vegetation_total_cover = models.CharField(_('Vegetation Total Cover'), max_length=200,
                                              blank=True)  # free text in column
    vegetation_dominant_trees = models.CharField(_('Vegetation Dominant Trees'), max_length=1000, blank=True)

    slope = models.CharField(max_length=20, blank=True)
    slope_aspect = models.CharField(_('Slope Aspect'),
                                    max_length=100,
                                    blank=True,
                                    help_text=_(u'Direction or degrees; e.g., NW or 315°'))

    profile_position = models.ForeignKey(ProfilePosition, verbose_name=_('Profile Position'), null=True)
    drainage_classification = models.ForeignKey(DrainageClassification, verbose_name=_('Drainage Classification'),
                                                null=True)

    # some history for this site
    environment_event = models.CharField(max_length=100, blank=True)  # fire, flood, extreme, other
    # fire
    fire_history = models.CharField(_('Fire History'), max_length=500, blank=True)
    fire_intensity = models.CharField(_('Fire Intensity'), max_length=500, blank=True)
    # land use
    date_since_change_in_land_use = models.DateField(_('Date Since Land Use Change'), blank=True, null=True)
    immediate_previous_land_use = models.ForeignKey(LandUse, related_name='previous', blank=True, null=True)
    crop_rotation_1 = models.ForeignKey(LandUse,
                                        verbose_name=_('Crop rotation 1 year ago'),
                                        related_name='crop_rotation_1',
                                        max_length=100,
                                        blank=True,
                                        null=True)
    crop_rotation_2 = models.ForeignKey(LandUse,
                                        verbose_name=_('Crop rotation 2 years ago'),
                                        related_name='crop_rotation_2',
                                        max_length=100,
                                        blank=True,
                                        null=True)
    crop_rotation_3 = models.ForeignKey(LandUse,
                                        verbose_name=_('Crop rotation 3 years ago'),
                                        related_name='crop_rotation_3',
                                        max_length=100,
                                        blank=True,
                                        null=True)
    crop_rotation_4 = models.ForeignKey(LandUse,
                                        verbose_name=_('Crop rotation 4 years ago'),
                                        related_name='crop_rotation_4',
                                        max_length=100,
                                        blank=True, null=True)
    crop_rotation_5 = models.ForeignKey(LandUse,
                                        verbose_name=_('Crop rotation 5 years ago'),
                                        related_name='crop_rotation_5',
                                        max_length=100,
                                        blank=True,
                                        null=True)

    agrochemical_additions = models.CharField(_('Agrochemical Additions'), max_length=300, blank=True, null=True)
    tillage = models.ForeignKey(TillageType, blank=True, null=True)

    other_comments = models.TextField(_('Comments'), blank=True, null=True)

    def get_location_name(self):
        """
        Get location name or lon, lat, no location name is available
        """
        if self.location_name:
            return self.location_name
        return u'{0}, {1}'.format(self.lon, self.lat)

    @property
    def geom(self):
        return Point(self.lon, self.lat, srid=4326)

    def __unicode__(self):
        return u','.join(str(s) for s in (self.location_name, self.lat, self.lon,) if s)

    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in CollectionSite._meta.fields]

    class Meta:
        # app_label = 'base'
        verbose_name_plural = _("Collection Sites")
        unique_together = ('lat', 'lon',)


class ChemicalAnalysis(models.Model):
    """
    Chemical Analysis assay
    """

    bpa_id = models.ForeignKey(BPAUniqueID, verbose_name=_('BPA ID'))
    # structural
    depth = models.CharField(max_length=100, blank=True, null=True)
    moisture = models.FloatField(_('Soil Moisture'), blank=True, null=True)
    colour = models.ForeignKey(SoilColour, verbose_name=_('Soil Colour'), null=True)
    gravel = models.CharField(_('Gravel'), max_length=100, blank=True, null=True, help_text=_(u'>2.0mm'))
    texture = models.FloatField(max_length=100, blank=True, null=True)
    course_sand = models.FloatField(blank=True, null=True, help_text=_(u'200-2000 µm'))
    fine_sand = models.FloatField(blank=True, null=True, help_text=_(u'20-200 µm'))
    sand = models.FloatField(blank=True, null=True)
    silt = models.FloatField(blank=True, null=True, help_text=_(u'2-20 µm'))
    clay = models.FloatField(blank=True, null=True, help_text=_(u'<2 µm'))

    # chemical
    ammonium_nitrogen = models.FloatField(_('Ammonium Nitrogen'), blank=True, null=True)
    nitrate_nitrogen = models.CharField(_('Nitrate Nitrogen'), max_length=10, blank=True, null=True)  # <>
    phosphorus_colwell = models.CharField(_('Phosphorus Colwell'), max_length=10, blank=True, null=True)  # <>
    potassium_colwell = models.FloatField(_('Potassium Colwell'), blank=True, null=True)
    sulphur_colwell = models.FloatField(blank=True, null=True)
    organic_carbon = models.FloatField(blank=True, null=True)
    conductivity = models.FloatField(blank=True, null=True)
    # pH
    cacl2_ph = models.FloatField(_('pH Level CaCl2'), blank=True, null=True)
    h20_ph = models.FloatField(_('pH Level H20'), blank=True, null=True)
    # DTPA
    dtpa_copper = models.FloatField(_('DTPA Copper'), blank=True, null=True)
    dtpa_iron = models.FloatField(_('DTPA Iron'), blank=True, null=True)
    dtpa_manganese = models.FloatField(_('DTPA Manganse'), blank=True, null=True)
    dtpa_zinc = models.FloatField(_('DTPA Zinc'), blank=True, null=True)
    # exc
    exc_aluminium = models.FloatField(_('Exc. Aluminium'), blank=True, null=True)
    exc_calcium = models.FloatField(_('Exc. Calsium'), blank=True, null=True)
    exc_magnesium = models.FloatField(_('Exc. Magnesium'), blank=True, null=True)
    exc_potassium = models.FloatField(_('Exc. Potassium'), blank=True, null=True)
    exc_sodium = models.FloatField(_('Exc. Sodium'), blank=True, null=True)
    boron_hot_cacl2 = models.FloatField(_('Boron Hot CaCl2'), blank=True, null=True)

    total_nitrogen = models.FloatField(_('Total Nitrogen'), blank=True, null=True)
    total_carbon = models.FloatField(_('Total Carbon'), blank=True, null=True)

    def __unicode__(self):
        return u"Chemical Analysis for {0}".format(self.bpa_id)

    class Meta:
        # app_label = 'base'
        verbose_name_plural = _("Sample Chemical Essays")


class CollectionSample(DebugNote):
    """
    A sample to collect sample specific info for contextual data.
    """

    bpa_id = models.ForeignKey(BPAUniqueID, verbose_name=_('BPA ID'), primary_key=True)
    site = models.ForeignKey(CollectionSite, null=True)  # there may be no site set

    horizon_classification1 = models.ForeignKey(HorizonClassification,
                                                null=True,
                                                related_name='one',
                                                verbose_name=_('Horizon Classification One'))
    horizon_classification2 = models.ForeignKey(HorizonClassification,
                                                null=True,
                                                related_name='two',
                                                verbose_name=_('Horizon Classification Two'))
    depth = models.CharField(_('Soil Depth'), max_length=20, blank=True)
    methodological_notes = models.TextField(_('Methodological Notes'), blank=True, null=True)

    def get_horizon_description(self):
        """
        String combing horizon classifications
        """
        desc = []
        for c in (self.horizon_classification1, self.horizon_classification2):
            if c is not None:
                desc.append(c.horizon)
        return u",".join(desc)

    def __unicode__(self):
        return u"{0} {1}".format(
            self.bpa_id,
            self.horizon_classification1,
            self.horizon_classification2,
            self.depth)

    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in CollectionSample._meta.fields]


    class Meta:
        verbose_name_plural = _('Collection Samples')


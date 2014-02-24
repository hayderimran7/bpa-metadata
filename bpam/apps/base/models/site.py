from django.db import models
from django.utils.translation import ugettext_lazy as _


class LandUse(models.Model):
    """
    Land use Controlled Vocabulary
    http://lrm.nt.gov.au/soil/landuse/classification
    """

    classification = models.IntegerField(unique=True)
    description = models.CharField(max_length=300)
    note = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return u"{0}".format(self.description)

    class Meta:
        verbose_name_plural = _("Land Uses")
        app_label = 'base'


class SiteOwner(models.Model):
    """
    The Site Owner
    """

    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField()
    address = models.TextField(blank=True)
    note = models.TextField(blank=True)

    def __unicode__(self):
        return u"{0} {1}".format(self.name, self.email)

    class Meta:
        app_label = 'base'
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
        return u"Site history on {0}".format(self.history_report_date)

    class Meta:
        app_label = 'base'
        verbose_name_plural = _("Site History")


class CollectionSite(models.Model):
    """
    Collection Site Information
    """

    country = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    location_name = models.CharField(max_length=100, blank=True)
    image_url = models.URLField(_('Site Photo'), blank=True, null=True)

    # positions = models.ManyToManyField(GPSPosition, null=True, blank=True)
    # TODO make use of geodjango
    lat = models.FloatField(_('Latitude'))
    lon = models.FloatField(_('Longitude'))

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
        return u"{0}, {1}, {2} {3}".format(self.country, self.state, self.location_name, self.plot_description)

    class Meta:
        app_label = 'base'
        verbose_name_plural = _("Collection Sites")
        unique_together = ('lat', 'lon',)


class SoilTexture(models.Model):
    """
    Soil Texture
    """
    texture = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=100)

    def __unicode__(self):
        return u"{0} {1}".format(self.texture, self.description)

    class Meta:
        app_label = 'base'


class SoilColour(models.Model):
    """
    Soil Colour
    """
    colour = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=5, unique=True)

    def __unicode__(self):
        return u"{0}".format(self.colour)

    class Meta:
        app_label = 'base'


class GeneralEcologicalZone(models.Model):
    """
    General ecological zone taxonomy
    """

    description = models.CharField(max_length=100, unique=True)
    note = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return u"{0}".format(self.description)

    class Meta:
        verbose_name_plural = _("General Ecological Zones")
        app_label = 'base'


class BroadVegetationType(models.Model):
    """
    Broad Vegetation Type
    """

    vegetation = models.CharField(max_length=100, unique=True)
    note = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return u"{0}".format(self.vegetation)

    class Meta:
        verbose_name_plural = _("Broad Vegetation Types")
        app_label = 'base'


class TillageType(models.Model):
    """
    Note method(s) used for tilling; moldboard plow, chisel, no-till, etc.
    """

    tillage = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __unicode__(self):
        return u"{0}".format(self.tillage)

    class Meta:
        app_label = 'base'
        verbose_name_plural = _("Tillage Types")


class HorizonClassification(models.Model):
    """
    Specific layer in the land area which measures parallel to the soil surface and possesses physical characteristics
    which differ from the layers above and beneath; master horizons (O, A, E,  B, C, R) are rather standard, but
    sub-designations (subordinate distinctions) will vary by country.
    """

    horizon = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __unicode__(self):
        return u"{0}".format(self.horizon)

    class Meta:
        app_label = 'base'
        verbose_name_plural = _("Horizon Classification")


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
        return u"{0} {1}".format(self.authority, self.classification)

    class Meta:
        app_label = 'base'
        verbose_name_plural = _("Soil Classification")


class DrainageClassification(models.Model):
    """
    Drainage classification from a standard system such as the US Department of Agriculture system.
    """

    drainage = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return u"{0}".format(self.drainage)

    class Meta:
        app_label = 'base'
        verbose_name_plural = _("Drainage Classifications")


class ProfilePosition(models.Model):
    """
    Cross-sectional position in the hill slope where sample was collected; sample area position in relation to
    surrounding areas
    """

    position = models.CharField(max_length=20)

    def __unicode__(self):
        return u"{0}".format(self.position)

    class Meta:
        app_label = 'base'
        verbose_name_plural = _("Profile Positions")

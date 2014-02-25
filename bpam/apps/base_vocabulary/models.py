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


class SoilTexture(models.Model):
    """
    Soil Texture
    """
    texture = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=100)

    def __unicode__(self):
        return u"{0} {1}".format(self.texture, self.description)



class SoilColour(models.Model):
    """
    Soil Colour
    """
    colour = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=5, unique=True)

    def __unicode__(self):
        return u"{0}".format(self.colour)


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


class TillageType(models.Model):
    """
    Note method(s) used for tilling; moldboard plow, chisel, no-till, etc.
    """

    tillage = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __unicode__(self):
        return u"{0}".format(self.tillage)

    class Meta:
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
        verbose_name_plural = _("Profile Positions")

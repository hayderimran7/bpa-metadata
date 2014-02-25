from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.common.models import BPAUniqueID
from apps.base_vocabulary.models import LandUse


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
        # app_label = 'base'
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
        # app_label = 'base'
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
        # app_label = 'base'
        verbose_name_plural = _("Collection Sites")
        unique_together = ('lat', 'lon',)


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
        # app_label = 'base'
        verbose_name_plural = _("Sample Chemical Essays")



from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.common.models import BPAUniqueID


class Sheet(models.Model):
    """ Single herbarium sheet """

    sheet_number = models.IntegerField("Sheet Number", primary_key=True)
    bpa_id = models.OneToOneField(BPAUniqueID, verbose_name=_('BPA ID'), null=True, blank=True)

    name_id = models.TextField("Name ID", null=True, blank=True)
    plant_description = models.TextField("Plant Description", null=True, blank=True)
    site_description = models.TextField("Site Description", null=True, blank=True)
    vegetation = models.TextField("Vegetation", null=True, blank=True)

    # position
    latitude = models.FloatField("Latitude", help_text="Degree decimal")
    longitude = models.FloatField("Longitude", help_text="Degree decimal")
    datum = models.CharField("Datum", max_length=50, null=True, blank=True)
    geocode_accuracy = models.FloatField("Geocode Accuracy", max_length=100, null=True, blank=True)
    geocode_method = models.CharField("Gecode Method", max_length=100, null=True, blank=True)
    barker_coordinate_accuracy_flag = models.IntegerField("Barker Coordinate Accuracy Flag", null=True, blank=True)

    # flora
    family = models.CharField("Family", max_length=100, null=True, blank=True)
    genus = models.CharField("Genus", max_length=100, null=True, blank=True)
    species = models.CharField("Species", max_length=100, null=True, blank=True)
    rank = models.CharField("Rank", max_length=100, null=True, blank=True)
    infraspecies_qualifier = models.CharField("Infraspecies Qualifier", max_length=100, null=True, blank=True)
    infraspecies = models.CharField("Infraspecies", max_length=100, null=True, blank=True)
    alien = models.BooleanField("Alien", default=False)

    # determination
    author = models.CharField("Author", max_length=100, null=True, blank=True)
    manuscript = models.CharField("Manuscript", max_length=100, null=True, blank=True)
    conservation_code = models.CharField("Conservation Code", max_length=100, null=True, blank=True)
    determiner_name = models.CharField("Determiner Name", max_length=100, null=True, blank=True)
    date_of_determination = models.DateField("Date of Determination", null=True, blank=True)
    determiner_role = models.CharField("Determiner Role", max_length=100, null=True, blank=True)
    name_comment = models.TextField("Name Comment", null=True, blank=True)
    frequency = models.CharField("Frequency", max_length=100, null=True, blank=True)
    locality = models.TextField("Locality", null=True, blank=True)
    state = models.CharField("State", max_length=100, null=True, blank=True)

    # collector
    collector = models.CharField("Collector", max_length=100, null=True, blank=True)
    collector_number = models.CharField("Collector Number", max_length=100, null=True, blank=True)
    collection_date = models.DateField("Collection Date", null=True, blank=True)
    voucher = models.TextField("Voucher", null=True, blank=True)
    voucher_id = models.IntegerField("Voucher ID", null=True, blank=True)
    voucher_site = models.CharField("Voucher Site", max_length=300, null=True, blank=True)
    type_status = models.CharField("Type Status", max_length=300, null=True, blank=True)

    note = models.TextField("Note", null=True, blank=True)

    @property
    def get_site_description(self):
        """ Get collection site description or lat, lon if no location name is available """

        if self.site_description:
            return u'{:4.4f}, {:4.4f} ({})'.format(self.latitude, self.longitude, self.site_description[:20])
        return u'{:4.4f}, {:4.4f}'.format(self.latitude, self.longitude)

    @property
    def get_classification(self):
        """ Plant classification """

        return u'{} {} {}'.format(self.family, self.genus, self.species)

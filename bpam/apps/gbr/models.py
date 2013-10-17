import urlparse
import urllib

from django.db import models
from django.conf import settings

from apps.bpaauth.models import BPAUser
from apps.common.models import Sample, Run, BPAUniqueID, SequenceFile, Organism, URLVerification
from django.utils.translation import ugettext_lazy as _

class Collection(models.Model):
    """
    Data surrounding a Coral collection
    """

    type = models.CharField(max_length=100)
    site = models.CharField(max_length=100)
    date = models.DateField()
    gps_location = models.CharField(max_length=100) # FIXME, nice geo types
    water_temperature = models.IntegerField()
    water_ph = models.IntegerField()
    depth = models.IntegerField()
    note = models.TextField(blank=True)

    def __unicode__(self):
        return u"{0} {1} {2}".format(self.type, self.site, self.date)

class GBRSample(Sample):
    """
    GBR specific Sample
    """

    organism = models.ForeignKey(Organism)
    passage_number = models.IntegerField(null=True)
    dataset = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    dna_concentration = models.FloatField(null=True, blank=True)
    total_dna = models.FloatField(null=True, blank=True)
    collection_site = models.CharField(max_length=100, null=True, blank=True)
    collector = models.CharField(max_length=100, null=True, blank=True)
    # this could be normalised to float (lat, lng) but then input in the admin might be tricky?
    gps_location = models.CharField(max_length=100, null=True, blank=True)
    water_temp = models.FloatField(null=True, blank=True)
    ph = models.FloatField(null=True, blank=True)
    depth = models.FloatField(null=True, blank=True)
    other = models.TextField(null=True, blank=True)
    sequencing_notes = models.TextField(null=True, blank=True)
    dna_rna_concentration = models.FloatField(null=True, blank=True)
    total_dna_rna_shipped = models.FloatField(null=True, blank=True)
    comments_by_facility = models.TextField(null=True, blank=True)
    sequencing_data_eta = models.DateField(blank=True, null=True)
    date_sequenced = models.DateField(blank=True, null=True)
    requested_read_length = models.IntegerField(blank=True, null=True)
    contact_bioinformatician = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)

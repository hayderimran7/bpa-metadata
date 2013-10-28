import urlparse
import urllib

from django.db import models
from django.conf import settings

from apps.bpaauth.models import BPAUser
from apps.common.models import Protocol, Sample, Run, BPAUniqueID, SequenceFile, Organism, URLVerification, DebugNote

from django.utils.translation import ugettext_lazy as _


class CollectionEvent(models.Model):
    """
    Data surrounding a Coral collection
    """

    name = models.CharField(max_length=100, null=True, blank=True)
    collection_date = models.DateField(blank=True, null=True)
    collector = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='collector')
    # this could be normalised to float (lat, lng) but then input in the admin might be tricky?
    gps_location = models.CharField(max_length=100, null=True, blank=True)
    water_temp = models.FloatField(null=True, blank=True)
    water_ph = models.FloatField(null=True, blank=True, verbose_name=_('pH'))
    depth = models.FloatField(null=True, blank=True)

    note = models.TextField(blank=True)

    class Meta:
        unique_together = (('name', 'collection_date'))

    def __unicode__(self):
        return u'{0} {1}'.format(self.name, self.collection_date)


class GBRSample(Sample, DebugNote):
    """
    GBR specific Sample
    """

    organism = models.ForeignKey(Organism)
    dataset = models.CharField(max_length=100, null=True, blank=True)
    dna_concentration = models.FloatField(null=True, blank=True, verbose_name=_('DNA Concentration'))
    total_dna = models.FloatField(null=True, blank=True, verbose_name=_('Total DNA'))

    collection_event = models.ForeignKey(CollectionEvent)

    sequencing_notes = models.TextField(null=True, blank=True, verbose_name=_('Sequencing Notes'))
    dna_rna_concentration = models.FloatField(null=True, blank=True, verbose_name=_('DNA/RNA Concentration'))
    total_dna_rna_shipped = models.FloatField(null=True, blank=True, verbose_name=_('Total DNA/RNA Shipped'))
    comments_by_facility = models.TextField(null=True, blank=True, verbose_name=_('Facility Comments'))
    sequencing_data_eta = models.DateField(blank=True, null=True, verbose_name=_('Sequence ETA'))
    date_sequenced = models.DateField(blank=True, null=True)
    requested_read_length = models.IntegerField(blank=True, null=True)
    contact_bioinformatician = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,
                                                 related_name='bioinformatician')

    class Meta:
        verbose_name = _('Great Barrier Reef Sample')


class GBRRun(Run):
    """
    A GBR Run
    """
    sample = models.ForeignKey(GBRSample)

    class Meta:
        verbose_name = _('Great Barrier Reef Run')

    def __unicode__(self):
        return u'Run {0} for {1}'.format(self.run_number, self.sample.name)


class GBRProtocol(Protocol):
    run = models.OneToOneField(GBRRun, blank=True, null=True)

    class Meta:
        verbose_name = _('Great Barrier Reef Protocol')


class GBRSequenceFile(SequenceFile):
    """
    Sequence Files resulting from a run
    """

    sample = models.ForeignKey(GBRSample)
    run = models.ForeignKey(GBRRun)
    url_verification = models.OneToOneField(URLVerification, null=True)

    def __unicode__(self):
        return u'Run {0} for {1}'.format(self.run, self.filename)

    def link_ok(self):
        if self.url_verification is not None:
            return self.url_verification.status_ok
        else:
            return False

    # FIXME move this into sequencefile, code duplicated with MelanomaSequenceFile
    def get_url(self):
        bpa_id = self.sample.bpa_id.bpa_id.replace('/', '.')
        uj = urlparse.urljoin
        uq = urllib.quote
        return uj(settings.BPA_BASE_URL, "GBR/%s/%s/%s" % (
            uq(bpa_id),
            uq(self.run.flow_cell_id),
            uq(self.filename)))

    url = property(get_url)

    class Meta:
        verbose_name = _('Great Barrier Reef Sequence File')
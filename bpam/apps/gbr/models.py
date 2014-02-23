from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from apps.common.models import Protocol, Sample, Run, SequenceFile, Organism, DebugNote


class CollectionEvent(models.Model):
    """
    Data surrounding a Coral collection
    """

    site_name = models.CharField(_('Site Name'), max_length=100, null=True, blank=True)
    collection_date = models.DateField(_('Collection Date'), blank=True, null=True)
    collector = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='collector')
    # this could be normalised to float (lat, lng) but then input in the admin might be tricky?
    gps_location = models.CharField(_('GPS Location'), max_length=100, null=True, blank=True)
    water_temp = models.FloatField(_('Water Temperature'), null=True, blank=True)
    water_ph = models.FloatField(_('Water pH'), null=True, blank=True)
    depth = models.CharField(_('Water Depth'), max_length=20, null=True, blank=True)

    note = models.TextField(blank=True)

    class Meta:
        unique_together = (('site_name', 'collection_date'))

    def __unicode__(self):
        return u'{0} {1}'.format(self.site_name, self.collection_date)


class GBRSample(Sample, DebugNote):
    """
    GBR specific Sample
    """

    organism = models.ForeignKey(Organism)
    dataset = models.CharField(max_length=100, null=True, blank=True)
    collection_event = models.ForeignKey(CollectionEvent)
    sequencing_notes = models.TextField(null=True, blank=True, verbose_name=_('Sequencing Notes'))
    dna_rna_concentration = models.FloatField(null=True, blank=True, verbose_name=_('DNA/RNA Concentration (ng/uL)'))
    total_dna_rna_shipped = models.FloatField(null=True, blank=True, verbose_name=_('Total DNA/RNA Shipped'))
    comments_by_facility = models.TextField(null=True, blank=True, verbose_name=_('Facility Comments'))
    sequencing_data_eta = models.DateField(blank=True, null=True, verbose_name=_('Sequence ETA'))
    date_sequenced = models.DateField(blank=True, null=True)
    requested_read_length = models.IntegerField(blank=True, null=True)
    contact_bioinformatician = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,
                                                 related_name='bioinformatician')


class GBRRun(Run):
    """
    A GBR Run
    """
    sample = models.ForeignKey(GBRSample)

    def __unicode__(self):
        return u'Run #{0} for Sample:{1}'.format(self.run_number, self.sample.name)


class GBRProtocol(Protocol):
    run = models.ForeignKey(GBRRun, blank=True, null=True)


class GBRSequenceFile(SequenceFile):
    """
    Sequence Files resulting from a run
    """

    sample = models.ForeignKey(GBRSample)
    run = models.ForeignKey(GBRRun)
    project_name = 'gbr'

    def __unicode__(self):
        return u'Run {0} for {1}'.format(self.run, self.filename)

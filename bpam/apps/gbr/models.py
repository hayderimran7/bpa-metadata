from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from apps.common.models import Protocol, Sample, Run, SequenceFile, Organism, DebugNote


class CollectionSite(models.Model):
    """
    Coral Collection Site
    """
    site_name = models.CharField(_('Site Name'), max_length=100, null=True, blank=True)
    lat = models.FloatField(_('Latitude'), help_text=_('Degree decimal'))
    lon = models.FloatField(_('Longitude'), help_text=_('Degree decimal'))
    note = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = _('Coral Collection Sites')
        unique_together = ('lat', 'lon',)

    def __unicode__(self):
        return u'{0} {1}, {2}'.format(self.site_name, self.lat, self.lon)

    def get_name(self):
        """
        Get site name or lat, lon if no location name is available
        """
        if self.site_name.strip() != '':
            return self.site_name
        return u'{0}, {1}'.format(self.lat, self.lon)


class CollectionEvent(models.Model):
    """
    Data surrounding a Coral collection
    """
    site = models.ForeignKey(CollectionSite, null=True)
    collection_date = models.DateField(_('Collection Date'), blank=True, null=True)
    collector = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='collector')
    water_temp = models.FloatField(_('Water Temperature'), null=True, blank=True)
    water_ph = models.FloatField(_('Water pH'), null=True, blank=True)
    depth = models.CharField(_('Water Depth'), max_length=20, null=True, blank=True)

    note = models.TextField(blank=True)

    def __unicode__(self):
        return u'{0} {1}'.format(self.site.site_name, self.collection_date, self.collector)


class GBRSample(Sample, DebugNote):
    """
    GBR specific Sample
    """

    organism = models.ForeignKey(Organism, null=True)
    collection_event = models.ForeignKey(CollectionEvent, null=True)

    dataset = models.CharField(_('Data Set'), max_length=100, null=True, blank=True)
    sequencing_notes = models.TextField(_('Sequencing Notes'), null=True, blank=True)
    dna_rna_concentration = models.FloatField(_('DNA/RNA Concentration'), null=True, blank=True)
    total_dna_rna_shipped = models.FloatField(_('Total DNA/RNA Shipped'), null=True, blank=True)
    comments_by_facility = models.TextField(_('Facility Comments'), null=True, blank=True)
    sequencing_data_eta = models.DateField(_('Sequence ETA'), blank=True, null=True)
    date_sequenced = models.DateField(_('Date Sequenced'), blank=True, null=True)
    requested_read_length = models.IntegerField(_('Requested Read Length'), blank=True, null=True)
    contact_bioinformatician = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,
                                                 related_name='bioinformatician',
                                                 verbose_name=_('Contact Bioinformatician'))

    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in GBRSample._meta.fields]


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

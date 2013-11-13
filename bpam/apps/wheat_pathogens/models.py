import urlparse
import urllib

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from apps.common.models import Protocol, Sample, Run, SequenceFile, Organism, URLVerification, DebugNote


class PathogenSample(Sample, DebugNote):
    """
    Wheat pathogen specific Sample
    """

    organism = models.ForeignKey(Organism)
    dataset = models.CharField(max_length=100, null=True, blank=True)
    dna_concentration = models.FloatField(null=True, blank=True, verbose_name=_('DNA Concentration'))
    total_dna = models.FloatField(null=True, blank=True, verbose_name=_('Total DNA'))

    sequencing_notes = models.TextField(null=True, blank=True, verbose_name=_('Sequencing Notes'))
    dna_rna_concentration = models.FloatField(null=True, blank=True, verbose_name=_('DNA/RNA Concentration'))
    total_dna_rna_shipped = models.FloatField(null=True, blank=True, verbose_name=_('Total DNA/RNA Shipped'))
    comments_by_facility = models.TextField(null=True, blank=True, verbose_name=_('Facility Comments'))
    sequencing_data_eta = models.DateField(blank=True, null=True, verbose_name=_('Sequence ETA'))
    date_sequenced = models.DateField(blank=True, null=True)
    requested_read_length = models.IntegerField(blank=True, null=True)
    contact_bioinformatician = models.ForeignKey(settings.AUTH_USER_MODEL,
                                                 blank=True,
                                                 null=True,
                                                 related_name='wheat_pathogen_bioinformatician')

    class Meta:
        verbose_name = _('Wheat Pathogen Sample')


class PathogenRun(Run):
    """
    A Wheat Pathogen Run
    """
    sample = models.ForeignKey(PathogenSample)

    class Meta:
        verbose_name = _('Wheat pathogen Run')

    def __unicode__(self):
        return u'Run {0} for {1}'.format(self.run_number, self.sample.name)


class PathogenProtocol(Protocol):
    run = models.OneToOneField(PathogenRun, blank=True, null=True)

    class Meta:
        verbose_name = _('Great Barrier Reef Protocol')


class PathogenSequenceFile(SequenceFile):
    """
    Sequence Files resulting from a run
    """

    sample = models.ForeignKey(PathogenSample)
    run = models.ForeignKey(PathogenRun)
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
        return uj(settings.BPA_BASE_URL, "wheat_pathogen/%s/%s/%s" % (
            uq(bpa_id),
            uq(self.run.flow_cell_id),
            uq(self.filename)))

    url = property(get_url)

    class Meta:
        verbose_name = _('Wheat Pathogen Sequence File')
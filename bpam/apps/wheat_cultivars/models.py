import urlparse
import urllib

from django.db import models
from django.conf import settings

from apps.common.models import Protocol, Sample, Run, SequenceFile, URLVerification, DebugNote, Organism


class CultivarSample(Sample, DebugNote):
    """
    Wheat pathogen specific Sample
    """

    organism = models.ForeignKey(Organism)
    sample_label = models.CharField(max_length=200, null=True, blank=True)
    cultivar_code = models.CharField(max_length=3, null=True, blank=True)
    extract_name = models.CharField(max_length=200, null=True, blank=True)
    protocol_reference = models.CharField(max_length=100, null=True, blank=True)
    casava_version = models.CharField(max_length=10, null=True, blank=True)


class CultivarRun(Run):
    """
    A Wheat Cultivar Run
    """
    sample = models.ForeignKey(CultivarSample)

    def __unicode__(self):
        return u'Run {0} for {1}'.format(self.run_number, self.sample.name)


class CultivarProtocol(Protocol):
    run = models.OneToOneField(CultivarRun, blank=True, null=True)


class CultivarSequenceFile(SequenceFile):
    """
    Sequence Files resulting from a run
    """

    sample = models.ForeignKey(CultivarSample)
    run = models.ForeignKey(CultivarRun)
    corrected_sequence_filename = models.CharField(max_length=200, null=True, blank=True)
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
        return uj(settings.BPA_BASE_URL, "wheat_cultivars/%s/%s/%s" % (
            uq(bpa_id),
            uq(self.run.flow_cell_id),
            uq(self.filename)))

    url = property(get_url)


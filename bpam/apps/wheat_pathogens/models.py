import urlparse
import urllib

from django.db import models
from django.conf import settings

from apps.common.models import Protocol, Sample, Run, SequenceFile, Organism, URLVerification, DebugNote


class PathogenSample(Sample, DebugNote):
    """
    Wheat pathogen specific Sample
    """
    organism = models.ForeignKey(Organism)
    official_variety_name = models.CharField(max_length=200, null=True, blank=True)
    original_source_host_species = models.CharField(max_length=200, null=True, blank=True)
    collection_location = models.CharField(max_length=200, null=True, blank=True)
    sample_label = models.CharField(max_length=200, null=True, blank=True)
    wheat_pathogenicity = models.CharField(max_length=200, null=True, blank=True)

    date_sequenced = models.DateField(blank=True, null=True)


class PathogenRun(Run):
    """
    A Wheat Pathogen Run
    """
    sample = models.ForeignKey(PathogenSample)

    def __unicode__(self):
        return u'Run {0} for {1}'.format(self.run_number, self.sample.name)


class PathogenProtocol(Protocol):
    run = models.OneToOneField(PathogenRun, blank=True, null=True)


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
        return uj(settings.BPA_BASE_URL, "Wheat_Pathogens/%s/%s/%s" % (
            uq(bpa_id),
            uq(self.run.flow_cell_id),
            uq(self.filename)))

    url = property(get_url)

from django.db import models

from apps.common.models import Protocol, Sample, Run, SequenceFile, DebugNote, Organism


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


class CultivarProtocol(Protocol):
    run = models.ForeignKey('CultivarRun', blank=True, null=True)


class CultivarRun(Run):
    """
    A Wheat Cultivar Run
    """
    sample = models.ForeignKey(CultivarSample)
    protocol = models.ForeignKey(CultivarProtocol, blank=True, null=True)

    def __unicode__(self):
        return u'Run {0} for {1}'.format(self.run_number, self.sample.name)


class CultivarSequenceFile(SequenceFile):
    """
    Sequence Files resulting from a run
    """
    project_name = 'wheat_cultivars'
    sample = models.ForeignKey(CultivarSample)
    run = models.ForeignKey(CultivarRun)
    original_sequence_filename = models.CharField(max_length=200, null=True, blank=True)

    def __unicode__(self):
        return u'Run {0} for {1}'.format(self.run, self.filename)

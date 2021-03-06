from django.db import models

from apps.common.models import Protocol, Sample, Run, SequenceFile, DebugNote


class WheatPathogenTranscriptSample(Sample, DebugNote):
    """
    Wheat pathogen Transcript specific Sample
    """
    project = models.CharField(max_length=200, null=True, blank=True)
    sample_label = models.CharField(max_length=200, null=True, blank=True)
    index = models.CharField(max_length=6, null=True, blank=True)
    institution = models.CharField(max_length=200, null=True, blank=True)
    species = models.CharField(max_length=100, null=True, blank=True)
    sample_type = models.CharField(max_length=20, null=True, blank=True)
    extraction_method = models.TextField(null=True, blank=True)
    growth_protocol = models.TextField(null=True, blank=True)
    treatment_protocol = models.TextField(null=True, blank=True)
    experimental_design = models.TextField(null=True, blank=True)


class WheatPathogenTranscriptProtocol(Protocol):
    run = models.ForeignKey('WheatPathogenTranscriptRun', blank=True, null=True)


class WheatPathogenTranscriptRun(Run):
    """
    A Wheat Pathogen Run
    """
    sample = models.ForeignKey(WheatPathogenTranscriptSample)
    protocol = models.ForeignKey(WheatPathogenTranscriptProtocol, blank=True, null=True)

    def __unicode__(self):
        return u'Run {0} for {1}'.format(self.run_number, self.sample.name)


class WheatPathogenTranscriptSequenceFile(SequenceFile):
    """
    Sequence Files resulting from a run
    """
    project_name = 'wheat_pathogens_transcript'
    sample = models.ForeignKey(WheatPathogenTranscriptSample)
    run = models.ForeignKey(WheatPathogenTranscriptRun)
    file_size = models.CharField(max_length=10, null=True, blank=True)

    def __unicode__(self):
        return u'Run {0} for {1}'.format(self.run, self.filename)

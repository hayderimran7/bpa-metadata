from django.db import models

from apps.common.models import Protocol, Sample, Run, SequenceFile, Organism, DebugNote


class WheatPathogenTranscriptSample(Sample, DebugNote):
    """
    Wheat pathogen Transcript specific Sample
    """
    organism = models.ForeignKey(Organism)
    official_variety_name = models.CharField(max_length=200, null=True, blank=True)
    original_source_host_species = models.CharField(max_length=200, null=True, blank=True)
    collection_location = models.CharField(max_length=200, null=True, blank=True)
    sample_label = models.CharField(max_length=200, null=True, blank=True)

    date_sequenced = models.DateField(blank=True, null=True)
    index = models.CharField(max_length=6, null=True, blank=True)
    library_id = models.CharField(max_length=20, null=True, blank=True)


class PathogenProtocol(Protocol):
    run = models.OneToOneField('WheatPathogenTranscriptRun', blank=True, null=True)


class WheatPathogenTranscriptRun(Run):
    """
    A Wheat Pathogen Run
    """
    sample = models.ForeignKey(WheatPathogenTranscriptSample)
    protocol = models.ForeignKey(PathogenProtocol, blank=True, null=True)

    def __unicode__(self):
        return u'Run {0} for {1}'.format(self.run_number, self.sample.name)


class WheatPathogenTranscriptSequenceFile(SequenceFile):
    """
    Sequence Files resulting from a run
    """
    project_name = 'Wheat_Pathogens_Transcript'
    sample = models.ForeignKey(WheatPathogenTranscriptSample)
    run = models.ForeignKey(WheatPathogenTranscriptRun)
    file_size = models.CharField(max_length=10, null=True, blank=True)

    def __unicode__(self):
        return u'Run {0} for {1}'.format(self.run, self.filename)

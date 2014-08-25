from django.db import models

from apps.common.models import Protocol, Sample, Run, SequenceFile, Organism, DebugNote


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
    index = models.CharField(max_length=6, null=True, blank=True)


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
    project_name = 'Wheat_Pathogens'
    sample = models.ForeignKey(PathogenSample)
    run = models.ForeignKey(PathogenRun)
    file_size = models.CharField(max_length=10, null=True, blank=True)

    def __unicode__(self):
        return u'Run {0} for {1}'.format(self.run, self.filename)

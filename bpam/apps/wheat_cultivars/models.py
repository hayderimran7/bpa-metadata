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


class CultivarProtocol(Protocol):
    casava_version = models.CharField(max_length=10, null=True, blank=True)

class CultivarSequenceFile(SequenceFile):
    """
    Sequence Files resulting from a run
    """

    project_name = 'wheat_cultivars'
    sample = models.ForeignKey(CultivarSample)
    original_sequence_filename = models.CharField(max_length=200, null=True, blank=True)
    run_number = models.IntegerField(null=True, blank=True)


    def __unicode__(self):
        return u'Run {0} for {1}'.format(self.run, self.filename)

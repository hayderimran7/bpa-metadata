from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.common.models import Sample, SequenceFile, Run, DebugNote


class MetagenomicsSample(Sample, DebugNote):
    """
    BASE Meta genomics Soil Sample
    """

    def __unicode__(self):
        return u"{0}".format(self.name)

    class Meta:
        app_label = 'base'
        verbose_name_plural = _("Metagenomics Sample")


class MetagenomicsRun(Run):
    """
    A Meta genomics sequence file generation Run
    """
    sample = models.ForeignKey(MetagenomicsSample)

    def __unicode__(self):
        return u'Run {0} for {1}'.format(self.run_number, self.sample.name)

    class Meta:
        app_label = 'base'
        verbose_name_plural = _("Metagenomics Run")


class MetagenomicsSequenceFile(SequenceFile):
    """
    Meta genomics Sequence File
    """

    sample = models.ForeignKey(MetagenomicsSample)
    run = models.ForeignKey(MetagenomicsRun, null=True)  # FIXME

    class Meta:
        app_label = 'base'
        verbose_name_plural = _("Metagenomics Sequence Files")

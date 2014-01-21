from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.common.models import Sample, SequenceFile, Run


class MetagenomicsSample(Sample):
    """
    base Metagenomics Soil Sample
    """

    def __unicode__(self):
        return u"{0}".format(self.name)

    class Meta:
        app_label = 'base'
        verbose_name_plural = _("Metagenomics Sample")


class MetagenomicsSequenceFile(SequenceFile):
    """
    Metagenomics Sequence File
    """

    sample = models.ForeignKey(MetagenomicsSample)

    class Meta:
        app_label = 'base'
        verbose_name_plural = _("Metagenomics Sequence Files")


class MetagenomicsRun(Run):
    """
    A Metagenomics sequence file generation Run
    """
    sample = models.ForeignKey(MetagenomicsSample)

    def __unicode__(self):
        return u'Run {0} for {1}'.format(self.run_number, self.sample.name)

    class Meta:
        app_label = 'base'
        verbose_name_plural = _("Metagenomics Run")

from django.utils.translation import ugettext_lazy as _
from django.db import models

from apps.common.models import SequenceFile, Run
from apps.base.models import BASESample


class MetagenomicsSample(BASESample):
    """
    BASE Meta genomics Soil Sample
    """

    def __unicode__(self):
        return u"{0}".format(self.name)

    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in MetagenomicsSample._meta.fields]

    class Meta:
        verbose_name_plural = _("Metagenomics Sample")


class MetagenomicsRun(Run):
    """
    A Meta genomics sequence file generation Run
    """
    sample = models.ForeignKey(MetagenomicsSample)

    def __unicode__(self):
        return u'Run {0} for {1}'.format(self.run_number, self.sample.name)

    class Meta:
        verbose_name_plural = _("Metagenomics Run")


class MetagenomicsSequenceFile(SequenceFile):
    """
    Metagenomics Sequence File
    """
    project_name = 'base_metagenomics'

    sample = models.ForeignKey(MetagenomicsSample)
    run = models.ForeignKey(MetagenomicsRun, null=True)

    class Meta:
        verbose_name_plural = _("Metagenomics Sequence Files")

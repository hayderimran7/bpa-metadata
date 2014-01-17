from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.common.models import Sample, SequenceFile


class SoilMetagenomicsSample(Sample):
    """
    BASE Metagenomics Soil Sample
    """

    def __unicode__(self):
        return u"{0}".format(self.name)

    class Meta:
        app_label = 'base'
        verbose_name_plural = _("Soil Metagenomics Sample")


class MetagenomicsSequenceFile(SequenceFile):
    """
    Metagenomics Sequence File
    """

    sample = models.ForeignKey(SoilMetagenomicsSample)

    class Meta:
        app_label = 'base'
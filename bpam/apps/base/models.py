from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.common.models import Sample, DebugNote

from apps.base_otu.models import OperationalTaxonomicUnit, SampleOTU


class BASESample(Sample, DebugNote):
    """
    BASE sample
    """

    otus = models.ManyToManyField(OperationalTaxonomicUnit, through=SampleOTU)

    def __unicode__(self):
        return u"{0}: {1}".format(self.name, self.bpa_id)

    class Meta:
        # abstract = True
        verbose_name_plural = _("Biome of Australia Soil Environment Samples")

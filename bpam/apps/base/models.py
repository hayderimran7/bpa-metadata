from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.common.models import Sample, DebugNote


#from apps.base_metagenomics.models import MetagenomicsSample
#from apps.base_otu.models import OperationalTaxonomicUnit


class BaseSample(Sample, DebugNote):
    """
    BASE sample
    """
    otu = models.ManyToManyField('base_otu.OperationalTaxonomicUnit', through='base_otu.SampleOTU')

    def __unicode__(self):
        return u"{0}: {1}".format(self.name, self.bpa_id)

    class Meta:
        # abstract = True
        verbose_name_plural = _("BASE Samples")
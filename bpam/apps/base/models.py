from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.common.models import Sample, DebugNote

# from apps.base_otu.models import OperationalTaxonomicUnit, SampleOTU


class BASESample(Sample, DebugNote):
    """
    BASE sample
    """

    # otus = models.ManyToManyField(OperationalTaxonomicUnit, through=SampleOTU)

    def __unicode__(self):
        return u"{0}".format(self.bpa_id)

    class Meta:
        # abstract = True
        verbose_name_plural = _("Biome of Australia Soil Environment Samples")

    @property
    def context(self):
        try:
            from apps.base_contextual.models import SampleContext

            return SampleContext.objects.get(bpa_id=self.bpa_id)
        except SampleContext.DoesNotExist:
            return None

    @property
    def chemical_analysis(self):
        try:
            from apps.base_contextual.models import ChemicalAnalysis

            return ChemicalAnalysis.objects.get(bpa_id=self.bpa_id)
        except ChemicalAnalysis.DoesNotExist:
            return None

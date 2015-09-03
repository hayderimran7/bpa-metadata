from django.db import models
from django.utils.translation import ugettext_lazy as _
from apps.common.models import Protocol, Sample, Run, SequenceFile, DebugNote, Organism


class CultivarSample(Sample, DebugNote):
    """
    Wheat pathogen specific Sample
    """

    sample_label = models.CharField(max_length=200, null=True, blank=True)

    source_name = models.CharField(_("Source"), max_length=50, null=True, blank=True)
    cultivar_code = models.CharField(_("Code"), max_length=3, null=True, blank=True)
    characteristics = models.CharField(_("Characteristics"), max_length=100, null=True, blank=True)
    variety = models.CharField(_("Variety"), max_length=100, null=True, blank=True)

    organism = models.ForeignKey(Organism)
    organism_part = models.CharField(_("Organism Part"), max_length=100, null=True, blank=True)
    pedigree = models.CharField(_("Pedigree"), max_length=200, null=True, blank=True)
    dev_stage = models.CharField(_("Developmental Stage"), max_length=200, null=True, blank=True)
    yield_properties = models.CharField(_("Yield"), max_length=200, null=True, blank=True)
    morphology = models.CharField(_("Morphology"), max_length=200, null=True, blank=True)
    maturity = models.CharField(_("Maturity"), max_length=200, null=True, blank=True)

    pathogen_tolerance = models.CharField(_("Pathogen Tolerance"), max_length=200, null=True, blank=True)
    drought_tolerance = models.CharField(_("Drought Tolerance"), max_length=200, null=True, blank=True)
    soil_tolerance = models.CharField(_("Soil Tolerance"), max_length=200, null=True, blank=True)

    classification = models.CharField(_("Classification"), max_length=200, null=True, blank=True)
    url = models.URLField(_("URL"), null=True, blank=True)


class CultivarProtocol(Protocol):
    casava_version = models.CharField(max_length=10, null=True, blank=True)

class CultivarSequenceFile(SequenceFile):
    """
    Sequence Files resulting from a run
    """

    project_name = 'wheat_cultivars'
    sample = models.ForeignKey(CultivarSample)
    run_number = models.IntegerField(null=True, blank=True)
    barcode = models.CharField(max_length=20, null=True, blank=True)

    def __unicode__(self):
        return u'Run {0} for {1}'.format(self.run, self.filename)

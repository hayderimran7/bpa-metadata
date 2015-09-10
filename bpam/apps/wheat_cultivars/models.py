from django.db import models
from django.utils.translation import ugettext_lazy as _
from apps.common.models import Sample, SequenceFile, DebugNote, Organism


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
    pedigree = models.TextField(_("Pedigree"), null=True, blank=True)
    dev_stage = models.CharField(_("Developmental Stage"), max_length=200, null=True, blank=True)
    yield_properties = models.CharField(_("Yield"), max_length=200, null=True, blank=True)
    morphology = models.CharField(_("Morphology"), max_length=200, null=True, blank=True)
    maturity = models.CharField(_("Maturity"), max_length=200, null=True, blank=True)

    pathogen_tolerance = models.CharField(_("Pathogen Tolerance"), max_length=200, null=True, blank=True)
    drought_tolerance = models.CharField(_("Drought Tolerance"), max_length=200, null=True, blank=True)
    soil_tolerance = models.CharField(_("Soil Tolerance"), max_length=200, null=True, blank=True)

    classification = models.CharField(_("Classification"), max_length=200, null=True, blank=True)
    url = models.URLField(_("URL"), null=True, blank=True)

class Protocol(models.Model):
    """
    Protocol
    """

    LIB_TYPES = (('PE', 'Paired End'), ('SE', 'Single End'), ('MP', 'Mate Pair'), ('UN', 'Unknown'))
    library_type = models.CharField(_('Type'), max_length=2, choices=LIB_TYPES)
    library_construction = models.CharField(_('Construction'), max_length=200, blank=True, null=True)
    base_pairs = models.IntegerField(_('Base Pairs'), blank=True, null=True)
    library_construction_protocol = models.CharField(_('Construction Protocol'), max_length=200)
    note = models.TextField(blank=True)

    class Meta:
        verbose_name = _('Protocol')
        verbose_name_plural = _('Protocol')

    def __unicode__(self):
        return u'Size:{0}, Type:{1}, Protocol:{2}'.format(self.base_pairs, self.library_type,
                                                          self.library_construction_protocol)

    def set_base_pairs(self, val):
        if val.find("bp") > -1:
            self.base_pairs = int(val[:-2])
        elif val.find("kb") > -1:
            self.base_pairs = int(val[:-2]) * 1000

class CultivarSequenceFile(SequenceFile):
    """
    Sequence Files resulting from a run
    """

    project_name = 'wheat_cultivars'
    sample = models.ForeignKey(CultivarSample)
    protocol = models.ForeignKey(Protocol)
    run_number = models.IntegerField(null=True, blank=True)
    barcode = models.CharField(max_length=20, null=True, blank=True)
    flowcell = models.CharField(max_length=20, null=True, blank=True)


    casava_version = models.CharField(max_length=10, null=True, blank=True)

    def __unicode__(self):
        return u'Run {0} for {1}'.format(self.run, self.filename)

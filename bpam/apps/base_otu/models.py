from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.common.models import BPAUniqueID
from apps.base.models import BaseSample


class OperationalTaxonomicUnit(models.Model):
    """
    http://en.wikipedia.org/wiki/Operational_taxonomic_unit
    """

    name = models.CharField(max_length=30)
    KINGDOMS = (('Bacteria', 'Bacteria'),
                ('Archea', 'Archea'),
                ('Eukaryote', 'Eukaryote'),
                ('Fungi', 'Fungi'))

    kingdom = models.CharField(_('Kingdom'), max_length=100, db_index=True, choices=KINGDOMS)
    phylum = models.CharField(_('Phylum'), max_length=100, db_index=True, default='undefined')
    otu_class = models.CharField(_('Class'), max_length=100, db_index=True, default='undefined')
    order = models.CharField(_('Order'), max_length=100, db_index=True, default='undefined')
    family = models.CharField(_('Family'), max_length=100, db_index=True, default='undefined')
    genus = models.CharField(_('Genus'), max_length=100, db_index=True, default='undefined')
    species = models.CharField(_('Species'), max_length=100, db_index=True, default='undefined')

    class Meta:
        verbose_name_plural = _("OTU")
        unique_together = ('kingdom', 'name',)

    def __unicode__(self):
        return u"{0}:{1}".format(self.kingdom, self.name)


class SampleOTU(models.Model):
    """
    Links Sample with OTU
    """

    sample = models.ForeignKey(BaseSample)
    # bpa_id = models.ForeignKey(BPAUniqueID)
    otu = models.ForeignKey(OperationalTaxonomicUnit)
    count = models.IntegerField(_('OTU Count'))

    class Meta:
        verbose_name_plural = _("OTU to Sample Links")

    def __unicode__(self):
        return u"{0}:{1}:{2}".format(self.sample, self.otu, self.count)


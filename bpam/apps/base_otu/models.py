from django.db import models
from django.utils.translation import ugettext_lazy as _


class OperationalTaxonomicUnit(models.Model):
    """
    http://en.wikipedia.org/wiki/Operational_taxonomic_unit
    """

    name = models.CharField(max_length=30)

    def __unicode__(self):
        return u"{0}".format(self.name)

    class Meta:
        verbose_name_plural = _("OTU")


import urlparse
import urllib
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from apps.common.models import SequenceFile, Run, Protocol
from apps.base.models import BASESample


class MetagenomicsProtocol(Protocol):
    """
    Metagenomics Protocol
    """


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


class Extraction(models.Model):
    """
    Many extractions can be made from a sample.
    """

    sample = models.ForeignKey(MetagenomicsSample)
    extraction_id = models.CharField(_('Extraction ID'), max_length=64)

    library_construction_protocol = models.CharField(_('Library Construction Protocol'), max_length=64, blank=True, null=True)
    sequencer = models.CharField(_('Sequencer'), max_length=64, blank=True, null=True)
    casava_version = models.CharField(_('Casava Version'), max_length=16, blank=True, null=True)
    insert_size_range = models.CharField(_('Insert Size Range'), max_length=64, blank=True, null=True)

    note = models.TextField(blank=True)

    def __unicode__(self):
        return u'Extraction {0} for {1}'.format(self.extraction_id, self.sample.bpa_id)

    class Meta:
        verbose_name_plural = _("Metagenomics Extractions")
        unique_together = (("sample", "extraction_id"),)


class MetagenomicsSequenceFile(SequenceFile):
    """
    Metagenomics Sequence File
    """

    project_name = 'base_metagenomics'
    sample = models.ForeignKey(MetagenomicsSample)
    extraction = models.ForeignKey(Extraction, null=True)
    run = models.ForeignKey(MetagenomicsRun, null=True)
    protocol = models.ForeignKey(MetagenomicsProtocol, null=True)
    index = models.CharField(_('Index'), max_length=32, blank=True, null=True)

    def get_path_parts(self):
        return ('base', 'metagenomics')

    class Meta:
        verbose_name_plural = _("Metagenomics Sequence Files")

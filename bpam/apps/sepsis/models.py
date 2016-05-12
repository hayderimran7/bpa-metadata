from django.db import models

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from apps.common.models import (
    SequenceFile,
    DebugNote,
)

class Host(models.Model, DebugNote):
    """ Host from who sepsis sample was collected"""

    host_description = models.CharField('Host Description', max_length=200, blank=True, null=True)
    host_location = models.CharField('Host Location', max_length=200, blank=True, null=True, help_text="State, Country")
    host_sex = models.CharField('Host Sex', max_length=1, blank=True, null=True, choices=(('M','Male'), ('F', 'Female')))
    host_age = models.IntegerField('Host Age', blank=True, null=True)
    host_dob = models.DateField('Host Day of Birth', blank=True, null=True, help_text="DD/MM/YY")
    host_disease_outcome = models.TextField('Host Disease Outcome', blank=True, null=True)

    class Meta:
        verbose_name = _('Hosts')

    def __unicode__(self):
        return u'{}'.format(self.description)


class Method(models.Model):
    """Sample preparation method"""

    note = models.TextField('Note', max_length=200, blank=True, null=True)
    growth_condition_temperature = models.IntegerField('Growth condition temperature', blank=True, null=True, help_text="Degrees Centigrade")
    growth_condition_time = models.IntegerField('Growth condition time', blank=True, null=True, help_text="Hours")
    growth_condition_media = models.IntegerField('Growth condition media', blank=True, null=True)

    class Meta:
        verbose_name = _('Growth Methods')

    def __unicode__(self):
        return u'{} {} {}'.format(self.growth_condition_media, self.growth_condition_temperature, self.growth_condition_time)

# Little point in expanding the common Sample Type
class SepsisSample(models.Model, DebugNote):
    """ Sepsis Sample """

    bpa_id = models.OneToOneField(BPAUniqueID, primary_key=True, verbose_name='BPA ID')
    taxon_or_organism = models.TextField('Taxon or Organism', max_length=200, blank=True, null=True)
    strain_or_isolate = models.TextField('Strain Or Isolate', max_length=200, blank=True, null=True)
    strain_description = models.TextField('Strain Description', max_length=300, blank=True, null=True)
    gram_stain = models.CharField('Gram Staining', max_length=3, choices=(('POS', 'Positive'), ('NEG', 'Negative')))
    serovar = models.CharField('Serovar', max_length=30, blank=True, null=True)
    key_virulence_genes = models.CharField('Key Virulence Genes', max_length=100, blank=True, null=True)
    isolation_source = models.CharField('Isolation Source', max_length=100, blank=True, null=True)
    publication_reference = models.CharField('Publication Reference', max_length=200, blank=True, null=True)
    contact_researcher = models.CharField('Contact Researcher', max_length=200, blank=True, null=True)
    collection_date = models.DateField('Collection Date', blank=True, null=True, help_text="DD/MM/YY")
    culture_collection_id = models.CharField('Culture Collection ID', max_length=100, blank=True, null=True)

    host = models.ForeignKey(Host, blank=True, null=True, related_name="%(app_label)s_%(class)s_sample")

    def __unicode__(self):
        return u'{0}:{1}, {2}'.format(self.bpa_id, self.taxon_or_organism, self.strain_or_isolate)

    class Meta:
        verbose_name = _('Sepsis Sample')

class SepsisSequenceFile(SequenceFile):
    """ Sequence Files """

    project_name = 'sepsis'
    sample = models.ForeignKey(SepsisSample)

    def __unicode__(self):
        return u'{}'.format(self.filename)

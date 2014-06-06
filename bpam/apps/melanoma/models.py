from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.common.models import Protocol
from apps.common.models import Sample
from apps.common.models import Run
from apps.common.models import BPAUniqueID
from apps.common.models import SequenceFile
from apps.common.models import Organism
from apps.common.models import DebugNote

GENDERS = (('M', 'Male'),
           ('F', 'Female'),
           ('U', 'Unknown'))


class TumorStage(models.Model):
    """
    Tumor Stage
    """

    description = models.CharField(max_length=100)
    note = models.TextField(blank=True)

    def __unicode__(self):
        return u'{0}'.format(self.description)


class Array(models.Model):
    """
    Micro Array ?
    """
    bpa_id = models.ForeignKey(BPAUniqueID, verbose_name=_('BPA ID'))
    array_id = models.CharField(_('Array ID'), max_length=17)
    batch_number = models.IntegerField(_('Batch'))
    well_id = models.CharField(_('Well ID'), max_length=4)
    mia_id = models.CharField(_('MIA ID'), max_length=200)
    call_rate = models.FloatField()
    gender = models.CharField(max_length=1, choices=GENDERS)

    def is_male(self):
        return self.gender == 'M'

    def is_female(self):
        return self.gender == 'F'

    def __unicode__(self):
        return u'{0} {1} {2}'.format(self.bpa_id, self.array_id, self.mia_id)


class MelanomaSample(Sample, DebugNote):
    """
    Melanoma specific Sample
    """
    organism = models.ForeignKey(Organism)

    # don't currently understand what this is.
    passage_number = models.IntegerField(null=True)

    gender = models.CharField(choices=GENDERS, max_length=1, null=True)
    tumor_stage = models.ForeignKey(TumorStage, null=True)
    histological_subtype = models.CharField(max_length=50, null=True)


    def is_male(self):
        return self.gender == 'M'

    def is_female(self):
        return self.gender == 'F'


    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in MelanomaSample._meta.fields]


class MelanomaRun(Run):
    """
    A Melanoma Run
    """

    sample = models.ForeignKey(MelanomaSample)

    def __unicode__(self):
        return u'Run {0} for {1}'.format(self.run_number, self.sample.name)


class MelanomaProtocol(Protocol):
    run = models.OneToOneField(MelanomaRun, blank=True, null=True)


class MelanomaSequenceFile(SequenceFile):
    """
    Sequence Files resulting from a run
    """

    project_name = 'Melanoma'
    sample = models.ForeignKey(MelanomaSample)
    run = models.ForeignKey(MelanomaRun)

    def __unicode__(self):
        return u'Run {0} for {1}'.format(self.run, self.filename)

    def link_ok(self):
        if self.url_verification is not None:
            return self.url_verification.status_ok
        else:
            return False

    @property
    def ingest_issue(self):
        """
        Any issue raised by the ingest process for this file
        """
        if self.url_verification is not None:
            return self.url_verification.status_note
        else:
            return ''



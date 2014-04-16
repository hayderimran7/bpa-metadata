from django.utils.translation import ugettext_lazy as _
from django.db import models

from apps.common.models import SequenceFile, Run, Facility, DebugNote
from apps.base.models import BaseSample


class AmpliconSequencingMetadata(BaseSample, DebugNote):
    """
    BASE Amplicon Soil Sample
    """

    sample_extraction_id = models.CharField(_('Sample Extraction ID'), max_length=200, blank=True, null=True)
    sequencing_facility = models.ForeignKey(Facility,
                                            verbose_name=_('Sequencing facility'),
                                            related_name='base_amplicon',
                                            blank=True,
                                            null=True)

    target = models.CharField(_('Type'), max_length=4,
                              choices=(('16S', '16S'), ('ITS', 'ITS'), ('18S', '18S'), ('A16S', 'A16S')))

    index = models.CharField(_('Index'), max_length=12, blank=True, null=True)

    PASS_OR_FAIL = (('P', 'Pass'), ('F', 'Fail'))
    pcr_1_to_10 = models.CharField(_('PCR 1:10'), max_length=1, blank=True, null=True, choices=PASS_OR_FAIL)
    pcr_1_to_100 = models.CharField(_('PCR 1:100'), max_length=1, blank=True, null=True, choices=PASS_OR_FAIL)
    pcr_neat = models.CharField(_('Neat PCR'), max_length=1, blank=True, null=True, choices=PASS_OR_FAIL)
    dilution = models.CharField(_('Dilution Used'), max_length=5, blank=True, null=True,
                                choices=(('1:10', '1:10'), ('1:100', '1:100'), ('NEAT', 'Neat')))

    analysis_software_version = models.CharField(_('Analysis Software Version'), max_length=100, blank=True, null=True)
    reads = models.IntegerField(_('Number of Reads'), blank=True, null=True)


    def __unicode__(self):
        return u"{0}".format(self.name)

    class Meta:
        verbose_name_plural = _("Amplicon Sequencing Metadata")




class AmpliconSequenceFile(SequenceFile):
    """
    Amplicon Sequence File
    """

    sample = models.ForeignKey(AmpliconSequencingMetadata)

    class Meta:
        verbose_name_plural = _("Amplicon Sequence Files")




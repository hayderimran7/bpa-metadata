from django.utils.translation import ugettext_lazy as _
from django.db import models

from apps.common.models import SequenceFile, Facility, DebugNote, BPAUniqueID, Run
from apps.base.models import BASESample


class AmpliconSequencingMetadata(DebugNote):
    """
    BASE Amplicon Soil Sample
    """

    bpa_id = models.ForeignKey(BPAUniqueID, verbose_name=_('BPA ID'))
    sample_extraction_id = models.CharField(_('Sample Extraction ID'), max_length=200, blank=True, null=True)
    sequencing_facility = models.ForeignKey(Facility,
                                            verbose_name=_('Sequencing Facility'),
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

    sequencing_run_number = models.CharField(_('Sequencing run number'), max_length=40, blank=True, null=True)
    flow_cell_id = models.CharField(_('Flow Cell ID'), max_length=5, blank=True, null=True)
    reads = models.IntegerField(_('Number of Reads'), blank=True, null=True)
    name = models.CharField(_('Sample Name'), max_length=50, blank=True, null=True)
    comments = models.TextField(_('Comments'), blank=True, null=True)

    analysis_software_version = models.CharField(_('Analysis Software Version'), max_length=100, blank=True, null=True)

    def passed_pcr_1_to_10(self):
        return self.pcr_1_to_10 == 'P'

    def passed_pcr_1_to_100(self):
        return self.pcr_1_to_100 == 'P'

    def passed_pcr_neat(self):
        return self.pcr_neat == 'P'

    def __unicode__(self):
        return u'{0}:{1}'.format(self.bpa_id, self.target)

    class Meta:
        verbose_name_plural = _('Amplicon Sequencing Metadata')
        unique_together = (('bpa_id', 'target'),)


class AmpliconRun(Run):
    sample = models.ForeignKey(BASESample, null=True)

    def __unicode__(self):
        return u'{0}'.format(self.sequencing_facility)

class AmpliconSequenceFile(SequenceFile):
    """
    Amplicon Sequence File
    """

    project_name = 'base_amplicon'
    metadata = models.ForeignKey(AmpliconSequencingMetadata)
    run = models.ForeignKey(AmpliconRun)
    sample = models.ForeignKey(BASESample)

    class Meta:
        verbose_name_plural = _("Amplicon Sequence Files")




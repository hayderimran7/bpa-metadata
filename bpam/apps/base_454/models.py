from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from apps.common.models import BPAUniqueID, DebugNote


class Sample454(DebugNote):
    RESULT = (("P", "Pass"), ("F", "Failed"), ("NP", "Not Performed"), ("U", "Unknown"), ("R", "Repeat"))

    bpa_id = models.OneToOneField(BPAUniqueID, unique=True, verbose_name=_("BPA ID"))
    sample_id = models.CharField(_("Sample ID"), max_length=100, blank=True, null=True)
    aurora_purified = models.BooleanField(_("Aurora Purified"), default=False)
    dna_storage_nunc_plate = models.CharField(_("Nunc Plate"), max_length=12, blank=True, null=True, default="")
    dna_storage_nunc_tube = models.CharField(_("Nunc Tube"), max_length=12, blank=True, null=True, default="")
    dna_storage_nunc_well_location = models.CharField(_("Well Location"), max_length=30, blank=True, null=True)
    agrf_batch_number = models.CharField(_("AGRF Batch Number"), max_length=15, blank=True, null=True)
    submitter = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, verbose_name=_("Submitter"), )
    date_received = models.DateField(blank=True, null=True)

    # AGRF Adelaide extraction
    adelaide_extraction_sample_weight = models.CharField(
            _("Extraction Sample Weight (mg)"),
            max_length=30,
            blank=True,
            null=True)  # another abused "integer" field
    adelaide_fluorimetry = models.FloatField(_("Fluorimetry ng/uL gDNA"), blank=True, null=True)
    adelaide_pcr_inhibition = models.CharField(
            _("PCR Inhibition (neat plus spike) 16S (V3-V8)"),
            max_length=2,
            choices=RESULT)
    adelaide_pcr1 = models.CharField(_("PCR1 (neat) 16S (V3-V8)"), max_length=2, choices=RESULT)
    adelaide_pcr2 = models.CharField(_("PCR2 (1:100) 16S (V3-V8)"), max_length=2, choices=RESULT)
    adelaide_date_shipped_to_agrf_454 = models.DateField(_("DNA shipped to AGRF (454)"), blank=True, null=True)
    adelaide_date_shipped_to_agrf_miseq = models.DateField(_("DNA shipped to AGRF (MiSeq)"), blank=True, null=True)
    adelaide_date_shipped_to_ramacciotti = models.DateField(_("DNA shipped to Ramaciotti"), blank=True, null=True)

    # Brisbane 454
    brisbane_16s_mid = models.CharField(_("16S MID"), max_length=7, blank=True, null=True)
    brisbane_its_mid = models.CharField(_("ITS MID"), max_length=7, blank=True, null=True)
    brisbane_16s_pcr1 = models.CharField(_("16S (V1-V3) PCR1 (neat)"), max_length=2, choices=RESULT)
    brisbane_16s_pcr2 = models.CharField(_("16S (V1-V3) PCR2 (1:10)"), max_length=2, choices=RESULT)
    brisbane_16s_pcr3 = models.CharField(_("16S (V1-V3) PCR3 (fusion-primer)"), max_length=2, choices=RESULT)
    brisbane_its_pcr1_neat = models.CharField(_("ITS PCR1 (neat)"), max_length=2, choices=RESULT)
    brisbane_its_pcr2_1_10 = models.CharField(_("ITS PCR1 (1:10)"), max_length=2, choices=RESULT)
    brisbane_its_pcr3_fusion = models.CharField(_("ITS PCR3 (fusion-primer)"), max_length=2, choices=RESULT)
    brisbane_fluorimetry_16s = models.FloatField(_("Fluorimetry ng/uL 16S"), blank=True, null=True)
    brisbane_fluorimetry_its = models.FloatField(_("Fluorimetry ng/uL ITS"), blank=True, null=True)
    brisbane_16s_qpcr = models.FloatField(_("16S qPCR"), blank=True, null=True)
    brisbane_its_qpcr = models.FloatField(_("ITS qPCR"), blank=True, null=True)
    brisbane_i6s_pooled = models.NullBooleanField(_("16S pooled"))
    brisbane_its_pooled = models.NullBooleanField(_("ITS pooled"))
    brisbane_16s_reads = models.IntegerField(_("16S >3000 reads - Trim Back 150bp"), blank=True, null=True)
    brisbane_its_reads = models.IntegerField(_("ITS >3000 reads - Trim Back 150bp Run1"), blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in Sample454._meta.fields]

    def __unicode__(self):
        return u"Soil Sample 454 {0}".format(self.bpa_id)

    class Meta:
        verbose_name_plural = _("Sample 454")

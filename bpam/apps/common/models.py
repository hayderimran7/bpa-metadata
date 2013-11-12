from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from tinymce.models import HTMLField


class BPAProject(models.Model):
    """
    The BPA project
    Examples would be: Melanoma, Coral
    """

    key = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=2000, blank=True)
    note = HTMLField(blank=True)

    class Meta:
        verbose_name = _('BPA Project')
        verbose_name_plural = _("BPA Projects")

    def __unicode__(self):
        return self.name


class BPAUniqueID(models.Model):
    """
    BPA Generated Label
    Each sample should be issued a Unique ID by BPA
    """

    bpa_id = models.CharField(verbose_name=_('BPA ID'), max_length=200, blank=False, primary_key=True, unique=True)
    project = models.ForeignKey(BPAProject)
    note = models.TextField(blank=True)

    class Meta:
        verbose_name = _('BPA Unique ID')
        verbose_name_plural = _("BPA Unique ID's")

    def __unicode__(self):
        return self.bpa_id


class Facility(models.Model):
    """
    The Sequencing Facility
    """

    name = models.CharField(max_length=100)
    note = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = _('Facilities')

    def __unicode__(self):
        return u'{0}'.format(self.name)


class Organism(models.Model):
    """
    An Organism
    """

    genus = models.CharField(max_length=100)
    species = models.CharField(max_length=100, primary_key=True)
    classification = models.URLField('NCBI organismal classification', blank=True)
    note = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = _('Organisms')
        unique_together = ('genus', 'species')

    def name(self):
        return u'{0} {1}'.format(self.genus, self.species)

    def __unicode__(self):
        return self.name()


class DNASource(models.Model):
    """
    DNA Source
    """
    description = models.CharField(max_length=100)
    note = models.TextField(blank=True)

    class Meta:
        verbose_name = _('DNA Source')
        verbose_name_plural = _('DNA Sources')

    def __unicode__(self):
        return self.description


class Sequencer(models.Model):
    """
    The Sequencer
    """

    name = models.CharField(max_length=100, primary_key=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = _('DNA Source')
        verbose_name_plural = _('DNA Sources')

    def __unicode__(self):
        return self.name


class Protocol(models.Model):
    """
    Protocol
    """

    LIB_TYPES = (('PE', 'Paired End'), ('SE', 'Single End'), ('MP', 'Mate Pair'), ('UN', 'Unknown'))
    library_type = models.CharField(max_length=2, choices=LIB_TYPES)
    base_pairs = models.IntegerField(blank=True, null=True)
    library_construction_protocol = models.CharField(max_length=200)
    note = models.TextField(blank=True)

    class Meta:
        abstract = True
        verbose_name_plural = _('Protocol')
        unique_together = ('library_type', 'base_pairs', 'library_construction_protocol')

    def __unicode__(self):
        return u'Size: {0} Type: {1} Protocol: {2}'.format(self.base_pairs, self.library_type,
                                                           self.library_construction_protocol)


class Sample(models.Model):
    """
    The common base Sample
    """

    bpa_id = models.OneToOneField(BPAUniqueID, unique=True, verbose_name=_('BPA ID'))
    contact_scientist = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    dna_source = models.ForeignKey(DNASource, blank=True, null=True, verbose_name=_('DNA Source'))

    name = models.CharField(max_length=200, verbose_name=_('Sample name'))
    dna_extraction_protocol = models.CharField(max_length=200, blank=True, null=True,
                                               verbose_name=_('DNA Extraction Protocol'))
    requested_sequence_coverage = models.CharField(max_length=6, blank=True)
    collection_date = models.DateField(blank=True, null=True)
    date_sent_to_sequencing_facility = models.DateField(blank=True, null=True)

    note = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        return u'{0} {1}'.format(self.bpa_id, self.name)


class Run(models.Model):
    """
    A Single Run.
    This run is abstract and needs to be extended in the client application with the specific sample, at least.
    """

    DNA_extraction_protocol = models.CharField(max_length=200, blank=True)
    passage_number = models.IntegerField(blank=True, null=True)

    # facilities
    sequencing_facility = models.ForeignKey(Facility,
                                            verbose_name=_('Sequencing'),
                                            related_name='+',
                                            blank=True,
                                            null=True)
    whole_genome_sequencing_facility = models.ForeignKey(Facility,
                                                         verbose_name=_('Whole Genome'),
                                                         related_name='+',
                                                         blank=True,
                                                         null=True)
    array_analysis_facility = models.ForeignKey(Facility,
                                                verbose_name=_('Array Analysis'),
                                                related_name='+',
                                                blank=True,
                                                null=True)

    sequencer = models.ForeignKey(Sequencer)
    run_number = models.IntegerField(blank=True, null=True)
    flow_cell_id = models.CharField(max_length=10, blank=True, verbose_name=_('Flow Cell ID'))

    class Meta:
        abstract = True


class SequenceFile(models.Model):
    """
    A sequence file resulting from a sequence run
    """

    index_number = models.IntegerField(blank=True, null=True, verbose_name=_('Index'))
    lane_number = models.IntegerField(blank=True, null=True, verbose_name=_('Lane'))
    date_received_from_sequencing_facility = models.DateField(blank=True, null=True)
    filename = models.CharField(max_length=300, blank=True, null=True)
    md5 = models.CharField(_('MD5 Checksum'), max_length=32, blank=True, null=True)
    analysed = models.BooleanField(blank=True)
    note = models.TextField(blank=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        return u'{0}'.format(self.filename)


class URLVerification(models.Model):
    """
    Notes whether a sequence file could be accessed via HTTP. As SequenceFile is abstract
    we can't use a straight DB relationship, so instead we use the calculated URL as the key
    for the join.
    The cron script will clean old entries up.
    """

    checked_url = models.URLField()
    checked_at = models.DateTimeField(auto_now=True, auto_now_add=True)
    status_ok = models.BooleanField()
    status_note = models.TextField()


class DebugNote(models.Model):
    """
    A text field to use for debugging. Stores the original parsed data.
    """

    debug_note = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True
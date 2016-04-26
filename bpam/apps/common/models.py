import urlparse
import urllib

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


class BPAProject(models.Model):
    """
    The BPA project
    Examples would be: Melanoma, Coral
    """

    key = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=200)
    description = models.CharField(_('Description'), max_length=2000, blank=True, help_text='BPA Project description')
    note = models.TextField(blank=True)

    class Meta:
        verbose_name = _('BPA Project')
        verbose_name_plural = _('BPA Projects')

    def __unicode__(self):
        return self.name


class BPAUniqueID(models.Model):
    """
    BPA Generated Label
    Each sample should be issued a Unique ID by BPA
    """

    bpa_id = models.CharField(_('BPA ID'), max_length=200, blank=False, primary_key=True, unique=True, help_text='Unique BPA ID')
    sra_id = models.CharField(_('SRA ID'), max_length=12, blank=True, null=True, unique=True, help_text='SRA ID')
    project = models.ForeignKey(BPAProject)
    note = models.TextField(blank=True)

    class Meta:
        verbose_name = _('BPA Unique ID')
        verbose_name_plural = _("BPA Unique ID's")

    def __unicode__(self):
        return self.bpa_id

    def get_short_name(self):
        """
        Strips the common BPA prefix
        """
        return str(self.bpa_id).split('.')[-1]


class FacilityManager(models.Manager):
    """
    Facility model manager
    """

    def add(self, name):
        """
        I the name is empty return the Unknown Facility
        """
        name = name.strip().upper()
        if name == '':
            name = 'Unknown'
        facility, _ = self.get_or_create(name=name)
        return facility


class Facility(models.Model):
    """
    The Sequencing Facility
    """

    facilities = {'RAM': 'Ramaciotti',
                  'UNSW': 'UNSW',
                  'AGRF': 'AGRF',
                  'ANU': 'ANU',
                  '': 'Unknown',
                  'Unknown': 'Unknown'}

    name = models.CharField(_('Facility Name'), max_length=100, help_text='Facility short name', unique=True)
    note = models.TextField(blank=True)
    objects = FacilityManager()

    class Meta:
        verbose_name_plural = _('Facilities')

    def get_name(self, key):
        """
        Facilities are commonly known by theses names, return standard name.
        """
        try:
            return self.facilities[key]
        except KeyError:
            return 'Unknown'

    def __unicode__(self):
        return u'{0}'.format(self.name)


class Organism(models.Model):
    """
    An Organism
    """

    domain = models.CharField(_('Domain'), max_length=100, blank=True)
    kingdom = models.CharField(max_length=100, blank=True)
    phylum = models.CharField(max_length=100, blank=True)
    organism_class = models.CharField(_('Class'), max_length=100, blank=True)
    order = models.CharField(max_length=100, blank=True)
    family = models.CharField(max_length=100, blank=True)
    genus = models.CharField(max_length=100, blank=True)
    species = models.CharField(max_length=100, blank=True)

    ncbi_classification = models.URLField('NCBI Organismal Classification', blank=True)
    note = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = _('Organisms')

    @property
    def name(self):
        return u'{0} {1}'.format(self.genus, self.species)

    def __unicode__(self):
        return self.name


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

    name = models.CharField(max_length=100, primary_key=True, help_text='The sequencer name')
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = _('Sequencer')

    def __unicode__(self):
        return self.name


class Protocol(models.Model):
    """
    Protocol
    """

    LIB_TYPES = (('PE', 'Paired End'), ('SE', 'Single End'), ('MP', 'Mate Pair'), ('UN', 'Unknown'))
    library_type = models.CharField(_('Type'), max_length=2, choices=LIB_TYPES)
    library_construction = models.CharField(_('Construction'), max_length=200, blank=True, null=True)
    base_pairs = models.IntegerField(_('Base Pairs'), blank=True, null=True)
    library_construction_protocol = models.TextField(_('Construction Protocol'))
    note = models.TextField(blank=True)

    class Meta:
        abstract = True
        verbose_name = _('Protocol')
        verbose_name_plural = _('Protocol')
        unique_together = ('library_type', 'base_pairs', 'library_construction_protocol')

    def __unicode__(self):
        return u'Size:{0}, Type:{1}, Protocol:{2}'.format(self.base_pairs, self.library_type,
                                                          self.library_construction_protocol)

    def set_base_pairs(self, val):
        if val.find("bp") > -1:
            self.base_pairs = int(val[:-2])
        elif val.find("kb") > -1:
            self.base_pairs = int(val[:-2]) * 1000


class Sample(models.Model):
    """
    The common base Sample
    """

    bpa_id = models.OneToOneField(BPAUniqueID, primary_key=True, verbose_name=_('BPA ID'))  # PK
    contact_scientist = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name="%(app_label)s_%(class)s_sample")
    dna_source = models.ForeignKey(DNASource, blank=True, null=True, verbose_name=_('DNA Source'), related_name="%(app_label)s_%(class)s_sample")

    name = models.CharField(_('Sample Name'), max_length=200)
    dna_extraction_protocol = models.TextField(_('DNA Extraction Protocol'), blank=True, null=True)
    requested_sequence_coverage = models.CharField(max_length=50, blank=True)
    collection_date = models.DateField(_('Collection Date'), blank=True, null=True)
    date_sent_to_sequencing_facility = models.DateField(_('Date sent to sequencing facility'), blank=True, null=True)

    note = models.TextField(_('Note'), blank=True, null=True)

    class Meta:
        abstract = True
        verbose_name = _('Sample')

    def __unicode__(self):
        return u'{0}:{1}'.format(self.bpa_id, self.name)


class Run(models.Model):
    """
    A Single Run.
    This run is abstract and needs to be extended in the client application with the specific sample, at least.
    """

    DNA_extraction_protocol = models.CharField(_('DNA Extraction Protocol'), max_length=200, blank=True)
    passage_number = models.IntegerField(_('Passage Number'), blank=True, null=True)

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

    sequencer = models.ForeignKey(Sequencer, blank=True, null=True)
    run_number = models.IntegerField(blank=True, null=True)
    flow_cell_id = models.CharField(_('Flow Cell ID'), max_length=10, blank=True)

    class Meta:
        abstract = True
        verbose_name = _('Run')


class URLVerification(models.Model):
    """
    Notes whether a sequence file could be accessed via HTTP. As SequenceFile is abstract
    we can't use a straight DB relationship, so instead we use the calculated URL as the key
    for the join.
    The cron script will clean old entries up.
    """

    checked_url = models.URLField()
    checked_at = models.DateTimeField()
    status_ok = models.NullBooleanField(null=True, default=False)
    status_note = models.TextField()


class SequenceFile(models.Model):
    """
    A sequence file resulting from a sequence run
    """

    run = None
    project_name = 'UNSET'  # derivative sequence files need to set this

    index_number = models.IntegerField(_('Index'), blank=True, null=True, )
    lane_number = models.IntegerField(_('Lane'), blank=True, null=True)
    read_number = models.IntegerField(_('Read'), blank=True, null=True)

    date_received_from_sequencing_facility = models.DateField(blank=True, null=True)
    filename = models.CharField(_('File Name'), max_length=300, blank=True, null=True)
    md5 = models.CharField(_('MD5 Checksum'), max_length=32, blank=True, null=True)
    analysed = models.NullBooleanField(default=False)
    note = models.TextField(blank=True)

    url_verification = models.ForeignKey(URLVerification, null=True, related_name="%(app_label)s_%(class)s_related")

    class Meta:
        abstract = True
        verbose_name = _('Sequence File')

    def __unicode__(self):
        return u'{0}'.format(self.filename)

    def link_ok(self):
        if self.url_verification is not None:
            return self.url_verification.status_ok
        else:
            return False

    def get_url(self, source_path="all"):
        uj = urlparse.urljoin
        uq = urllib.quote

        return uj(settings.BPA_BASE_URL, "%s/%s/%s" % (
            self.project_name,
            source_path,
            uq(self.filename)))

    url = property(get_url)


class DebugNote(models.Model):
    """
    A text field to use for debugging. Stores the original parsed data.
    """

    debug_note = models.TextField(_('Original Data'), blank=True, null=True)

    class Meta:
        abstract = True

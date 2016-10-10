# -*- coding: utf-8 -*-

import urlparse
import urllib
import re
from django.conf import settings
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point


class FacilityManager(models.Manager):
    """ Facility model manager """

    def add(self, name):
        """ If the name is empty return the Unknown Facility """
        name = name.strip().upper()
        if name == '':
            name = 'Unknown'
        facility, _ = self.get_or_create(name=name)
        return facility


class Facility(models.Model):
    """ The Sequencing Facility """

    # FIXME
    facilities = {'RAM': 'Ramaciotti',
                  'UNSW': 'UNSW',
                  'AGRF': 'AGRF',
                  'ANU': 'ANU',
                  '': 'Unknown',
                  'Unknown': 'Unknown'}

    name = models.CharField('Facility Name', max_length=100, help_text='Facility short name', unique=True)
    note = models.TextField(blank=True)
    objects = FacilityManager()

    class Meta:
        verbose_name_plural = 'Facilities'

    # FIXME
    def get_name(self, key):
        """ Facilities are commonly known by theses names, return standard name. """
        try:
            return self.facilities[key]
        except KeyError:
            return 'Unknown'

    def __unicode__(self):
        return u'{0}'.format(self.name)


class SampleSite(models.Model):
    """ A sample site """

    # Site name
    name = models.TextField("Location Description", blank=False)
    # position
    point = models.PointField("Position", help_text="Represented as (longitude, latitude)")
    # Notes
    note = models.TextField("Note", null=True, blank=True)

    @classmethod
    def _get_point(cls, lon, lat):
        leading_nums_re = re.compile(r'^\s*(-?[\d.]+)')

        def leading_nums(s):
            m = leading_nums_re.match(s)
            if m:
                return m.groups()[0]
            return s
        lat = float(leading_nums(lat))
        lon = float(leading_nums(lon))
        point = Point((lat, lon), srid=settings.GIS_SOURCE_RID)
        point.transform(settings.GIS_TARGET_RID)
        return point

    @classmethod
    def create(cls, lat, lon, site_name):
        site = cls(name=site_name, point=cls._get_point(lat, lon))
        return site

    @classmethod
    def get_or_create(cls, lat, lon, site_name):
        site, _ = cls.objects.get_or_create(name=site_name, point=cls._get_point(lat, lon))
        return site

    def point_description(self):
        return '{:.4f} {:.4f}'.format(self.point.x, self.point.y)

    @property
    def lat(self):
        return self.point.y

    @property
    def lon(self):
        return self.point.x

    def get_name(self):
        if self.name:
            return u"{} ({:4.4f}, {:4.4f})".format(self.name, self.lat, self.lon)
        return u"{:4.4f}, {:4.4f}".format(self.lat, self.lon)

    def __str__(self):
        return '{} ({:.4f} {:.4f})'.format(self.name, self.point.x, self.point.y)

    class Meta:
        abstract = True
        unique_together = ('name', 'point')
        verbose_name = "Sample Collection Site"
        verbose_name_plural = "Sample Collection Sites"


class DataSet(models.Model):
    """ Model representing a dataset """

    name = models.CharField('Dataset', max_length=20, primary_key=True)
    transfer_to_archive_date = models.DateField("Transfer to Archive Date")
    facility = models.ForeignKey(Facility,
                                 related_name='%(app_label)s_%(class)s_facility',
                                 verbose_name='Sequencing Facility',
                                 blank=True,
                                 null=True)

    ticket_url = models.URLField('JIRA')
    downloads_url = models.URLField('Downloads')
    note = models.TextField("Note", blank=True)

    class Meta:
        abstract = True
        verbose_name_plural = 'Datasets'

    def __str__(self):
        return '{}'.format(self.name)


class TransferLog(models.Model):
    """ Notes transfer to CCG """

    facility = models.ForeignKey(Facility,
                                 related_name='%(app_label)s_%(class)s_facility',
                                 verbose_name='Sequencing Facility',
                                 blank=True,
                                 null=True)
    transfer_to_facility_date = models.DateField("Transfer to Facility Date")
    description = models.CharField("Description", max_length=100)
    data_type = models.CharField("Data Type", max_length=50)
    folder_name = models.CharField("Folder", max_length=100)
    transfer_to_archive_date = models.DateField("Transfer to Archive Date")
    notes = models.TextField('Notes', blank=True, null=True)

    ticket_url = models.URLField('Dataset')
    downloads_url = models.URLField('Downloads')

    class Meta:
        abstract = True
        verbose_name = 'Transfer Log'
        verbose_name_plural = 'Transfers'

    def __str__(self):
        return "{} {}".format(self.facility, self.description)


class BPAMirror(models.Model):
    """ A download site, offering the BPA Archive catalogue via a base prefix """

    name = models.CharField(max_length=30, primary_key=True)
    base_url = models.URLField(max_length=200)
    order = models.IntegerField(unique=True)

    def __repr__(self):
        return self.name

    class Meta:
        ordering = ['order']

    @classmethod
    def primary(cls):
        "Returns the lowest order (primary) mirror"
        mirrors = cls.objects.all()
        if len(mirrors) > 0:
            return mirrors[0]
        else:
            print("Please set the mirrors")
            return None


class CKANServer(models.Model):
    """a CKAN installation that we use to retrieve object data"""

    name = models.CharField(max_length=30, primary_key=True)
    base_url = models.URLField(max_length=200)
    order = models.IntegerField(unique=True)

    def __repr__(self):
        return self.name

    class Meta:
        ordering = ['order']

    @classmethod
    def primary(cls):
        "Returns the lowest order (primary) mirror"
        servers = cls.objects.all()
        if len(servers) > 0:
            return servers[0]
        else:
            print("Please set the CKAN servers")
            return None


class BPAProject(models.Model):
    """
    The BPA project
    Examples would be: Melanoma, Coral
    """

    key = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=200)
    description = models.CharField('Description', max_length=2000, blank=True, help_text='BPA Project description')
    note = models.TextField(blank=True)

    class Meta:
        verbose_name = 'BPA Project'
        verbose_name_plural = 'BPA Projects'

    def __unicode__(self):
        return self.name


class BPAUniqueID(models.Model):
    """
    BPA Generated Label
    Each sample should be issued a Unique ID by BPA
    """

    bpa_id = models.CharField('BPA ID',
                              max_length=200,
                              blank=False,
                              primary_key=True,
                              unique=True,
                              help_text='Unique BPA ID')
    sra_id = models.CharField('SRA ID', max_length=12, blank=True, null=True, unique=True, help_text='SRA ID')
    project = models.ForeignKey(BPAProject, related_name='bpa_ids')
    note = models.TextField(blank=True)

    class Meta:
        verbose_name = 'BPA Unique ID'
        verbose_name_plural = "BPA Unique ID's"

    def __unicode__(self):
        return self.bpa_id

    def get_short_name(self):
        """ Strips the common BPA prefix """
        return str(self.bpa_id).split('.')[-1]


class Organism(models.Model):
    """ An Organism """

    domain = models.CharField('Domain', max_length=100, blank=True)
    kingdom = models.CharField(max_length=100, blank=True)
    phylum = models.CharField(max_length=100, blank=True)
    organism_class = models.CharField('Class', max_length=100, blank=True)
    order = models.CharField(max_length=100, blank=True)
    family = models.CharField(max_length=100, blank=True)
    genus = models.CharField(max_length=100, blank=True)
    species = models.CharField(max_length=100, blank=True)

    ncbi_classification = models.URLField('NCBI Organismal Classification', blank=True)
    note = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Organisms'

    @property
    def name(self):
        return u'{0} {1}'.format(self.genus, self.species)

    def __unicode__(self):
        return self.name


class DNASource(models.Model):
    """ DNA Source """

    description = models.CharField(max_length=100)
    note = models.TextField(blank=True)

    class Meta:
        verbose_name = 'DNA Source'
        verbose_name_plural = 'DNA Sources'

    def __unicode__(self):
        return self.description


class Sequencer(models.Model):
    """ The Sequencer """

    name = models.CharField(max_length=100, primary_key=True, help_text='The sequencer name')
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Sequencer'

    def __unicode__(self):
        return self.name


class Protocol(models.Model):
    """ Protocol """

    LIB_TYPES = (('PE', 'Paired End'), ('SE', 'Single End'), ('MP', 'Mate Pair'), ('UN', 'Unknown'))
    library_type = models.CharField('Type', max_length=2, choices=LIB_TYPES)
    library_construction = models.CharField('Construction', max_length=200, blank=True, null=True)
    base_pairs = models.IntegerField('Base Pairs', blank=True, null=True)
    library_construction_protocol = models.TextField('Construction Protocol')
    note = models.TextField(blank=True)

    class Meta:
        abstract = True
        verbose_name = 'Protocol'
        verbose_name_plural = 'Protocol'
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
    """ The common base Sample """

    bpa_id = models.OneToOneField(BPAUniqueID, primary_key=True, verbose_name='BPA ID')
    contact_scientist = models.ForeignKey(settings.AUTH_USER_MODEL,
                                          blank=True,
                                          null=True,
                                          related_name="%(app_label)s_%(class)s_sample")
    dna_source = models.ForeignKey(DNASource,
                                   blank=True,
                                   null=True,
                                   verbose_name='DNA Source',
                                   related_name="%(app_label)s_%(class)s_sample")

    name = models.CharField('Sample Name', max_length=200)
    dna_extraction_protocol = models.TextField('DNA Extraction Protocol', blank=True, null=True)
    requested_sequence_coverage = models.CharField(max_length=50, blank=True)
    collection_date = models.DateField('Collection Date', blank=True, null=True)
    date_sent_to_sequencing_facility = models.DateField('Date sent to sequencing facility', blank=True, null=True)

    note = models.TextField('Note', blank=True, null=True)

    class Meta:
        abstract = True
        verbose_name = 'Sample'

    def __unicode__(self):
        return u'{0}:{1}'.format(self.bpa_id, self.name)


class Run(models.Model):
    """
    A Single Run.
    This run is abstract and needs to be extended in the client application with the specific sample, at least.
    """

    DNA_extraction_protocol = models.CharField('DNA Extraction Protocol', max_length=200, blank=True)
    passage_number = models.IntegerField('Passage Number', blank=True, null=True)

    # facilities
    sequencing_facility = models.ForeignKey(Facility,
                                            verbose_name='Sequencing',
                                            related_name='+',
                                            blank=True,
                                            null=True)
    whole_genome_sequencing_facility = models.ForeignKey(Facility,
                                                         verbose_name='Whole Genome',
                                                         related_name='+',
                                                         blank=True,
                                                         null=True)
    array_analysis_facility = models.ForeignKey(Facility,
                                                verbose_name='Array Analysis',
                                                related_name='+',
                                                blank=True,
                                                null=True)

    sequencer = models.ForeignKey(Sequencer, blank=True, null=True)
    run_number = models.IntegerField(blank=True, null=True)
    flow_cell_id = models.CharField('Flow Cell ID', max_length=10, blank=True)

    class Meta:
        abstract = True
        verbose_name = 'Run'


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
    """ A sequence file resulting from a sequence run """

    run = None
    project_name = 'UNSET'  # derivative sequence files need to set this

    index_number = models.IntegerField('Index Number', blank=True, null=True)
    lane_number = models.IntegerField('Lane Number', blank=True, null=True)
    read_number = models.IntegerField('Read Number', blank=True, null=True)

    date_received_from_sequencing_facility = models.DateField(blank=True, null=True)
    filename = models.CharField('File Name', max_length=300, blank=True, null=True)
    md5 = models.CharField('MD5 Checksum', max_length=32, blank=True, null=True)
    analysed = models.NullBooleanField(default=False)
    note = models.TextField(blank=True)

    url_verification = models.ForeignKey(URLVerification, null=True, related_name="%(app_label)s_%(class)s_related")

    class Meta:
        abstract = True
        verbose_name = 'Sequence File'

    def __unicode__(self):
        return u'{0}'.format(self.filename)

    def link_ok(self):
        if self.url_verification is not None:
            return self.url_verification.status_ok
        else:
            return False

    def get_path_parts(self):
        return (self.project_name, 'all')

    def get_url(self, mirror=None):
        uj = urlparse.urljoin
        uq = urllib.quote

        if mirror is None:
            mirror = BPAMirror.primary()

        return uj(mirror.base_url, "%s/%s" % ('/'.join(uq(t) for t in self.get_path_parts()), uq(self.filename)))

    url = property(get_url)


class DebugNote(models.Model):
    """ A text field to use for debugging. Stores the original parsed data. """

    debug_note = models.TextField('Original Data', blank=True, null=True)

    class Meta:
        abstract = True

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from apps.bpaauth.models import BPAUser


class BPAProject(models.Model):
    """
    The BPA project
    Examples would be: Melanoma, Coral 
    """
    
    name = models.CharField(max_length=20, primary_key=True)
    description = models.CharField(max_length=200, blank=True)
    note = models.TextField(blank=True)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = _('BPA Project')
        verbose_name_plural = _("BPA Projects")
    
class BPAUniqueID(models.Model):
    """
    BPA Generated Label
    Each sample should be issued a Unique ID by BPA
    """
    
    bpa_id = models.CharField("BPA Unique ID", max_length=16, blank=False, primary_key=True, unique=True)
    project = models.ForeignKey(BPAProject)
    note = models.TextField(blank=True)
    
    def __unicode__(self):
        return self.bpa_id
    
    class Meta:
        verbose_name = 'BPA Unique ID'
        verbose_name_plural = "BPA Unique ID's"

    
class Facility(models.Model):
    """
    The Sequencing Facility
    """
    
    name = models.CharField(max_length=100)
    service = models.CharField(max_length=200)
    note = models.TextField(blank=True)

    def __unicode__(self):
        return "{0} {1}".format(self.name, self.service)
    
    class Meta:
        unique_together = ('name', 'service',)
        verbose_name_plural = "Facilities"

        
class Organism(models.Model):
    """
    An Organism
    """    
    
    genus = models.CharField(max_length=100)
    species = models.CharField(max_length=100, primary_key=True)
    classification = models.URLField('NCBI organismal classification', blank=True)   
    note = models.TextField(blank=True) 

    def __unicode__(self):
        return "{0} {1}".format(self.genus, self.species)
    
    class Meta:
        verbose_name_plural = "Organisms"
        unique_together = ('genus', 'species')
        

class DNASource(models.Model):
    """
    DNA Source
    """
    description = models.CharField(max_length=100)    
    note = models.TextField(blank=True) 
    
    def __unicode__(self):
        return self.description

    class Meta:
        verbose_name = "DNA Source"
        verbose_name_plural = "DNA Sources"

class Sequencer(models.Model):
    """
    The Sequencer
    """
    
    name = models.CharField(max_length=100, primary_key=True)
    description = models.TextField(blank=True)
        
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
    
    def __unicode__(self):
        return "Size: " + str(self.base_pairs) + " Type: " + str(self.library_type) + " Protocol: " + str(self.library_construction_protocol)

    class Meta:
        verbose_name_plural = "Protocol"
        unique_together = ('library_type', 'base_pairs', 'library_construction_protocol')


class Sample(models.Model):
    """
    The common base Sample
    """

    bpa_id = models.OneToOneField(BPAUniqueID, unique=True)
    name = models.CharField(max_length=200)   
        
    dna_source = models.ForeignKey(DNASource, verbose_name="DNA Source", blank=True, null=True)
    dna_extraction_protocol = models.CharField(max_length=200, blank=True, null=True)             
    requested_sequence_coverage = models.CharField(max_length=6, blank=True)
    collection_date = models.DateField(blank=True, null=True)
    date_sent_to_sequencing_facility = models.DateField(blank=True, null=True)    
    contact_scientist = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    
    # facilities
    sequencing_facility = models.ForeignKey(Facility, related_name='+', blank=True, null=True)
    array_analysis_facility = models.ForeignKey(Facility, related_name='+', blank=True, null=True)
    whole_genome_sequencing_facility = models.ForeignKey(Facility, related_name='+', blank=True, null=True)
    
    protocol = models.ForeignKey(Protocol, blank=True, null=True)    
    note = models.TextField(blank=True, null=True)
    
    def __unicode__(self):
        return "{0} {1}".format(self.bpa_id, self.name)

    class Meta:        
        abstract = True
    
    
class Run(models.Model):
    """
    A Single Run
    """
     
    protocol = models.ForeignKey(Protocol, blank=True, null=True)   
    DNA_extraction_protocol = models.CharField(max_length=200, blank=True)
    passage_number = models.IntegerField(blank=True, null=True)
     
    # Facilities
    sequencing_faciltiy = models.ForeignKey(Facility, related_name='sequencing_facility', blank=True, null=True)
    array_analysis_faciltiy = models.ForeignKey(Facility, related_name='array_analysis_facility', blank=True, null=True)
    whole_genome_sequencing_faciltiy = models.ForeignKey(Facility, related_name='whole_genome_sequencing_facility', blank=True, null=True)    

    sequencer = models.ForeignKey(Sequencer)
    run_number = models.IntegerField(blank=True, null=True)
    flow_cell_id = models.CharField(max_length=10, blank=True)    
   
    class Meta:
        abstract = True


class SequenceFile(models.Model):
    """
    A sequence file resulting from a sequence run
    """
        
    index_number = models.IntegerField(blank=True, null=True)
    lane_number = models.IntegerField(blank=True, null=True)    
    date_received_from_sequencing_facility = models.DateField(blank=True, null=True)
    filename = models.CharField(max_length=300, blank=True, null=True)
    md5 = models.CharField('MD5 Checksum', max_length=32, blank=True, null=True)
    BPA_archive_url = models.URLField('BPA Archive URL', blank=True, null=True)    
    analysed = models.BooleanField(blank=True)
    analysed_url = models.URLField(blank=True, null=True)    
    ftp_url = models.URLField('FTP URL', blank=True, null=True)
    note = models.TextField(blank=True)

    def __unicode__(self):
        return "{0}".format(self.filename)

    class Meta:
        abstract = True





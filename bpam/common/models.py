from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from bpaauth.models import BPAUser

GENDERS = (('M', 'Male'), ('F', 'Female'), ('U', 'Unknown'),)

class BPAProject(models.Model):
    """
    The BPA project
    Examples would be: Melanoma, Coral 
    """
    
    name = models.CharField(max_length=20, primary_key=True)
    description = models.CharField(max_length=200, blank=True)

    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = 'BPA Project'
        verbose_name_plural = "BPA Projects"
    
class BPAUniqueID(models.Model):
    """
    BPA Generated Label
    Each sample should be issued a Unique ID by BPA
    """
    
    bpa_id = models.CharField("BPA Unique ID", max_length=16, blank=False, primary_key=True)
    project = models.ForeignKey(BPAProject)
    note = models.TextField(blank=True)
    
    def __unicode__(self):
        return self.bpa_id
    
    class Meta:
        verbose_name = 'BPA Unique ID'
        verbose_name_plural = "BPA Unique ID's"


class Service(models.Model):
    ''' A service rendered by a facility'''
    
    description = models.CharField(max_length=300)
       
    def __unicode__(self):
        return self.description
    
    
class Facility(models.Model):
    """
    The Sequencing Facility
    """
    name = models.CharField(max_length=100)
    service = models.ForeignKey(Service)
    note =  models.TextField(blank=True)

    def __unicode__(self):
        return self.name
    
    class Meta:
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
        return "{} {}".format(self.genus, self.species)
    
    class Meta:
        verbose_name_plural = "Organisms"
        unique_together = ('genus', 'species')
        

class DNASource(models.Model):
    """
    DNA Source
    """
    source = models.CharField(max_length=100)

    def __unicode__(self):
        return self.source

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


class LibraryProtocol(models.Model):
    """
    Library Protocol 
    """
    
    description = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.description
    

class Library(models.Model):
    """
    Library
    """
    
    LIB_TYPES = (('PE', 'Paired End'), ('SE', 'Single End'), ('MP', 'Mate Pair'))
    type = models.CharField(max_length=2, choices=LIB_TYPES)
    base_pairs = models.IntegerField()
    protocol = models.ForeignKey(LibraryProtocol)
    
    def __unicode__(self):
        return "Size: " + str(self.base_pairs) + " Type: " + str(self.type) + " Protocol: " + str(self.protocol)

    class Meta:
        verbose_name_plural = "Libraries"


class Sample(models.Model):
    """
    The common base Sample
    """

    bpa_id = models.OneToOneField(BPAUniqueID, unique=True)
    name = models.CharField(max_length=200)    
    
    organism = models.ForeignKey(Organism)
    dna_source = models.ForeignKey(DNASource, verbose_name="DNA Source", blank=True, null=True)
            
    requested_sequence_coverage = models.CharField(max_length=4, blank=True)
   
    contact_scientist = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    date_sent_to_sequencing_facility = models.DateField(blank=True, null=True)
    note = models.TextField(blank=True)
    
    def __unicode__(self):
        return "{} {}".format(self.bpa_id, self.name)

    class Meta:        
        abstract = True
    
    
class Run(models.Model):
    """
    A Single Run
    """
     
    library = models.ForeignKey(Library, blank=True, null=True)   
    DNA_extraction_protocol = models.CharField(max_length=200, blank=True)
    passage_number = models.IntegerField()
     
    # Facilities
    sequencing_faciltiy = models.ForeignKey(Facility, related_name='sequencing_facility', blank=True, null=True)
    array_analysis_faciltiy = models.ForeignKey(Facility, related_name='array_analysis_facility', blank=True, null=True)
    whole_genome_sequencing_faciltiy = models.ForeignKey(Facility, related_name='whole_genome_sequencing_facility', blank=True, null=True)    

    index_number = models.IntegerField()
    sequencer = models.ForeignKey(Sequencer)
    run_number = models.IntegerField()
    flow_cell_id = models.CharField(max_length=10)
    lane_number = models.IntegerField()
   
    class Meta:
        abstract = True


class SequenceFile(models.Model):
    """
    A sequence file resulting from a sequence run
    """
    
    date_received_from_sequencing_facility = models.DateField()
    filename = models.CharField(max_length=300)
    md5 = models.CharField('MD5 Checksum', max_length=32)
    BPA_archive_url = models.URLField('BPA Archive URL')    
    analysed = models.BooleanField()
    analysed_url = models.URLField()    
    ftp_url = models.URLField('FTP URL')

    def __unicode__(self):
        return "{}".format(self.filename)

    class Meta:
        abstract = True



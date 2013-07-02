from django.db import models
from common.models import *

GENDERS = (('M', 'Male'), ('F', 'Female'), ('U', 'Unknown'),)


class DNASource(models.Model):
    """
    DNA Source
    """
    source = models.CharField(max_length=100)


    def __unicode__(self):
        return self.source

    class Meta:
        verbose_name = 'DNA Source'
        verbose_name_plural = "DNA Sources"

class Sequencer(models.Model):
    """
    The Sequencer
    """
    name = models.CharField(max_length=100)
        
    def __unicode__(self):
        return self.name


class TumorStage(models.Model):
    """
    Tumor Stage
    """
    
    name = models.CharField(max_length=100)

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
    
    paired_end = models.BooleanField()
    base_pairs = models.IntegerField()
    protocol = models.ForeignKey(LibraryProtocol)
    
    def __unicode__(self):
        return "Size: " + str(self.base_pairs) + " Paired: " + str(self.paired_end) + " Protocol: " + str(self.protocol)

    class Meta:
        verbose_name_plural = "Libraries"

class Array(models.Model):
    """
    Array
    """
    
    bpa_id = models.ForeignKey(BPA_ID)
    array_id = models.CharField(max_length=17, unique=True)
    batch_number = models.IntegerField()
    well_id = models.CharField(max_length=4)
    MIA_id = models.CharField(max_length=50)
    call_rate = models.FloatField()
    
    gender = models.CharField(max_length=1, choices=GENDERS)


class Sample(models.Model):
    """
    A Melanoma sample
    """

    bpa_id = models.ForeignKey(BPA_ID)
    sample_name = models.CharField(max_length=200)
    requested_sequence_coverage = models.CharField(max_length=4)
    species = models.CharField(max_length=100)
    
    sequencing_faciltiy = models.ForeignKey(Facility, related_name='sequencing_facility')
    array_analysis_faciltiy = models.ForeignKey(Facility, related_name='array_analysis_facility')
    whole_genome_sequencing_faciltiy = models.ForeignKey(Facility, related_name='whole_genome_sequencing_facility')    
    
    date_sent_to_sequencing_facility = models.DateField()
    date_recieved_from_sequencing_facility = models.DateField()
    
    dna_source = models.ForeignKey(DNASource)
    
    library = models.ForeignKey(Library)
    
    index_number = models.IntegerField()
    sequencer = models.ForeignKey(Sequencer)
    run_number = models.IntegerField()
    flow_cell_id = models.CharField(max_length=10)
    lane_number = models.IntegerField()

    sex = models.CharField(choices=GENDERS, max_length=1)
    
    tumor_stage = models.ForeignKey(TumorStage)
    histological_subtype = models.CharField(max_length=50)
    passage_number = models.IntegerField()
    DNA_extraction_protocol = models.CharField(max_length=200)
    
    contact = models.ForeignKey(Contact)
    
    sequence_facility_filename = models.CharField(max_length=300)
    md5cheksum = models.CharField(max_length=32)
    BPA_archive_url = models.URLField()    
    analysed = models.BooleanField()
    analysed_url = models.URLField()    
    ftp_url = models.URLField()
    
    note = models.TextField()
    
    


    def __unicode__(self):
        return self.bpa_sample_id + " " + self.sample_name






from django.db import models


class Affiliation(models.Model):
    """
    Affiliation
    """
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class DNASource(models.Model):
    """
    DNA Source
    """
    source = models.CharField(max_length=100)


    def __unicode__(self):
        return self.source


class Facility(models.Model):
    """
    The Sequencing SequencingFacility
    """
    name = models.CharField(max_length=100)
    service = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


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


class Contact(models.Model):
    """
    Contact Detail
    """
    name = models.CharField(max_length=200)
    affiliation = models.ForeignKey(Affiliation)
    email = models.CharField(max_length=200)


    def __unicode__(self):
        return self.name




class Sample(models.Model):
    """
    A sample
    """

    BPA_sample_id = models.CharField(max_length=16)
    sample_name = models.CharField(max_length=200)
    requested_sequence_coverage = models.CharField(max_length=4)
    species = models.CharField(max_length=100)
    
    sequencing_faciltiy = models.ForeignKey(Facility, related_name='sequencing_facility')
    array_analysis_faciltiy = models.ForeignKey(Facility, related_name='array_analysis_facility')
    whole_genome_sequencing_faciltiy = models.ForeignKey(Facility, related_name='whole_genome_sequencing_facility')    
    
    date_sent_to_sequencing_facility = models.DateField()
    date_recieved_from_sequencing_facility = models.DateField()
    
    dna_source = models.ForeignKey(DNASource)
    
    # Library
    # FIXME, factor out ? 
    library = models.CharField(max_length=20)
    library_construction = models.CharField(max_length=20)
    library_construction_protocol = models.CharField(max_length=100)
    
    index_number = models.IntegerField()
    sequencer = models.ForeignKey(Sequencer)
    run_number = models.IntegerField()
    flow_cell_id = models.CharField(max_length=10)
    lane_number = models.IntegerField()

    sex = models.CharField(max_length=1)
    tumor_stage = models.ForeignKey(TumorStage)
    histological_subtype = models.CharField(max_length=50)
    passage_number = models.IntegerField()
    DNA_extraction_protocol = models.CharField(max_length=200)
    
    contact = models.ForeignKey(Contact)
    
    sequence_facility_filename = models.CharField(max_length=300)
    md5cheksum =  models.CharField(max_length=32)
    BPA_archive_url = models.URLField()    
    analysed = models.BooleanField()
    analysed_url = models.URLField()    
    ftp_url = models.URLField()
    
    


    def __unicode__(self):
        return self.bpa_sample_id + " " + self.sample_name





from django.db import models

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
    
class BPASampleID(models.Model):
    """
    BPA Generated Sample ID
    Each sample should be issued a Unique ID by BPA
    """
    
    id = models.CharField(max_length=16, blank=False, primary_key=True)
    project = models.ForeignKey(BPAProject)
    note = models.TextField(blank=True)

    def __unicode__(self):
        return self.id
    
    class Meta:
        verbose_name = 'BPA Identification'
        verbose_name_plural = "BPA IDs"


class Affiliation(models.Model):
    """
    Affiliation
    """
    name = models.CharField(max_length=20, primary_key=True)
    description = models.CharField(max_length=200, blank=True)

    def __unicode__(self):
        return self.name

class Contact(models.Model):
    """
    Contact Detail
    """
    name = models.CharField(max_length=200)
    affiliation = models.ForeignKey(Affiliation)
    email = models.EmailField(blank=True)


    def __unicode__(self):
        return self.name
    
    
class Facility(models.Model):
    """
    The Sequencing Facility
    """
    name = models.CharField(max_length=100)
    service = models.CharField(max_length=100, blank=True)

    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Facilities"
        
        
class Organism(models.Model):
    """
    An Organism
    """    
    genus = models.CharField(max_length=100)
    species = models.CharField(max_length=100)

    def __unicode__(self):
        return "{}.{}".format(self.genus, self.species)
    
    class Meta:
        verbose_name_plural = "Organisms"
        

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

class Array(models.Model):
    """
    Array
    """
    
    bpa_id = models.ForeignKey(BPASampleID)
    array_id = models.CharField(max_length=17, unique=True)
    batch_number = models.IntegerField()
    well_id = models.CharField(max_length=4)
    MIA_id = models.CharField(max_length=50)
    call_rate = models.FloatField()
    
    gender = models.CharField(max_length=1, choices=GENDERS)


class Sample(models.Model):
    """
    The common base Sample
    """

    # ID
    bpa_id = models.ForeignKey(BPASampleID)
    bpa_project = models.ForeignKey(BPAProject)
    sample_name = models.CharField(max_length=200)    
    
    organism = models.ForeignKey(Organism)
    dna_source = models.ForeignKey(DNASource, verbose_name="DNA Source")
            
    requested_sequence_coverage = models.CharField(max_length=4)
   
    contact = models.ForeignKey(Contact)
    date_sent_to_sequencing_facility = models.DateField()
    note = models.TextField(blank=True)
    
class Run(models.Model):
    """
    A Single Run
    """
    
    sample = models.ForeignKey(Sample)
    date_recieved_from_sequencing_facility = models.DateField()
     
    library = models.ForeignKey(Library)   
    DNA_extraction_protocol = models.CharField(max_length=200)
    passage_number = models.IntegerField()
     
    # Facilities
    sequencing_faciltiy = models.ForeignKey(Facility, related_name='sequencing_facility')
    array_analysis_faciltiy = models.ForeignKey(Facility, related_name='array_analysis_facility')
    whole_genome_sequencing_faciltiy = models.ForeignKey(Facility, related_name='whole_genome_sequencing_facility')    

    index_number = models.IntegerField()
    sequencer = models.ForeignKey(Sequencer)
    run_number = models.IntegerField()
    flow_cell_id = models.CharField(max_length=10)
    lane_number = models.IntegerField()

    def __unicode__(self):
        return "Run {} for {}".format(self.run_number, self.sample.sample_name)


class SequenceFile(models.Model):
    """
    A sequence file resulting from a sequence run
    """
    
    run =  models.ForeignKey(Run)
    date_received_from_sequencing_facility = models.DateField()
    filename = models.CharField(max_length=300)
    md5cheksum = models.CharField('MD5 Checksum', max_length=32)
    BPA_archive_url = models.URLField('BPA Archive URL')    
    analysed = models.BooleanField()
    analysed_url = models.URLField()    
    ftp_url = models.URLField()

    def __unicode__(self):
        return "{}".format(self.filename)





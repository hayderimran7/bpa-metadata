from django.db import models


class BPASampleID(models.Model):
    """
    BPA Generated Sample ID
    Each sample should be issued a Unique ID by BPA
    """
    
    bpa_sample_id = models.CharField(max_length=16, unique=True)
    note =  models.TextField()

    def __unicode__(self):
        return self.bpa_sample_id
    
    class Meta:
        verbose_name = 'BPA Identification'
        verbose_name_plural = "BPA IDs"

class Affiliation(models.Model):
    """
    Affiliation
    """
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

class Contact(models.Model):
    """
    Contact Detail
    """
    name = models.CharField(max_length=200)
    affiliation = models.ForeignKey(Affiliation)
    email = models.EmailField()


    def __unicode__(self):
        return self.name
    
    
class Facility(models.Model):
    """
    The Sequencing Facility
    """
    name = models.CharField(max_length=100)
    service = models.CharField(max_length=100)

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
        
    

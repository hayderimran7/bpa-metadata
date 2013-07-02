from django.db import models


class BPA_ID(models.Model):
    """
    BPA Generated ID 
    """
    
    bpa_id = models.CharField(max_length=16, unique=True)

    def __unicode__(self):
        return self.bpa_id
    
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
        
        
class Species(models.Model):
    """
    A Species
    """
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Species"
        
    

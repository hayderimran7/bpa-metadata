from django.db import models
from django.conf import settings
from apps.bpaauth.models import BPAUser
from apps.common.models import Sample, Run, BPAUniqueID, SequenceFile, Organism
import urlparse, urllib

GENDERS=(('M', 'Male'),
         ('F', 'Female'),
         ('U', 'Unknown'))

class TumorStage(models.Model):
    """ Tumor Stage """
    
    description = models.CharField(max_length=100)
    note = models.TextField(blank=True) 

    def __unicode__(self):
        return self.description
    
    
class Array(models.Model):
    """ Array """
    
    bpa_id = models.ForeignKey(BPAUniqueID)
    array_id = models.CharField(max_length=17)
    batch_number = models.IntegerField()
    well_id = models.CharField(max_length=4)
    mia_id = models.CharField(max_length=200)
    call_rate = models.FloatField()    
    gender = models.CharField(max_length=1, choices=GENDERS)
    
    def __unicode__(self):
        return "{0} {1} {2}".format(self.bpa_id, self.array_id, self.mia_id)
    
class MelanomaSample(Sample):
    """ Melanoma specific Sample """
    
    organism = models.ForeignKey(Organism)
    # don't currently understand what this is. 
    passage_number = models.IntegerField(null=True)
    
    gender = models.CharField(choices=GENDERS, max_length=1, null=True)    
    tumor_stage = models.ForeignKey(TumorStage, null=True)
    histological_subtype = models.CharField(max_length=50, null=True)


class MelanomaRun(Run):
    """ A Melanoma Run """
    
    sample = models.ForeignKey(MelanomaSample)
    
    def __unicode__(self):
        return "Run {0} for {1}".format(self.run_number, self.sample.name)
    
    
class MelanomaSequenceFile(SequenceFile):
    """ Sequence Files resulting from a run """
    
    sample = models.ForeignKey(MelanomaSample)
    run = models.ForeignKey(MelanomaRun)

    def __unicode__(self):
        return "Run {0} for {1}".format(self.run, self.filename)

    def get_url(self):
        bpa_id = self.sample.bpa_id.bpa_id.replace('/', '.')
        uj = urlparse.urljoin
        uq = urllib.quote
        return uj(uj(uj(settings.BPA_BASE_URL, 'melanoma/'), uq(bpa_id) + '/'), uq(self.filename.strip()))
        
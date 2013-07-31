from django.db import models
from bpaauth.models import BPAUser
from common.models import Sample, Run, BPAUniqueID, SequenceFile, GENDERS

class TumorStage(models.Model):
    '''Tumor Stage'''
    
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name
    
    
class Array(models.Model):
    '''Array'''
    
    bpa_id = models.ForeignKey(BPAUniqueID)
    array_id = models.CharField(max_length=17)
    batch_number = models.IntegerField()
    well_id = models.CharField(max_length=4)
    mia_id = models.CharField(max_length=50)
    call_rate = models.FloatField()    
    gender = models.CharField(max_length=1, choices=GENDERS)
    
    def __unicode__(self):
        return "{} {} {}".format(self.bpa_id, self.array_id, self.mia_id)
    
class MelanomaSample(Sample):
    '''Melanoma specific Sample'''
    
    sex = models.CharField(choices=GENDERS, max_length=1, null=True)    
    tumor_stage = models.ForeignKey(TumorStage, null=True)
    histological_subtype = models.CharField(max_length=50, null=True)


class MelanomaRun(Run):
    '''A Melanoma Run '''
    
    sample = models.ForeignKey(MelanomaSample)
    
    def __unicode__(self):
        return "Run {} for {}".format(self.run_number, self.sample.name)
    
    
class MelanomaSequenceFile(SequenceFile):
    '''Resulting Sequence Files resulting from a run'''
    
    run = models.ForeignKey(MelanomaRun)

    

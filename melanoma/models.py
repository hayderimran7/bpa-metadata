from django.db import models
import common.models 
from common.models import GENDERS


class TumorStage(models.Model):
    """
    Tumor Stage
    """
    
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name
    
    
class Sample(common.models.Sample):
    """
    Melanoma specific Sample
    """
    
    sex = models.CharField(choices=GENDERS, max_length=1)    
    tumor_stage = models.ForeignKey(TumorStage)
    histological_subtype = models.CharField(max_length=50)

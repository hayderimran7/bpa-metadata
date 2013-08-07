from django.db import models
from common.models import Sample

class SoilSample(Sample):
    """ Soil Sample """
    
    plot_description = models.TextField(blank=True)
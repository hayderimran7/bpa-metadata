from django.db import models
from apps.common.models import Sample

class SoilSample(Sample):
    """ Soil Sample """
    
    plot_description = models.TextField(blank=True)
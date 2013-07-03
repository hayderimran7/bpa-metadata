from django.db import models

import common.models 


class Collection(models.Model):
    """
    Data surrounding a Coral collection
    """
    
    type = models.CharField(max_length=100)
    site = models.CharField(max_length=100)
    date = models.DateField()
    gps_location = models.CharField(max_length=100) # FIXME, nice geo types
    water_temperature = models.IntegerField()
    water_ph = models.IntegerField()
    depth = models.IntegerField()
    note = models.TextField(blank=True)

    def __unicode__(self):
        return "{} {} {}".format(self.type, self.site, self.date)
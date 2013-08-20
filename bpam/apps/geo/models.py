from django.db import models
from django.contrib.gis.db import models
 
class GPSPosition(models.Model):
    """ A GPS Position """  
    
    description = models.CharField(max_length=100) 
    longitude = models.FloatField() 
    latitude = models.FloatField()
    elevation = models.FloatField()

    # in_geom = models.PointField('shp', srid=4326)
    objects = models.GeoManager() 
    
    def __unicode__(self): 
        return "{0} {1} {2} {3}".format(self.description, self.elevation, self.longitude, self.latitude)
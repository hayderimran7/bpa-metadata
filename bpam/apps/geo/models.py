from django.db import models
from django.contrib.gis.db import models
 
class GPSPosition(models.Model):
    """ A GPS Position """  
    
    description = models.CharField(max_length=100, help_text='Press "Tab" to refresh the map') 
    longitude = models.FloatField(help_text='WGS84 Decimal Degree. Press "Tab" to refresh the map') 
    latitude = models.FloatField(help_text='WGS84 Decimal Degree. Press "Tab" to refresh the map')
    altitude = models.FloatField(help_text='Altitude, meters above sea level.')
    in_geom = models.PointField('shp', srid=4326)
     
    objects = models.GeoManager() 
    
    def __unicode__(self): 
        return "{0} {1} {2} {3}".format(self.description, self.altitude, self.longitude, self.latitude)
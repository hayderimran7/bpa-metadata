from django.contrib import admin
from .models import GPSPosition
                     
class GPSPositionAdmin(admin.ModelAdmin):
    list_display = ('description', 'altitude', 'longitude', 'latitude')

admin.site.register(GPSPosition, GPSPositionAdmin)


    
    


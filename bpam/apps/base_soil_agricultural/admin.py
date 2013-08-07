from django.contrib import admin
from .models import SoilSample

class SampleAdmin(admin.ModelAdmin):
    list_display = ('bpa_id', 'name', 'note')

admin.site.register(SoilSample, SampleAdmin)

    
    


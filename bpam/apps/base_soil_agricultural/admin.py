from django.contrib import admin
from .models import (SoilSample, 
                     LandUse, 
                     SiteOwner,
                     CollectionSiteHistory, 
                     CollectionSite,
                     SequenceConstruct,
                     ChemicalAnalysis,)
                     
                     
                     
class SampleAdmin(admin.ModelAdmin):
    list_display = ('bpa_id', 'name')

admin.site.register(SoilSample, SampleAdmin)
admin.site.register(LandUse)
admin.site.register(SiteOwner)
admin.site.register(CollectionSiteHistory)
admin.site.register(CollectionSite)
admin.site.register(SequenceConstruct)
admin.site.register(ChemicalAnalysis)



    
    


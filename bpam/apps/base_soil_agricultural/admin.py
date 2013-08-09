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

class ChemicalAnalysisAdmin(admin.ModelAdmin):
    list_display = ('bpa_id', 'lab_name_id', 'depth', 'colour', 'texture')

admin.site.register(SoilSample, SampleAdmin)
admin.site.register(LandUse)
admin.site.register(SiteOwner)
admin.site.register(CollectionSiteHistory)
admin.site.register(CollectionSite)
admin.site.register(SequenceConstruct)
admin.site.register(ChemicalAnalysis, ChemicalAnalysisAdmin)



    
    


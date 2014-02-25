from django.contrib import admin

from models import *


class CollectionSiteAdmin(admin.ModelAdmin):
    list_display = ('location_name', 'lat', 'lon')


admin.site.register(CollectionSite, CollectionSiteAdmin)





class ChemicalAnalysisAdmin(admin.ModelAdmin):
    list_display = ('bpa_id', 'lab_name_id', 'depth', 'colour', 'gravel', 'texture')
admin.site.register(ChemicalAnalysis, ChemicalAnalysisAdmin)

admin.site.register(SiteOwner)
admin.site.register(CollectionSiteHistory)




    
    


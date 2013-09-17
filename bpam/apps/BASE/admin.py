from django.contrib import admin
from .models import *

class LandUseAdmin(admin.ModelAdmin):
    list_display = ('description', 'classification')


class SampleAdmin(admin.ModelAdmin):
    list_display = ('bpa_id', 'name')


class ChemicalAnalysisAdmin(admin.ModelAdmin):
    list_display = ('bpa_id', 'lab_name_id', 'depth', 'colour', 'texture')


class CollectionSiteAdmin(admin.ModelAdmin):
    list_display = ('country', 'state', 'location_name')


class SoilClassificationAdmin(admin.ModelAdmin):
    list_display = ('authority', 'classification')

admin.site.register(SoilClassification, SoilClassificationAdmin)
admin.site.register(TillageType)
admin.site.register(BroadVegetationType)
admin.site.register(GeneralEcologicalZone)
admin.site.register(SoilSample, SampleAdmin)
admin.site.register(LandUse, LandUseAdmin)
admin.site.register(SiteOwner)
admin.site.register(CollectionSiteHistory)
admin.site.register(CollectionSite)
admin.site.register(SequenceConstruct)
admin.site.register(ChemicalAnalysis, ChemicalAnalysisAdmin)
admin.site.register(PCRPrimer)
admin.site.register(TargetGene)
admin.site.register(TargetTaxon)


    
    


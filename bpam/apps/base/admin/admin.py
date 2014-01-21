from django.contrib import admin

from ..models.site import *
from ..models.contextual import *


class LandUseAdmin(admin.ModelAdmin):
    list_display = ('description', 'classification')


admin.site.register(LandUse, LandUseAdmin)


class ChemicalAnalysisAdmin(admin.ModelAdmin):
    list_display = ('bpa_id', 'lab_name_id', 'depth', 'colour', 'gravel', 'texture')


admin.site.register(ChemicalAnalysis, ChemicalAnalysisAdmin)


class CollectionSiteAdmin(admin.ModelAdmin):
    list_display = ('country', 'state', 'location_name')


class SoilClassificationAdmin(admin.ModelAdmin):
    list_display = ('authority', 'classification')


admin.site.register(SoilClassification, SoilClassificationAdmin)


class SoilTextureAdmin(admin.ModelAdmin):
    list_display = ('texture', 'description')


admin.site.register(SoilTexture, SoilTextureAdmin)


class DrainageAdmin(admin.ModelAdmin):
    list_display = ('drainage', 'description')


admin.site.register(DrainageClassification, DrainageAdmin)


class ColourAdmin(admin.ModelAdmin):
    list_display = ('colour', 'code')


admin.site.register(SoilColour, ColourAdmin)

admin.site.register(HorizonClassification)
admin.site.register(ProfilePosition)
admin.site.register(TillageType)
admin.site.register(BroadVegetationType)
admin.site.register(GeneralEcologicalZone)
admin.site.register(SiteOwner)
admin.site.register(CollectionSiteHistory)
admin.site.register(CollectionSite)
admin.site.register(SequenceConstruct)
admin.site.register(PCRPrimer)
admin.site.register(TargetGene)
admin.site.register(TargetTaxon)


    
    


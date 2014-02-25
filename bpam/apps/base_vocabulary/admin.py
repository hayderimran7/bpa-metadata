from django.contrib import admin

from models import (SoilClassification, DrainageClassification, SoilTexture, SoilColour, HorizonClassification,
                    ProfilePosition, TillageType, BroadVegetationType, GeneralEcologicalZone, LandUse)


class SoilClassificationAdmin(admin.ModelAdmin):
    list_display = ('authority', 'classification')


admin.site.register(SoilClassification, SoilClassificationAdmin)


class DrainageAdmin(admin.ModelAdmin):
    list_display = ('drainage', 'description')


admin.site.register(DrainageClassification, DrainageAdmin)


class SoilTextureAdmin(admin.ModelAdmin):
    list_display = ('texture', 'description')


admin.site.register(SoilTexture, SoilTextureAdmin)


class ColourAdmin(admin.ModelAdmin):
    list_display = ('colour', 'code')


admin.site.register(SoilColour, ColourAdmin)


class LandUseAdmin(admin.ModelAdmin):
    list_display = ('description', 'classification')


admin.site.register(LandUse, LandUseAdmin)

admin.site.register(HorizonClassification)
admin.site.register(ProfilePosition)
admin.site.register(TillageType)
admin.site.register(BroadVegetationType)
admin.site.register(GeneralEcologicalZone)
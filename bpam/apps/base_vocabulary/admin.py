from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from suit.admin import SortableModelAdmin

from models import (AustralianSoilClassification, FAOSoilClassification, DrainageClassification, SoilTexture, SoilColour, HorizonClassification,
                    ProfilePosition, TillageType, BroadVegetationType, GeneralEcologicalZone, LandUse)


admin.site.register(AustralianSoilClassification)
admin.site.register(FAOSoilClassification)


class DrainageAdmin(admin.ModelAdmin):
    list_display = ('drainage', 'description')


admin.site.register(DrainageClassification, DrainageAdmin)


class SoilTextureAdmin(admin.ModelAdmin):
    list_display = ('texture', 'description')


admin.site.register(SoilTexture, SoilTextureAdmin)


class ColourAdmin(admin.ModelAdmin):
    list_display = ('colour', 'code')


admin.site.register(SoilColour, ColourAdmin)


class LandUseAdmin(MPTTModelAdmin, SortableModelAdmin):
    mptt_level_indent = 20
    search_fields = ('description', )
    list_display = ('description',)
    list_display_links = ('description',)
    sortable = 'order'



admin.site.register(LandUse, LandUseAdmin)

admin.site.register(HorizonClassification)
admin.site.register(ProfilePosition)
admin.site.register(TillageType)
admin.site.register(BroadVegetationType)
admin.site.register(GeneralEcologicalZone)
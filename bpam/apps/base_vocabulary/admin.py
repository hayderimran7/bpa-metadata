from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from suit.admin import SortableModelAdmin, AutosizedTextarea
from django import forms

from models import (AustralianSoilClassification, FAOSoilClassification, DrainageClassification, SoilTexture,
                    SoilColour, HorizonClassification,
                    ProfilePosition, TillageType, BroadVegetationType, GeneralEcologicalZone, LandUse)


class AustralianSoilAdmin(admin.ModelAdmin):
    class Form(forms.ModelForm):
        class Meta:
            model = AustralianSoilClassification
            widgets = {
                'classification': forms.TextInput(attrs={'class': 'input-large'}),
                'note': AutosizedTextarea(attrs={'class': 'input-xlarge', 'style': 'width:95%'})
            }

    form = Form
    list_display = ('classification', 'note',)


admin.site.register(AustralianSoilClassification, AustralianSoilAdmin)


class FAOSoilAdmin(admin.ModelAdmin):
    class Form(forms.ModelForm):
        class Meta:
            model = FAOSoilClassification
            widgets = {
                'classification': forms.TextInput(attrs={'class': 'input-large'}),
                'note': AutosizedTextarea(attrs={'class': 'input-xlarge', 'style': 'width:95%'})
            }

    form = Form
    list_display = ('classification', 'note',)


admin.site.register(FAOSoilClassification, FAOSoilAdmin)


class DrainageAdmin(admin.ModelAdmin):
    class Form(forms.ModelForm):
        class Meta:
            model = DrainageClassification
            widgets = {
                'drainage': forms.TextInput(attrs={'class': 'input-large'}),
                'description': AutosizedTextarea(attrs={'class': 'input-xlarge', 'style': 'width:95%'})
            }

    form = Form
    list_display = ('drainage', 'description')


admin.site.register(DrainageClassification, DrainageAdmin)


class SoilTextureAdmin(admin.ModelAdmin):
    class Form(forms.ModelForm):
        class Meta:
            model = SoilTexture
            widgets = {
                'texture': forms.TextInput(attrs={'class': 'input-large'}),
                'description': AutosizedTextarea(attrs={'class': 'input-xlarge', 'style': 'width:95%'})
            }

    form = Form

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


class HorizonAdmin(admin.ModelAdmin):
    class Form(forms.ModelForm):
        class Meta:
            model = HorizonClassification
            widgets = {
                'horizon': forms.TextInput(attrs={'class': 'input-large'}),
                'description': AutosizedTextarea(attrs={'class': 'input-xlarge', 'style': 'width:95%'})
            }

    form = Form
    list_display = ('horizon', 'description',)


admin.site.register(HorizonClassification, HorizonAdmin)

admin.site.register(ProfilePosition)


class TillageAdmin(admin.ModelAdmin):
    class Form(forms.ModelForm):
        class Meta:
            model = TillageType
            widgets = {
                'tillage': forms.TextInput(attrs={'class': 'input-large'}),
                'description': AutosizedTextarea(attrs={'class': 'input-xlarge', 'style': 'width:95%'})
            }

    form = Form
    list_display = ('tillage', 'description',)


admin.site.register(TillageType, TillageAdmin)


class BroadVegetationTypeAdmin(admin.ModelAdmin):
    class BroadVegetationTypeForm(forms.ModelForm):
        class Meta:
            model = BroadVegetationType
            widgets = {
                'vegetation': forms.TextInput(attrs={'class': 'input-large'}),
                'note': AutosizedTextarea(attrs={'class': 'input-xlarge', 'style': 'width:95%'})
            }

    form = BroadVegetationTypeForm
    list_display = ('vegetation', 'note',)


admin.site.register(BroadVegetationType, BroadVegetationTypeAdmin)

admin.site.register(GeneralEcologicalZone)
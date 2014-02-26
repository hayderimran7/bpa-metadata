from django.contrib import admin
from django import forms
from suit.widgets import LinkedSelect, AutosizedTextarea
from mptt.forms import TreeNodeChoiceField

from models import CollectionSite, ChemicalAnalysis, SiteOwner, CollectionSiteHistory, LandUse


class LandUseInlineForm(forms.ModelForm):
    current_land_use = TreeNodeChoiceField(queryset=LandUse.objects.all())


class LandUseInline(admin.TabularInline):
    model = LandUse
    form = LandUseInlineForm
    extra = 1


class CollectionSiteAdmin(admin.ModelAdmin):
    class CollectionForm(forms.ModelForm):
        class Meta:
            model = CollectionSite
            widgets = {
                'location_name': AutosizedTextarea(attrs={'class': 'input-large', 'style': 'width:95%'}),
                'note': AutosizedTextarea(attrs={'class': 'input-large', 'style': 'width:95%'}),
                'plot_description': AutosizedTextarea(attrs={'class': 'input-large', 'style': 'width:95%'}),
                'debug_note': AutosizedTextarea(attrs={'class': 'input-large', 'style': 'width:95%'}),
                'vegetation_type_descriptive': AutosizedTextarea(attrs={'class': 'input-large', 'style': 'width:95%'}),
                'vegetation_dominant_trees': AutosizedTextarea(attrs={'class': 'input-large', 'style': 'width:95%'}),
                'vegetation_total_cover': forms.TextInput(attrs={'class': 'input-xlarge'}),
                'horizon_classification': LinkedSelect,
                'soil_type_australian_classification': LinkedSelect,
                'soil_type_fao_classification': LinkedSelect,
                # 'current_land_use': TreeNodeChoiceField(queryset=LandUse.objects.all()),
                'general_ecological_zone': LinkedSelect,
                'vegetation_type': LinkedSelect
            }

    form = CollectionForm
    # inlines = (LandUseInline, )

    fieldsets = [
        ('Location Description',
         {'fields': (
             'location_name',
             'plot_description',
             ('lat', 'lon'),
             'country',
             'state',
             'image_url',
         )}),
        ('Vegetation',
         {'fields': (
             'current_land_use',
             'vegetation_type',
             'general_ecological_zone',
             'vegetation_type_descriptive',
             'vegetation_total_cover',
             'vegetation_dominant_trees',
         )}),
        ('Context',
         {'fields': (
             'horizon_classification',
             'collection_depth',
             'elevation',
             ('slope', 'slope_aspect'),
             'profile_position',
             'drainage_classification',
             'soil_type_australian_classification'
         )}),
        ('History',
         {'fields': (
             'owner',
             'history'
         )}),
        ('Notes', {'fields': ('note', 'debug_note', )})

    ]

    list_display = ('location_name', 'lat', 'lon')


admin.site.register(CollectionSite, CollectionSiteAdmin)


class ChemicalAnalysisAdmin(admin.ModelAdmin):
    list_display = ('bpa_id', 'lab_name_id', 'depth', 'colour', 'gravel', 'texture')


admin.site.register(ChemicalAnalysis, ChemicalAnalysisAdmin)

admin.site.register(SiteOwner)
admin.site.register(CollectionSiteHistory)




    
    


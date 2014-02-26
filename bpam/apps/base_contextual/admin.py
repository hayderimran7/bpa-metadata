from django.contrib import admin
from django import forms
from suit.widgets import LinkedSelect, AutosizedTextarea, SuitDateWidget, EnclosedInput
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
                'fire_history': AutosizedTextarea(attrs={'class': 'input-large', 'style': 'width:95%'}),
                'fire_intensity': EnclosedInput(prepend='icon-fire'),
                'vegetation_total_cover': forms.TextInput(attrs={'class': 'input-xlarge'}),
                'horizon_classification1': LinkedSelect,
                'horizon_classification2': LinkedSelect,
                'soil_type_australian_classification': LinkedSelect,
                'soil_type_fao_classification': LinkedSelect,
                'current_land_use': LinkedSelect,
                'general_ecological_zone': LinkedSelect,
                'vegetation_type': LinkedSelect,
                'date_sampled': SuitDateWidget,
            }

    form = CollectionForm
    # inlines = (LandUseInline, )

    fieldsets = [
        ('Location Description',
         {'fields': (
             'location_name',
             'plot_description',
             'date_sampled',
             ('lat', 'lon', 'elevation'),
             'country',
             'state',
             'image_url',
         )}),
        ('Vegetation',
         {'description': 'Vegetation found on site',
          'fields': (
              'current_land_use',
              'vegetation_type',
              'general_ecological_zone',
              'vegetation_type_descriptive',
              'vegetation_total_cover',
              'vegetation_dominant_trees',
          )}),
        ('Context',
         {  #'classes': ('suit-tab suit-tab-general',),
            'description': 'Sample site contextual information',
            'fields': (
                'horizon_classification1',
                'horizon_classification2',
                'upper_depth',
                'lower_depth',
                ('slope', 'slope_aspect'),
                'profile_position',
                'drainage_classification',
                ('soil_type_australian_classification', 'soil_type_fao_classification'),
            )}),
        ('Fire',
         {'description': 'Site Fire History',
          'fields': (
              'fire_history',
              'fire_intensity'
          )}),
        ('History',
         {'description': 'General Site History',
          'fields': (
              'owner',
              'history'
          )}),
        ('Notes', {'fields': ('note', 'debug_note', )})

    ]
    list_select_related = True
    search_fields = ('location_name', 'plot_description', 'note', 'vegetation_type_descriptive',)
    list_filter = ('location_name', 'date_sampled', 'vegetation_type', 'vegetation_type_descriptive', )
    list_display = ('location_name', 'vegetation_type_descriptive', 'lat', 'lon', 'elevation')


admin.site.register(CollectionSite, CollectionSiteAdmin)


class ChemicalAnalysisAdmin(admin.ModelAdmin):
    list_display = ('bpa_id', 'lab_name_id', 'depth', 'colour', 'gravel', 'texture')


admin.site.register(ChemicalAnalysis, ChemicalAnalysisAdmin)

admin.site.register(SiteOwner)
admin.site.register(CollectionSiteHistory)




    
    


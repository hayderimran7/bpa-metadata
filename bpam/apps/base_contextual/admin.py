# -*- coding: utf-8 -*-

from django.contrib import admin
from django import forms
from suit.widgets import LinkedSelect, AutosizedTextarea, SuitDateWidget, EnclosedInput
from mptt.forms import TreeNodeChoiceField

from models import CollectionSite, SampleContext, ChemicalAnalysis, LandUse


class CollectionSampleAdmin(admin.ModelAdmin):
    class SampleForm(forms.ModelForm):
        class Meta:
            model = SampleContext
            widgets = {
                'bpa_id': LinkedSelect,
                'site': LinkedSelect,
                'horizon_classification1': LinkedSelect,
                'horizon_classification2': LinkedSelect,
                'debug_note': AutosizedTextarea(attrs={'class': 'input-large', 'style': 'width:95%'}),
                'methodological_notes': AutosizedTextarea(attrs={'class': 'input-large', 'style': 'width:95%'}),
            }

    form = SampleForm

    fieldsets = [
        ('Sample Description',
         {'description': 'Sample contextual information',
          'fields': (
              'bpa_id',
              'site',
              'horizon_classification1',
              'horizon_classification2',
              'depth',
              'methodological_notes'
          )}),
        ('Notes', {'fields': ('debug_note', )}),
    ]
    list_select_related = True
    search_fields = ('horizon_classification1', 'horizon_classification2', 'methodological_notes')
    list_filter = ('bpa_id', 'site', 'depth', )
    list_display = ('bpa_id', 'horizon_classification1', 'horizon_classification2', 'depth',)


admin.site.register(SampleContext, CollectionSampleAdmin)


class LandUseInlineForm(forms.ModelForm):
    current_land_use = TreeNodeChoiceField(queryset=LandUse.objects.all())


class LandUseInline(admin.TabularInline):
    model = LandUse
    form = LandUseInlineForm
    extra = 1


class CollectionSiteAdmin(admin.ModelAdmin):
    class CollectionSampleInline(admin.TabularInline):
        class CollectionSampleInlineForm(forms.ModelForm):
            class Meta:
                model = SampleContext

        suit_classes = 'suit-tab suit-tab-samples'
        model = SampleContext
        form = CollectionSampleInlineForm
        fields = ('bpa_id', 'horizon_classification1', 'horizon_classification2', 'depth')
        extra = 0

    class CollectionForm(forms.ModelForm):
        class Meta:
            model = CollectionSite
            widgets = {
                'location_name': AutosizedTextarea(attrs={'class': 'input-large', 'style': 'width:95%'}),
                'debug_note': AutosizedTextarea(attrs={'class': 'input-large', 'style': 'width:95%'}),
                'vegetation_dominant_trees': AutosizedTextarea(attrs={'class': 'input-large', 'style': 'width:95%'}),
                'slope': EnclosedInput(append='%'),
                'fire_history': AutosizedTextarea(attrs={'class': 'input-large', 'style': 'width:95%'}),
                'fire_intensity': EnclosedInput(prepend='icon-fire'),
                'vegetation_total_cover': forms.TextInput(attrs={'class': 'input-xlarge'}),
                'soil_type_australian_classification': LinkedSelect,
                'soil_type_fao_classification': LinkedSelect,
                'current_land_use': LinkedSelect,
                'immediate_previous_land_use': LinkedSelect,
                'date_since_change_in_land_use': SuitDateWidget,
                'crop_rotation_1': LinkedSelect,
                'crop_rotation_2': LinkedSelect,
                'crop_rotation_3': LinkedSelect,
                'crop_rotation_4': LinkedSelect,
                'crop_rotation_5': LinkedSelect,
                'general_ecological_zone': LinkedSelect,
                'vegetation_type': LinkedSelect,
                'date_sampled': SuitDateWidget,
                'profile_position': LinkedSelect,
                'drainage_classification': LinkedSelect,
                'tillage': LinkedSelect,
                'agrochemical_additions': AutosizedTextarea(attrs={'class': 'input-large', 'style': 'width:95%'}),
                'other_comments': AutosizedTextarea(attrs={'class': 'input-large', 'style': 'width:95%'}),
            }

    form = CollectionForm
    inlines = (CollectionSampleInline, )
    suit_form_tabs = (
        ('description', 'Location Description'),
        ('context', 'Context'),
        ('landuse', 'Land Use'),
        ('vegetation', 'Vegetation'),
        ('fire', 'Fire'),
        ('samples', 'Collection Samples'),
        ('notes', 'Notes')
    )

    fieldsets = [
        (None,  # 'Location Description',
         {'classes': ('suit-tab suit-tab-description',),
          'fields': (
              'location_name',
              'date_sampled',
              'lat',
              'lon',
              'elevation',
              'country',
              'state',
              'image_url',
          )}),
        (None,  # 'Vegetation',
         {'classes': ('suit-tab suit-tab-vegetation',),
          'description': 'Vegetation found on site',
          'fields': (
              'vegetation_type',
              'general_ecological_zone',
              'vegetation_total_cover',
              'vegetation_dominant_trees',
          )}),
        (None,  # Land use,
         {'classes': ('suit-tab suit-tab-landuse',),
          'description': 'Current and previous Land Use',
          'fields': (
              'current_land_use',
              'immediate_previous_land_use',
              'date_since_change_in_land_use',
              'crop_rotation_1',
              'crop_rotation_2',
              'crop_rotation_3',
              'crop_rotation_4',
              'crop_rotation_5',
              'tillage',
              'agrochemical_additions',
              'other_comments',
          )}),
        (None,  # 'Context',
         {'classes': ('suit-tab suit-tab-context',),
          'description': 'Sample site contextual information',
          'fields': (
              'slope',
              'slope_aspect',
              'profile_position',
              'drainage_classification',
              'soil_type_australian_classification',
              'soil_type_fao_classification',
          )}),
        (None,  # 'Fire',
         {'classes': ('suit-tab suit-tab-fire',),
          'description': 'Site Fire History',
          'fields': (
              'fire_history',
              'fire_intensity'
          )}),
        (None,  # 'Notes',
         {'classes': ('suit-tab suit-tab-notes',),
          'fields': (
              'debug_note',
          )})
    ]

    list_select_related = True
    search_fields = ('location_name', 'other_comments', 'vegetation_type_descriptive', 'vegetation_dominant_trees')
    list_filter = ('location_name', 'date_sampled', 'current_land_use__description', 'vegetation_type',
                   'vegetation_dominant_trees')
    list_display = ('location_name', 'current_land_use', 'vegetation_type', 'lat', 'lon', 'elevation')


admin.site.register(CollectionSite, CollectionSiteAdmin)


class ChemicalAnalysisAdmin(admin.ModelAdmin):
    class ChemicalAnalysisForm(forms.ModelForm):
        class Meta:
            model = ChemicalAnalysis
            widgets = {
                'bpa_id': LinkedSelect,
                'colour': LinkedSelect,
                'moisture': EnclosedInput(append='%'),
                'gravel': EnclosedInput(append='%'),
                'course_sand': EnclosedInput(append='%'),
                'fine_sand': EnclosedInput(append='%'),
                'sand': EnclosedInput(append='%'),
                'clay': EnclosedInput(append='%'),

                'ammonium_nitrogen': EnclosedInput(append='mg/Kg'),
                'nitrate_nitrogen': EnclosedInput(append='mg/Kg'),
                'phosphorus_colwell': EnclosedInput(append='mg/Kg'),
                'potassium_colwell': EnclosedInput(append='mg/Kg'),
                'sulphur_colwell': EnclosedInput(append='mg/Kg'),
                'organic_carbon': EnclosedInput(append='%'),
                'conductivity': EnclosedInput(append='dS/m'),
                'cacl2_ph': EnclosedInput(append='pH'),
                'h20_ph': EnclosedInput(append='pH'),
                'dtpa_copper': EnclosedInput(append='mg/Kg'),
                'dtpa_iron': EnclosedInput(append='mg/Kg'),
                'dtpa_manganese': EnclosedInput(append='mg/Kg'),
                'dtpa_zinc': EnclosedInput(append='mg/Kg'),

                'exc_aluminium': EnclosedInput(append='meq/100g'),
                'exc_calcium': EnclosedInput(append='meq/100g'),
                'exc_magnesium': EnclosedInput(append='meq/100g'),
                'exc_potassium': EnclosedInput(append='meq/100g'),
                'exc_sodium': EnclosedInput(append='meq/100g'),

                'boron_hot_cacl2': EnclosedInput(append='mg/Kg'),
            }

    form = ChemicalAnalysisForm
    suit_form_tabs = (
        ('structure', 'Soil Structure'),
        ('chemical', 'Chemical'),
    )

    fieldsets = [
        (None,  # structual
         {'classes': ('suit-tab suit-tab-structure',),
          'description': 'Soil Structure',
          'fields': (
              'bpa_id',
              'colour',
              'texture',
              'moisture',
              'gravel',
              'course_sand',
              'fine_sand',
              'sand',
              'clay',
          )}),
        (None,  # chemical
         {'classes': ('suit-tab suit-tab-chemical',),
          'description': 'Chemical Analysis',
          'fields': (
              'ammonium_nitrogen',
              'nitrate_nitrogen',
              'phosphorus_colwell',
              'potassium_colwell',
              'sulphur_colwell',
              'organic_carbon',
              'conductivity',
              'cacl2_ph',
              'h20_ph',
              'dtpa_copper',
              'dtpa_iron',
              'dtpa_manganese',
              'dtpa_zinc',
              'exc_aluminium',
              'exc_calcium',
              'exc_magnesium',
              'exc_potassium',
              'exc_sodium',
              'boron_hot_cacl2',
              'total_nitrogen',
              'total_carbon'
          )})
    ]

    list_display = ('bpa_id', 'depth', 'colour', 'texture', 'gravel', 'sand', 'course_sand', 'fine_sand', 'clay',)
    list_filter = ('bpa_id', 'depth', 'colour',)
    search_fields = ('colour__colour', 'colour__code',)


admin.site.register(ChemicalAnalysis, ChemicalAnalysisAdmin)






    
    


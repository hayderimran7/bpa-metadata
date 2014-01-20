from django.contrib import admin
from django import forms
from .models.metagenomics import *
from .models.sample454 import *
from .models.site import *

from apps.common.admin import SequenceFileAdmin


class LandUseAdmin(admin.ModelAdmin):
    list_display = ('description', 'classification')


admin.site.register(LandUse, LandUseAdmin)


class SampleAdmin(admin.ModelAdmin):
    list_display = ('bpa_id', 'name')


admin.site.register(SoilMetagenomicsSample, SampleAdmin)


class Sample454Admin(admin.ModelAdmin):
    class Sample454AdminForm(forms.ModelForm):
        class Meta:
            model = Sample454
            widgets = {
                'note': forms.TextInput(attrs={'class': 'input-large',
                                               'style': 'width:95%'}),
            }

    form = Sample454AdminForm
    list_display = ('bpa_id', 'sample_id', 'agrf_batch_number',)
    search_fields = ('bpa_id__bpa_id', 'sample_id',)
    list_filter = ('bpa_id__bpa_id', 'sample_id')

    radio_fields = {'adelaide_pcr_inhibition': admin.HORIZONTAL,
                    'adelaide_pcr1': admin.HORIZONTAL,
                    'adelaide_pcr2': admin.HORIZONTAL,
                    'brisbane_16s_pcr1': admin.HORIZONTAL,
                    'brisbane_16s_pcr2': admin.HORIZONTAL,
                    'brisbane_16s_pcr3': admin.HORIZONTAL,
                    'brisbane_its_pcr1_neat': admin.HORIZONTAL,
                    'brisbane_its_pcr2_1_10': admin.HORIZONTAL,
                    'brisbane_its_pcr3_fusion': admin.HORIZONTAL}

    fieldsets = [
        (None,
         {'fields':
              ('bpa_id', 'sample_id', 'aurora_purified', 'agrf_batch_number', 'submitter', 'date_received')
         }),
        ('DNA Storage',
         {'fields':
              ('dna_storage_nunc_plate', 'dna_storage_nunc_tube', 'dna_storage_nunc_well_location', )
         }),
        ('AGRF Adelaide Extraction',
         {'description': 'Extracted at Adelaide Node',
          'fields':
              ('adelaide_extraction_sample_weight',
               'adelaide_fluorimetry',
               'adelaide_pcr_inhibition',
               'adelaide_pcr1',
               'adelaide_pcr2',
               'adelaide_date_shipped_to_agrf_454',
               'adelaide_date_shipped_to_agrf_miseq',
               'adelaide_date_shipped_to_ramacciotti')
         }),
        ('Brisbane 454',
         {'description': 'Extracted at Brisbane Node',
          'fields':
              ('brisbane_16s_mid',
               'brisbane_its_mid',
               'brisbane_16s_pcr1',
               'brisbane_16s_pcr2',
               'brisbane_16s_pcr3',
               'brisbane_its_pcr1_neat',
               'brisbane_its_pcr2_1_10',
               'brisbane_its_pcr3_fusion',
               'brisbane_fluorimetry_16s',
               'brisbane_fluorimetry_its',
               'brisbane_16s_qpcr',
               'brisbane_its_qpcr',
               'brisbane_i6s_pooled',
               'brisbane_its_pooled',
               'brisbane_16s_reads',
               'brisbane_its_reads',)
         }),
        ('Comments and Notes',
         {'description': 'Any notes or comments on this Extraction',
          'fields': ('note', )})
    ]


admin.site.register(Sample454, Sample454Admin)


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

admin.site.register(MetagenomicsSequenceFile, SequenceFileAdmin)

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


    
    


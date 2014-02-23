from django.contrib import admin
from django import forms
from suit.widgets import LinkedSelect, AutosizedTextarea, SuitDateWidget

from ..models.sample454 import *


class Sample454Admin(admin.ModelAdmin):
    class Sample454AdminForm(forms.ModelForm):
        class Meta:
            model = Sample454
            widgets = {
                'bpa_id': LinkedSelect,
                'submitter': LinkedSelect,
                'date_received': SuitDateWidget,
                'adelaide_date_shipped_to_agrf_454': SuitDateWidget,
                'adelaide_date_shipped_to_agrf_miseq': SuitDateWidget,
                'adelaide_date_shipped_to_ramacciotti': SuitDateWidget,
                'note': AutosizedTextarea(attrs={'class': 'input-large', 'style': 'width:95%'}),
                'debug_note': AutosizedTextarea(attrs={'class': 'input-large', 'style': 'width:95%'}),
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
          'fields': ('note', 'debug_note')})
    ]


admin.site.register(Sample454, Sample454Admin)

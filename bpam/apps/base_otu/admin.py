from django.contrib import admin
from django import forms

from .models import OperationalTaxonomicUnit, SampleOTU


class OperationalTaxonomicUnitAdmin(admin.ModelAdmin):
    class Form(forms.ModelForm):
        class Meta:
            model = OperationalTaxonomicUnit
            widgets = {
                'name': forms.TextInput(),
            }

    form = Form
    list_display = ('name', 'kingdom', 'phylum', 'otu_class', 'order', 'family', 'genus', 'species', )
    search_fields = ('name', 'kingdom', 'phylum', 'otu_class', 'order', 'family', 'genus', 'species', )



class SampleOTUAdmin(admin.ModelAdmin):
    class Form(forms.ModelForm):
        class Meta:
            model = SampleOTU
            widgets = {
                'name': forms.TextInput(),
            }

    form = Form
    list_display = ('sample', 'otu', 'count', )
    search_fields = ('sample__bpa_id__bpa_id', 'otu__name', )

admin.site.register(OperationalTaxonomicUnit, OperationalTaxonomicUnitAdmin)
admin.site.register(SampleOTU, SampleOTUAdmin)

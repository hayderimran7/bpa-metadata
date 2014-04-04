from django.contrib import admin
from django import forms

from .models import OperationalTaxonomicUnit


class OperationalTaxonomicUnitAdmin(admin.ModelAdmin):
    class Form(forms.ModelForm):
        class Meta:
            model = OperationalTaxonomicUnit
            widgets = {
                'name': forms.TextInput(),
            }

    form = Form
    list_display = ('name',)


admin.site.register(OperationalTaxonomicUnit, OperationalTaxonomicUnitAdmin)
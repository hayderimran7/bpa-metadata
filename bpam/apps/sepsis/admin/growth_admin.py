# -*- coding: utf-8 -*-

from django.contrib import admin
from django import forms
from django.utils.html import format_html
from suit.widgets import AutosizedTextarea
from suit.widgets import LinkedSelect
from suit.widgets import SuitDateWidget

from apps.common.admin import BPAImportExportModelAdmin

from ..models import GrowthMethod


class Form(forms.ModelForm):
    class Meta:
        fields = "__all__"
        model = GrowthMethod
        widgets = {
            'note': AutosizedTextarea(attrs={'class': 'input-large',
                                             'style': 'width:95%'}),
            'growth_condition_temperature':
            AutosizedTextarea(attrs={'class': 'input-large',
                                     'style': 'width:95%'}),
            'growth_condition_time':
            AutosizedTextarea(attrs={'class': 'input-large',
                                     'style': 'width:95%'}),
            'growth_condition_media':
            AutosizedTextarea(attrs={'class': 'input-large',
                                     'style': 'width:95%'}),
        }


class Admin(BPAImportExportModelAdmin):
    form = Form
    list_display = ("growth_condition_media",
                    "growth_condition_temperature",
                    "growth_condition_time",
                    "note", )

    fields = list_display
    list_filter = list_display


admin.site.register(GrowthMethod, Admin)

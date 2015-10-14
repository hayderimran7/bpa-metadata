# -*- coding: utf-8 -*-

from django.contrib import admin
from django import forms
from suit.widgets import LinkedSelect, AutosizedTextarea, SuitDateWidget, EnclosedInput

from .models import Sheet

class SheetAdmin(admin.ModelAdmin):
    class SheetForm(forms.ModelForm):
        class Meta:
            fields = "__all__"
            model = Sheet
            widgets = {
                    "latitude": EnclosedInput(prepend="icon-map-marker"),
                    "longitude": EnclosedInput(prepend="icon-map-marker"),
                    "note": AutosizedTextarea(attrs={"class": "input-large", "style": "width:95%"}),
                    "plant_description": AutosizedTextarea(attrs={"class": "input-large", "style": "width:95%"}),
                    "site_description": AutosizedTextarea(attrs={"class": "input-large", "style": "width:95%"}),
                    "vegetation": AutosizedTextarea(attrs={"class": "input-large", "style": "width:95%"}),
                    }

    form = SheetForm
    fieldsets = [
            ("Sheet",
                {"fields": ("sheet_number", "name_id", "plant_description", "site_description", "vegetation",), }),
            ("Location",
                {"fields": ("latitude", "longitude", "geocode_accuracy", "geocode_method", "barker_coordinate_accuracy_flag", "datum",), }),
            ("Flora",
                {"fields": ( "family", "genus", "species", "rank", "infraspecies_qualifier", "infraspecies"), }),
            ("Note",
                {"fields": ("note",) }),
            ]

    list_display = ("sheet_number", "latitude", "longitude", "note")
    search_fields = ("sheet_number", "latitude", "longitude", "note")
    list_filter = ("sheet_number", "latitude", "longitude",)

admin.site.register(Sheet, SheetAdmin)

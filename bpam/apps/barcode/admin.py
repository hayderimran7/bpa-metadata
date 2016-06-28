# -*- coding: utf-8 -*-

from django.contrib import admin
from django import forms
from suit.widgets import AutosizedTextarea, EnclosedInput

from .models import Sheet


class SheetAdmin(admin.ModelAdmin):
    class SheetForm(forms.ModelForm):
        class Meta:
            fields = "__all__"
            model = Sheet
            widgets = {
                "name_id": AutosizedTextarea(attrs={"class": "input-small",
                                                    "style": "width:55%"}),
                "latitude": EnclosedInput(prepend="icon-map-marker"),
                "longitude": EnclosedInput(prepend="icon-map-marker"),
                "note": AutosizedTextarea(attrs={"class": "input-large",
                                                 "style": "width:95%"}),
                "plant_description": AutosizedTextarea(attrs={"class": "input-large",
                                                              "style": "width:95%"}),
                "site_description": AutosizedTextarea(attrs={"class": "input-large",
                                                             "style": "width:95%"}),
                "vegetation": AutosizedTextarea(attrs={"class": "input-large",
                                                       "style": "width:95%"}),
                "name_comment": AutosizedTextarea(attrs={"class": "input-large",
                                                         "style": "width:95%"}),
                "locality": AutosizedTextarea(attrs={"class": "input-large",
                                                     "style": "width:95%"}),
                "voucher": AutosizedTextarea(attrs={"class": "input-large",
                                                    "style": "width:95%"}),
            }

    form = SheetForm
    fieldsets = [
        ("Sheet", {"fields": ("sheet_number",
                              "bpa_id",
                              "name_id",
                              "plant_description",
                              "site_description",
                              "vegetation", ), }),
        ("Location", {"fields": ("latitude",
                                 "longitude",
                                 "geocode_accuracy",
                                 "geocode_method",
                                 "barker_coordinate_accuracy_flag",
                                 "datum", ), }),
        ("Flora", {"fields": ("family",
                              "genus",
                              "species",
                              "rank",
                              "infraspecies_qualifier",
                              "infraspecies",
                              "alien", ), }),
        ("Determination", {"fields": ("author",
                                      "manuscript",
                                      "conservation_code",
                                      "determiner_name",
                                      "date_of_determination",
                                      "determiner_role",
                                      "name_comment",
                                      "frequency",
                                      "locality",
                                      "state", ), }),
        ("Collector",
         {"fields":
          ("collector", "collector_number", "collection_date", "voucher", "voucher_id", "voucher_site", "type_status"),
          }),
        ("Note", {"fields": ("note", )}),
    ]

    list_display = ("sheet_number", "bpa_id", "family", "genus", "species", "latitude", "longitude", "note")
    search_fields = ("sheet_number", "bpa_id", "latitude", "longitude", "note")
    list_filter = ("sheet_number",
                   "bpa_id",
                   "latitude",
                   "longitude", )


admin.site.register(Sheet, SheetAdmin)

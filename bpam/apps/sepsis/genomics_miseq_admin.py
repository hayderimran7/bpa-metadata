# -*- coding: utf-8 -*-

from django.contrib import admin
from django import forms
from suit.widgets import LinkedSelect, AutosizedTextarea, SuitDateWidget, EnclosedInput
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields, widgets

from .models import GenomicsMiseqFile

class FileForm(forms.ModelForm):
    class Meta:
        fields = "__all__"
        model = GenomicsMiseqFile
        widgets = {
            'date_received_from_sequencing_facility': SuitDateWidget,
            'filename': forms.TextInput(
                attrs={'class': 'input-medium',
                        'style': 'width:50%'}),
            'md5': forms.TextInput(
                attrs={'class': 'input-medium',
                        'style': 'width:50%'}),
            'sample': LinkedSelect(
                attrs={'class': 'input-medium',
                        'style': 'width:40%'}),
            'note': AutosizedTextarea(
                attrs={'class': 'input-large',
                        'style': 'width:95%'})
        }

class FileAdmin(admin.ModelAdmin):
    form = FileForm

    fieldsets = [
        ('Sequence File',
         {'fields': (
             'filename',
             'md5',
             'sample',
             'lane_number',
             'index_number',
             'analysed',
             'vendor',
             'date_received_from_sequencing_facility',
             'library',
             'size',
             'plate',
             'index',
             'runsamplenum',
             'read',
             'note',
             ),
         }),
    ]

    def download_field(self, obj):
        if obj.link_ok():
            return '<a href="%s">%s</a>' % (obj.url, obj.filename)
        else:
            return '<a style="color:grey">%s</a>' % obj.filename

    download_field.allow_tags = True
    download_field.short_description = 'Filename'

    # Sample ID
    def get_sample_id(self, obj):
        return obj.sample.bpa_id

    get_sample_id.short_description = 'BPA ID'
    get_sample_id.admin_order_field = 'sample__bpa_id'

    list_display = ('filename', 'get_sample_id', )
    search_fields = ('sample__bpa_id__bpa_id', )
    list_filter = ('sample__bpa_id', 'date_received_from_sequencing_facility',)

# -*- coding: utf-8 -*-

from django.contrib import admin
from django import forms
from django.utils.html import format_html
from suit.widgets import AutosizedTextarea
from suit.widgets import LinkedSelect
from suit.widgets import SuitDateWidget
from import_export.admin import ImportExportModelAdmin

from ..models import GenomicsMiseqFile


class FileForm(forms.ModelForm):
    class Meta:
        fields = "__all__"
        model = GenomicsMiseqFile
        widgets = {
            'date_received_from_sequencing_facility': SuitDateWidget,
            'md5': forms.TextInput(attrs={'class': 'input-large',
                                          'style': 'font-family: monospace'}),
            'filename': forms.TextInput(attrs={'class': 'input-medium',
                                               'style': 'width:50%'}),
            'sample': LinkedSelect(attrs={'class': 'input-medium',
                                          'style': 'width:40%'}),
            'method': LinkedSelect(attrs={'class': 'input-medium',
                                          'style': 'width:40%'}),
            'note': AutosizedTextarea(attrs={'class': 'input-large',
                                             'style': 'width:95%'})
        }


class FileAdmin(ImportExportModelAdmin):
    form = FileForm

    fieldsets = [
        ('Sequence File', {'fields': ('filename',
                                      'sample',
                                      'extraction',
                                      'library',
                                      'size',
                                      'vendor',
                                      'flow_cell_id',
                                      'index',
                                      'runsamplenum',
                                      'lane_number',
                                      'read', )}),
        ('Metadata', {'fields': ('date_received_from_sequencing_facility',
                                 'method',
                                 'md5',
                                 'analysed',
                                 'note', )}),
    ]

    def monospace_md5(obj):
        return format_html('<span style="font-family: monospace;">{}</span>', obj.md5)

    monospace_md5.short_description = "MD5 Checksum"

    list_display = ('filename',
                    monospace_md5,
                    'sample',
                    'extraction',
                    'library',
                    'index',
                    'vendor', )
    list_display_links = ('filename', )
    search_fields = list_display  # the search field widget
    list_filter = ('sample',
                   'library',
                   'index',
                   'date_received_from_sequencing_facility',
                   'vendor', )


admin.site.register(GenomicsMiseqFile, FileAdmin)

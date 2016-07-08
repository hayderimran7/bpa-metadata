# -*- coding: utf-8 -*-

from django.contrib import admin
from django import forms
from django.utils.html import format_html
from suit.widgets import AutosizedTextarea
from suit.widgets import LinkedSelect
from suit.widgets import SuitDateWidget
from import_export.admin import ImportExportModelAdmin

from apps.common.admin import CommonAmpliconAdmin
from apps.common.admin import CommonAmpliconResource

from ..models import Amplicon
from ..models import AmpliconSequenceFile


class AmpliconResource(CommonAmpliconResource):
    class Meta(CommonAmpliconResource.Meta):
        model = Amplicon


class AmpliconAdmin(CommonAmpliconAdmin):
    resource_class = AmpliconResource


class FileForm(forms.ModelForm):
    class Meta:
        fields = "__all__"
        model = AmpliconSequenceFile
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
                                      'amplicon',
                                      'vendor',
                                      'index',
                                      'flow_cell',
                                      'runsamplenum',
                                      'read',
                                      'pcr_1_to_10',
                                      'pcr_1_to_100',
                                      'pcr_neat',
                                      'dilution',
                                      'number_of_reads',
                                      'analysis_software_version')}),
        ('Metadata', {'fields': ('date_received_from_sequencing_facility',
                                 'md5',
                                 'analysed',
                                 'note', )}),
    ] # yapf: disable

    def monospace_md5(obj):
        return format_html('<span style="font-family: monospace;">{}</span>', obj.md5)

    monospace_md5.short_description = "MD5 Check sum"

    list_display = ('filename',
                    monospace_md5,
                    'sample',
                    'extraction',
                    'amplicon',
                    'vendor',
                    'read',
                    'pcr_1_to_10',
                    'pcr_1_to_100',
                    'pcr_neat',
                    'dilution',
                    'index', )

    list_display_links = ('filename', )
    search_fields = list_display  # the search field widget
    list_filter = ('sample',
                   'amplicon',
                   'index',
                   'date_received_from_sequencing_facility',
                   'vendor', )


admin.site.register(Amplicon, AmpliconAdmin)
admin.site.register(AmpliconSequenceFile, FileAdmin)

# -*- coding: utf-8 -*-
import logging
from functools import partial
from django.contrib import admin
from django import forms
from suit.widgets import AutosizedTextarea, SuitDateWidget, LinkedSelect

from libs.ingest_utils import get_date
from django.contrib.gis.admin import OSMGeoAdmin
from django.contrib.gis.geos import Point
from django.http import HttpResponse
from django.utils.html import format_html
from import_export import resources, fields, widgets
from import_export.formats import base_formats
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin

from django.conf import settings
from .models import BPAProject
from .models import BPAUniqueID
from .models import CKANServer
from .models import Facility
from .models import Organism
from .models import SequenceFile
from .models import DNASource
from .models import Sequencer
from .models import Sample
from .models import SampleSite

TICKET_URL = ""


logger = logging.getLogger(__name__)


class CKANServerAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_url')


admin.site.register(CKANServer, CKANServerAdmin)


class BPAImportExportModelAdmin(ImportExportModelAdmin):
    """
    Customised ImportExportModelAdmin class to be used everywhere in the project.
    """

    # The default class tries only to decode files using 'utf-8' and returns an error
    # if that fails.
    # Our class changes the default behaviour to try all the ENCODINGS defined below
    ENCODINGS = ('utf-8', 'latin1', 'windows-1252')

    IMPORT_FORMATS = (base_formats.CSV, base_formats.XLS, base_formats.XLSX)

    def get_import_formats(self):
        return filter(lambda f: f in self.IMPORT_FORMATS,
                      super(BPAImportExportModelAdmin, self).get_import_formats())

    def import_action(self, request, *args, **kwargs):
        for encoding in self.ENCODINGS:
            self.from_encoding = encoding
            response = super(BPAImportExportModelAdmin, self).import_action(request, *args, **kwargs)
            if not (type(response) is HttpResponse and 'wrong encoding' in response.content):
                break

        return response

    def process_import(self, *args, **kwargs):
        last_error = None
        for encoding in self.ENCODINGS:
            self.from_encoding = encoding
            try:
                response = super(BPAImportExportModelAdmin, self).process_import(*args, **kwargs)
                return response
            except UnicodeDecodeError as e:
                last_error = e
        raise last_error


class BPAModelResource(resources.ModelResource):

    def transform_row(self, row):
        transformations = {}
        # Override and add your transformations here
        return transformations

    def maybe_transform_row(self, row):
        transformations = self.transform_row(row)

        if len(transformations) > 0:
            logger.info('Transforming row')
            new_row = row.copy()
            # log the column headers in the order of the row (OrderedDict)
            for name in filter(lambda x: x in transformations, row):
                logger.info("'%s': '%s' -> '%s'", name, row.get(name), transformations.get(name))
            new_row.update(transformations)
            return new_row
        return row

    def import_row(self, row, *args, **kwargs):
        new_row = self.maybe_transform_row(row)
        return super(BPAModelResource, self).import_row(new_row, *args, **kwargs)


class FacilityWidget(widgets.ForeignKeyWidget):

    def __init__(self):
        self.model = Facility
        self.field = "name"

    def clean(self, value):
        facility, _ = self.model.objects.get_or_create(name=value)
        return facility


class FacilityAdmin(admin.ModelAdmin):

    class Form(forms.ModelForm):

        class Meta:
            fields = "__all__"
            model = Facility
            widgets = {
                'project': LinkedSelect,
                'note': AutosizedTextarea(attrs={'class': 'input-large',
                                                 'style': 'width:95%'})
            }

    form = Form
    fields = ('name', 'note')
    list_display = ('name', )


admin.site.register(Facility, FacilityAdmin)


class DateField(fields.Field):
    """
    This field automatically parses a number of known date formats and returns
    the standard python date
    """

    def __init__(self, *args, **kwargs):
        super(DateField, self).__init__(*args, **kwargs)

    def clean(self, data):
        return get_date(data[self.column_name])


# Amplicon
class CommonAmpliconResource(resources.ModelResource):
    extraction_id = fields.Field(attribute='extraction_id', column_name='Sample extraction ID')
    target = fields.Field(attribute='target', column_name='Target')
    comments = fields.Field(attribute='comments', column_name='Comments')
    metadata_filename = fields.Field('metadata_filename', column_name='Metadata Filename')
    facility = fields.Field(attribute='facility', column_name='Facility', widget=FacilityWidget())

    class Meta:
        abstract = True
        import_id_fields = ('extraction_id', )
        export_order = ('extraction_id', 'target', 'facility', 'metadata_filename', 'comments')


class CommonAmpliconAdmin(BPAImportExportModelAdmin):
    list_display = ('extraction_id', 'facility', 'target', 'metadata_filename', 'comments')
    list_filter = ('facility',
                   'target', )
    search_fields = ('extraction_id', 'facility__name', 'target', 'comments')


# Metagenomics
class CommonMetagenomicResource(resources.ModelResource):
    extraction_id = fields.Field(attribute='extraction_id', column_name='Sample extraction ID')
    facility = fields.Field(attribute='facility', column_name='Facility', widget=FacilityWidget())
    comments = fields.Field(attribute='comments', column_name='Comments')

    class Meta:
        abstract = True
        import_id_fields = ('extraction_id', )
        export_order = ('extraction_id', 'facility', 'metadata_filename', 'comments')


class CommonMetagenomicAdmin(BPAImportExportModelAdmin):
    list_display = ('extraction_id', 'facility', 'metadata_filename', 'comments')
    list_filter = ('facility', )
    search_fields = ('extraction_id', 'facility__name', 'comments')


# TransferLog
class CommonTransferLogResource(resources.ModelResource):
    facility = fields.Field(attribute='facility', column_name='Sequencing facility', widget=FacilityWidget())
    transfer_to_facility_date = DateField(attribute='transfer_to_facility_date', column_name='Date of transfer')
    description = fields.Field(attribute='description', column_name='Description')
    data_type = fields.Field(attribute='data_type', column_name='Data type')
    folder_name = fields.Field(attribute='folder_name', column_name='Folder name')
    transfer_to_archive_date = DateField(attribute='transfer_to_archive_date',
                                         column_name='Date of transfer to archive')
    notes = fields.Field(attribute='notes', column_name='Notes')
    ticket_url = fields.Field(attribute='ticket_url', column_name='Ticket URL')
    downloads_url = fields.Field(attribute='downloads_url', column_name='Download')

    class Meta:
        abstract = True
        import_id_fields = ('folder_name', )


class CommonTransferLogAdmin(BPAImportExportModelAdmin):

    def show_downloads_url(self, obj):
        try:
            short = obj.downloads_url.split("/")[-2]
            return format_html("<a href='{url}'>{short}</a>", url=obj.downloads_url, short=short)
        except IndexError:
            return ""

    show_downloads_url.short_description = "Downloads URL"
    show_downloads_url.allow_tags = True

    def show_ticket_url(self, obj):
        ticket_url = TICKET_URL + obj.ticket_url
        return format_html("<a href='{ticket_url}'>{url}</a>", url=obj.ticket_url, ticket_url=ticket_url)

    show_ticket_url.short_description = "Ticket URL"
    show_ticket_url.allow_tags = True

    date_hierarchy = 'transfer_to_archive_date'

    list_display = ('facility', 'transfer_to_facility_date', 'description', 'data_type', 'folder_name',
                    'transfer_to_archive_date', 'notes', 'show_ticket_url', 'show_downloads_url')

    list_filter = ('facility',
                   'transfer_to_facility_date',
                   'transfer_to_archive_date',
                   'data_type', )

    search_fields = ('facility__name', 'transfer_to_facility_date', 'description', 'data_type', 'folder_name',
                     'transfer_to_archive_date', 'notes', 'ticket_url', 'downloads_url')


class CommonDataSetAdmin(BPAImportExportModelAdmin):
    date_hierarchy = 'transfer_to_archive_date'

    list_display = ('name', 'facility', 'transfer_to_archive_date', 'ticket_url', 'downloads_url', 'note')

    list_filter = ('facility', )
    search_fields = ('facility__name',
                     'comments', )


# Site
class SampleSiteResource(resources.ModelResource):
    """
    Maps sample sites file to object. Sites file does not come with WKT strings
    it ships with lat/lon columns
    """

    # these are in the model
    name = fields.Field(attribute='name', column_name='Sample Site')
    note = fields.Field(attribute='note', column_name='Notes')

    # these come from the file, they will be converted to a point
    lat = fields.Field(attribute='lat', column_name='lat (decimal degrees)')
    lon = fields.Field(attribute='lon', column_name='long (decimal degrees)')

    def before_save_instance(self, site, dry_run):
        site.point = Point(float(site.lon), float(site.lat))

    def dehydrate_lat(self, site):
        return site.point.x

    def dehydrate_lon(self, site):
        return site.point.y

    class Meta:
        model = SampleSite  # override
        import_id_fields = ('name', )
        export_order = ('name',
                        'lat',
                        'lon',
                        'note',
                        'point', )


class SampleSiteAdmin(BPAImportExportModelAdmin, ImportExportActionModelAdmin, OSMGeoAdmin):
    resource_class = SampleSiteResource  # override
    openlayers_url = settings.GIS_OPENLAYERS_URL
    # default_zoom = settings.GIS_ZOOM
    point_zoom = settings.GIS_POINT_ZOOM
    center = Point(settings.GIS_CENTER, srid=settings.GIS_SOURCE_RID)
    center.transform(settings.GIS_TARGET_RID)
    default_lon = center.x
    default_lat = center.y

    list_display = ('name', 'point_description', 'note')

    fields = ('point', 'name', 'note', )

    list_filter = ('name', )
    search_fields = ('name', )


class SampleAdmin(admin.ModelAdmin):

    class SampleForm(forms.ModelForm):

        class Meta:
            fields = "__all__"
            model = Sample
            widgets = {
                'bpa_id': LinkedSelect(attrs={'class': 'input-medium',
                                              'style': 'width:50%'}),
                'name': forms.TextInput(attrs={'class': 'input-large',
                                               'style': 'width:95%'})
            }

    form = SampleForm
    fieldsets = [
        ('Sample Identification', {'fields': (('bpa_id', 'name'))}),
        ('DNA Source', {'fields': ('organism', 'dna_source', 'dna_extraction_protocol', 'gender', 'tumor_stage',
                                   'histological_subtype')}),
        ('Sample Management',
         {'fields': ('requested_sequence_coverage', 'date_sent_to_sequencing_facility', 'contact_scientist', 'note')}),
    ]

    list_display = ('bpa_id', 'name', 'dna_source', 'dna_extraction_protocol', 'tumor_stage')
    search_fields = ('bpa_id__bpa_id', 'name', 'tumor_stage__description')
    list_filter = ('dna_source',
                   'gender',
                   'requested_sequence_coverage', )


class SequenceFileAdmin(admin.ModelAdmin):

    class SequenceFileForm(forms.ModelForm):

        class Meta:
            fields = "__all__"
            model = SequenceFile
            widgets = {
                'date_received_from_sequencing_facility': SuitDateWidget,
                'filename': forms.TextInput(attrs={'class': 'input-medium',
                                                   'style': 'width:50%'}),
                'md5': forms.TextInput(attrs={'class': 'input-medium',
                                              'style': 'width:50%'}),
                'sample': LinkedSelect(attrs={'class': 'input-medium',
                                              'style': 'width:40%'}),
                'run': LinkedSelect(attrs={'class': 'input-medium',
                                           'style': 'width:40%'}),
                'note': AutosizedTextarea(attrs={'class': 'input-large',
                                                 'style': 'width:95%'})
            }

    form = SequenceFileForm

    fieldsets = [
        ('Sequence File', {'fields': ('filename', 'md5', 'sample', 'run', 'lane_number', 'index_number', 'analysed',
                                      'date_received_from_sequencing_facility', 'note'), }),
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

    # Sample Name
    def get_sample_name(self, obj):
        return obj.sample.name

    get_sample_name.short_description = 'Sample Name'
    get_sample_name.admin_order_field = 'sample__name'

    search_fields = ('sample__bpa_id__bpa_id', 'sample__name')
    list_display = ('get_sample_id', 'download_field', 'get_sample_name', 'date_received_from_sequencing_facility',
                    'run')
    list_filter = ('sample__bpa_id',
                   'sample__name',
                   'date_received_from_sequencing_facility', )


class BPAProjectAdmin(admin.ModelAdmin):

    class BPAProjectForm(forms.ModelForm):

        class Meta:
            fields = ('key', 'name', 'description', 'note')
            model = BPAProject
            widgets = {'note': AutosizedTextarea(attrs={'class': 'input-large', 'style': 'width:95%'})}

    form = BPAProjectForm
    fields = ('key', 'name', 'description', 'note')
    list_display = ('key', 'name', 'description')


admin.site.register(BPAProject, BPAProjectAdmin)


class BPAUniqueIDAdmin(admin.ModelAdmin):

    class BPAIDForm(forms.ModelForm):

        class Meta:
            fields = "__all__"
            model = BPAUniqueID
            widgets = {
                'project': LinkedSelect,
                'note': AutosizedTextarea(attrs={'class': 'input-large',
                                                 'style': 'width:95%'})
            }

    form = BPAIDForm
    fields = ('bpa_id', 'project', 'note')
    list_display = ('bpa_id', 'project', 'note')
    search_fields = ('bpa_id', 'project__name', 'note')


admin.site.register(BPAUniqueID, BPAUniqueIDAdmin)


class OrganismAdmin(admin.ModelAdmin):

    class Form(forms.ModelForm):

        class Meta:
            fields = "__all__"
            model = Organism
            widgets = {'note': AutosizedTextarea(attrs={'class': 'input-large', 'style': 'width:95%'})}

    form = Form

    def get_organism_name(self, obj):
        return obj.name

    get_organism_name.short_description = 'Name'
    get_organism_name.admin_order_field = 'species'
    list_display = ('get_organism_name', 'kingdom', 'phylum', 'genus')


admin.site.register(Organism, OrganismAdmin)


class DNASourceFormAdmin(admin.ModelAdmin):

    class DNASourceForm(forms.ModelForm):

        class Meta:
            fields = "__all__"
            model = DNASource
            widgets = {
                'description': forms.TextInput(attrs={'class': 'input-large',
                                                      'style': 'width:95%'}),
                'note': AutosizedTextarea(attrs={'class': 'input-large',
                                                 'style': 'width:95%'})
            }

    form = DNASourceForm


def can_widget_clean_value(widget, value):
    try:
        widget.clean(value)
    except:
        return False
    return True


isinteger = partial(can_widget_clean_value, widgets.IntegerWidget())
isdecimal = partial(can_widget_clean_value, widgets.DecimalWidget())
istime = partial(can_widget_clean_value, widgets.TimeWidget())
isshorttime = partial(can_widget_clean_value, widgets.TimeWidget(format="%H:%M"))

admin.site.register(DNASource, DNASourceFormAdmin)
admin.site.register(Sequencer)

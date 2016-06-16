# -*- coding: utf-8 -*-

from django.contrib import admin
from import_export import resources, fields, widgets
from import_export.admin import ImportExportModelAdmin

from apps.common.admin import DateField

from ..models import CoralContextual
from ..models import SeaGrassContextual
from ..models import SeaWeedContextual
from ..models import SpongeContextual
from ..models import SedimentContextual


class CommonAdmin(ImportExportModelAdmin):
    date_hierarchy = 'date_sampled'

    list_display = ('bpa_id',
                    'date_sampled',
                    'time_sampled',
                    'site',
                    'depth', )

    list_filter = ('site__name', 'date_sampled', 'depth')


class MarineResource(resources.ModelResource):
    """ SeaWeed, Coral and SeaGrass common resource """

    bpa_id = fields.Field(attribute="bpa_id", column_name="BPA_ID")
    date_sampled = DateField(attribute="date_sampled", column_name="Date Sampled")

    time_sampled = fields.Field(widget=widgets.TimeWidget(format="%H:%M"),
                                attribute="time_sampled",
                                column_name="Time Sampled")

    lat = fields.Field(attribute="lat", column_name="Latitude")
    lon = fields.Field(attribute="lon", column_name="Longitude")
    depth = fields.Field(attribute="depth", column_name="Depth (m)")
    location_description = fields.Field(attribute="location_description", column_name="Location Description")
    note = fields.Field(attribute="note", column_name="Note")
    host_species = fields.Field(attribute="host_species", column_name="Host Species")

    class Meta:
        import_id_fields = ('bpa_id', )


class SpongeResource(MarineResource):

    host_state = fields.Field(attribute="host_state", column_name="host state (free text field)")
    host_abundance = fields.Field(attribute="host_abundance", column_name="host abundance (individuals per m2)")


class CommonResource(MarineResource):
    """ SeaWeed, Coral and SeaGrass common resource """

    pam = fields.Field(attribute="pam", column_name="Pulse amplitude modulated (PAM)")
    fluoro = fields.Field(attribute="fluoro", column_name="Fluorometer Measurement")
    host_state = fields.Field(attribute="host_state", column_name="Host State")
    host_abundance = fields.Field(attribute="host_abundance", column_name="Host Abundance")


class CoralResource(CommonResource):
    class Meta(CommonResource.Meta):
        model = CoralContextual


class SeaGrassResource(CommonResource):
    class Meta(CommonResource.Meta):
        model = SeaGrassContextual


class SpongeAdmin(CommonAdmin):
    resource_class = SpongeResource


class CoralAdmin(CommonAdmin):
    resource_class = CoralResource


class SeaWeedResource(CommonResource):
    class Meta(CommonResource.Meta):
        model = SeaWeedContextual


class SeaWeedAdmin(CommonAdmin):
    resource_class = SeaWeedResource


class SeaGrassAdmin(CommonAdmin):
    resource_class = SeaGrassResource


class SedimentResource(MarineResource):

    carbon = fields.Field(attribute="carbon", column_name="% total carbon")
    sediment = fields.Field(attribute="sediment", column_name="% fine sediment")
    nitrogen = fields.Field(attribute="nitrogen", column_name="% total nitrogen")
    phosphorous = fields.Field(attribute="phosphorous", column_name="% total phosphorous")
    sedimentation_rate = fields.Field(attribute="sedimentation_rate", column_name="sedimentation rate (g /(cm2 x y)r)")


class SedimentAdmin(CommonAdmin):
    resource_class = SedimentResource


admin.site.register(SeaWeedContextual, SeaWeedAdmin)
admin.site.register(SeaGrassContextual, SeaGrassAdmin)
admin.site.register(CoralContextual, CoralAdmin)
admin.site.register(SpongeContextual, SpongeAdmin)
admin.site.register(SedimentContextual, SedimentAdmin)

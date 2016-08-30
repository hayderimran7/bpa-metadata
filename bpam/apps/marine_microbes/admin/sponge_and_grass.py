# -*- coding: utf-8 -*-
from django.contrib import admin
from import_export import resources, fields, widgets

from apps.common.admin import BPAImportExportModelAdmin
from apps.common.admin import DateField

from ..models import CoralContextual
from ..models import MMSite
from ..models import SeaGrassContextual
from ..models import SeaWeedContextual
from ..models import SpongeContextual
from ..models import SedimentContextual

from .admin import MarineMicrobesModelResource


class CommonAdmin(BPAImportExportModelAdmin):
    date_hierarchy = 'date_sampled'

    list_display = ('bpa_id',
                    'date_sampled',
                    'time_sampled',
                    'site',
                    'depth', )

    list_filter = ('site__name', 'date_sampled', 'depth')


class MarineResource(MarineMicrobesModelResource):
    """ SeaWeed, Coral and SeaGrass common resource """

    bpa_id = fields.Field(attribute="bpa_id", column_name="BPA_ID")
    date_sampled = DateField(attribute="date_sampled", column_name="Date Sampled")

    time_sampled = fields.Field(widget=widgets.TimeWidget(format="%H:%M:%S"),
                                attribute="time_sampled",
                                column_name="Time Sampled")

    lat = fields.Field(attribute="lat", column_name="Latitude")
    lon = fields.Field(attribute="lon", column_name="Longitude")

    # ignore during import
    site = fields.Field(readonly=True,
                        attribute="site",
                        column_name="Sample Site",
                        widget=widgets.ForeignKeyWidget(MMSite, 'name'))

    depth = fields.Field(attribute="depth", column_name="Depth (m)", widget=widgets.DecimalWidget())
    location_description = fields.Field(attribute="location_description", column_name="Location Description")
    note = fields.Field(attribute="note", column_name="Note")
    host_species = fields.Field(attribute="host_species", column_name="Host Species")

    class Meta:
        import_id_fields = ('bpa_id', )

    def before_save_instance(self, instance, *args, **kwargs):
        site = MMSite.get_or_create(instance.lat, instance.lon, instance.location_description)
        instance.site = site


class SpongeResource(MarineResource):

    host_state = fields.Field(attribute="host_state", column_name="host state (free text field)")
    host_abundance = fields.Field(attribute="host_abundance", column_name="host abundance (individuals per m2)", widget=widgets.DecimalWidget())

    class Meta:
        model = SpongeContextual


class CommonResource(MarineResource):
    """ SeaWeed, Coral and SeaGrass common resource """

    pam = fields.Field(attribute="pam", column_name="Pulse amplitude modulated (PAM)", widget=widgets.DecimalWidget())
    fluoro = fields.Field(attribute="fluoro", column_name="Fluorometer Measurement", widget=widgets.DecimalWidget())
    host_state = fields.Field(attribute="host_state", column_name="Host State")
    host_abundance = fields.Field(attribute="host_abundance", column_name="Host Abundance", widget=widgets.DecimalWidget())


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

    carbon = fields.Field(attribute="carbon", column_name="% total carbon", widget=widgets.DecimalWidget())
    sediment = fields.Field(attribute="sediment", column_name="% fine sediment", widget=widgets.DecimalWidget())
    nitrogen = fields.Field(attribute="nitrogen", column_name="% total nitrogen", widget=widgets.DecimalWidget())
    phosphorous = fields.Field(attribute="phosphorous", column_name="% total phosphorous", widget=widgets.DecimalWidget())
    sedimentation_rate = fields.Field(attribute="sedimentation_rate", column_name="sedimentation rate (g /(cm2 x y)r)", widget=widgets.DecimalWidget())

    class Meta(MarineResource.Meta):
        model = SedimentContextual


class SedimentAdmin(CommonAdmin):
    resource_class = SedimentResource


admin.site.register(SeaWeedContextual, SeaWeedAdmin)
admin.site.register(SeaGrassContextual, SeaGrassAdmin)
admin.site.register(CoralContextual, CoralAdmin)
admin.site.register(SpongeContextual, SpongeAdmin)
admin.site.register(SedimentContextual, SedimentAdmin)

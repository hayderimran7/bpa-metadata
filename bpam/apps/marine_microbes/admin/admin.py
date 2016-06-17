# -*- coding: utf-8 -*-

from django.contrib import admin
from import_export import resources, fields, widgets
from import_export.admin import ImportExportModelAdmin

from apps.common.models import Site

from apps.common.admin import DateField
from apps.common.admin import CommonAmpliconResource
from apps.common.admin import CommonMetagenomicResource
from apps.common.admin import CommonMetagenomicAdmin
from apps.common.admin import CommonTransferLogResource
from apps.common.admin import CommonTransferLogAdmin
from apps.common.admin import CommonAmpliconAdmin

from ..models import Amplicon
from ..models import Metagenomic
from ..models import OpenWaterContextual
from ..models import PelagicContextual
from ..models import SampleStateTrack
from ..models import TransferLog


class TransferLogResource(CommonTransferLogResource):
    class Meta(CommonTransferLogResource.Meta):
        model = TransferLog


class TransferLogAdmin(CommonTransferLogAdmin):
    resource_class = TransferLogResource


class AmpliconResource(CommonAmpliconResource):
    class Meta(CommonAmpliconResource.Meta):
        model = Amplicon


class AmpliconAdmin(CommonAmpliconAdmin):
    resource_class = AmpliconResource


class MetagenomicResource(CommonMetagenomicResource):
    class Meta(CommonMetagenomicResource.Meta):
        model = Metagenomic


class MetagenomicAdmin(CommonMetagenomicAdmin):
    resource_class = MetagenomicResource


class SampleStateTrackAdmin(ImportExportModelAdmin):
    list_display = ('extraction_id', 'quality_check_preformed', 'metagenomics_data_generated',
                    'amplicon_16s_data_generated', 'amplicon_18s_data_generated', 'amplicon_ITS_data_generated',
                    'minimum_contextual_data_received', 'full_contextual_data_received')

    list_filter = ('quality_check_preformed', 'metagenomics_data_generated', 'amplicon_16s_data_generated',
                   'amplicon_18s_data_generated', 'amplicon_ITS_data_generated', 'minimum_contextual_data_received',
                   'full_contextual_data_received')


class CommonAdmin(ImportExportModelAdmin):
    date_hierarchy = 'date_sampled'

    list_display = ('bpa_id',
                    'date_sampled',
                    'time_sampled',
                    'site',
                    'depth', )

    list_filter = ('site__name', 'date_sampled', 'depth')


class CommonWaterResource(resources.ModelResource):

    bpa_id = fields.Field(attribute="bpa_id", column_name="BPA_ID")

    # these fields will be site-ified
    sample_site_name = fields.Field(attribute="sample_site_name", column_name="Sample Site")

    # ignore during import
    site = fields.Field(readonly=True,
                        attribute="site",
                        column_name="Sample Site",
                        widget=widgets.ForeignKeyWidget(Site, 'name'))

    lat = fields.Field(attribute="lat", column_name="Latitude")
    lon = fields.Field(attribute="lon", column_name="Longitude")
    date_sampled = DateField(attribute="date_sampled", column_name="Date Sampled")
    time_sampled = fields.Field(widget=widgets.TimeWidget(), attribute="time_sampled", column_name="Time Sampled")
    depth = fields.Field(attribute="depth", column_name="Depth")
    note = fields.Field(attribute="note", column_name="Note")

    def before_save_instance(self, instance, dry_run):
        """ set the site """

        site = Site.get_or_create(instance.lat, instance.lon, instance.sample_site_name)
        instance.site = site

    def dehydrate_lat(self, resource):
        if resource.site:
            return resource.site.get_lat()

    def dehydrate_lon(self, resource):
        if resource.site:
            return resource.site.get_lon()

    def dehydrate_sample_site_name(self, resource):
        if resource.site:
            return resource.site.name


class ContextualPelagicResource(CommonWaterResource):

    host_species = fields.Field(attribute="host_species", column_name="Host Species")
    ph = fields.Field(attribute="ph", column_name="pH Level H20")
    oxygen = fields.Field(attribute="oxygen", column_name="Oxygen (μmol/L) Lab")
    oxygen_ctd = fields.Field(attribute="oxygen_ctd", column_name="Oxygen (ml/L) CDT")
    nitrate = fields.Field(attribute="nitrate", column_name="Nitrate/Nitrite (μmol/L)")
    phosphate = fields.Field(attribute="phosphate", column_name="Phosphate (μmol/L)")
    ammonium = fields.Field(attribute="ammonium", column_name="Ammonium (μmol/L)")
    co2_total = fields.Field(attribute="co2_total", column_name="Total CO2 (μmol/kg)")
    alkalinity_total = fields.Field(attribute="alkalinity_total", column_name="Total alkalinity (μmol/kg)")
    temperature = fields.Field(attribute="temperature", column_name="Temperature [ITS-90, deg C]")
    conductivity = fields.Field(attribute="conductivity", column_name="Conductivity [S/m]")
    turbitity = fields.Field(attribute="turbitity", column_name="Turbidity (Upoly 0, WET Labs FLNTURT)")
    salinity = fields.Field(attribute="salinity", column_name="Salinity [PSU] Laboratory")
    microbial_abandance = fields.Field(attribute="microbial_abundance",
                                       column_name="Microbial abundance (cells per ml)")
    chlorophyl = fields.Field(attribute="chlorophyl", column_name="Chlorophyll a (μg/L)")
    carbon_total = fields.Field(attribute="carbon_total", column_name="% total carbon")
    inorganic_carbon_total = fields.Field(attribute="inorganic_carbon_total", column_name="% total inorganc carbon")
    flux = fields.Field(attribute="flux", column_name="Light intensity (lux)")

    class Meta:
        model = PelagicContextual
        import_id_fields = ('bpa_id', )
        export_order = ('bpa_id',
                        'sample_site_name',
                        'lat',
                        'lon',
                        'depth',
                        'date_sampled',
                        'time_sampled',
                        'note',
                        'host_species',
                        'ph',
                        'oxygen',
                        'oxygen_ctd',
                        'nitrate',
                        'phosphate',
                        'ammonium',
                        'co2_total',
                        'alkalinity_total',
                        'temperature',
                        'conductivity',
                        'turbitity',
                        'salinity',
                        'microbial_abandance',
                        'chlorophyl',
                        'carbon_total',
                        'inorganic_carbon_total',
                        'flux', )


class ContextualPelagicAdmin(CommonAdmin):
    resource_class = ContextualPelagicResource

    _required = ('bpa_id',
                 'date_sampled',
                 'time_sampled',
                 'depth',
                 'site',
                 'host_species', )

    _extra = ('ph',
              'oxygen',
              'oxygen_ctd',
              'nitrate',
              'phosphate',
              'ammonium',
              'co2_total',
              'alkalinity_total',
              'temperature',
              'conductivity',
              'turbitity',
              'salinity',
              'microbial_abandance',
              'chlorophyl',
              'carbon_total',
              'inorganic_carbon_total',
              'flux',
              'note', )

    fieldsets = ((None, {
        'fields': _required,
    }),
                 ('Detailed Contextual', {
                     'classes': ('collapse', ),
                     'fields': _extra,
                 }), )


class ContextualOpenWaterResource(CommonWaterResource):

    host_species = fields.Field(attribute="host_species", column_name="Host Species")
    ph = fields.Field(attribute="ph", column_name="pH Level H20")
    oxygen = fields.Field(attribute="oxygen", column_name="Oxygen (μmol/L) Lab")
    oxygen_ctd = fields.Field(attribute="oxygen_ctd", column_name="Oxygen (ml/L) CDT")
    nitrate = fields.Field(attribute="nitrate", column_name="Nitrate/Nitrite (μmol/L)")
    phosphate = fields.Field(attribute="phosphate", column_name="Phosphate (μmol/L)")
    ammonium = fields.Field(attribute="ammonium", column_name="Ammonium (μmol/L)")
    co2_total = fields.Field(attribute="co2_total", column_name="Total CO2 (μmol/kg)")
    alkalinity_total = fields.Field(attribute="alkalinity_total", column_name="Total alkalinity (μmol/kg)")
    temperature = fields.Field(attribute="temperature", column_name="Temperature [ITS-90, deg C]")
    conductivity = fields.Field(attribute="conductivity", column_name="Conductivity [S/m]")
    turbitity = fields.Field(attribute="turbitity", column_name="Turbidity (Upoly 0, WET Labs FLNTURT)")
    salinity = fields.Field(attribute="salinity", column_name="Salinity [PSU] Laboratory")
    salinity_cdt = fields.Field(attribute="salinity_cdt", column_name="Salinity [PSU] CTD")
    microbial_abandance = fields.Field(attribute="microbial_abundance",
                                       column_name="Microbial abundance (cells per ml)")
    chlorophyl = fields.Field(attribute="chlorophyl", column_name="Chlorophyll a (μg/L)")
    carbon_total = fields.Field(attribute="carbon_total", column_name="% total carbon")
    inorganic_carbon_total = fields.Field(attribute="inorganic_carbon_total", column_name="% total inorganc carbon")
    flux = fields.Field(attribute="flux", column_name="Light intensity (lux)")
    silicate = fields.Field(attribute="silicate", column_name="Silicate (μmol/L)")
    fluorescence = fields.Field(attribute="fluorescence", column_name="Fluorescence, Wetlab ECO-AFL/FL [mg/m^3]")
    density = fields.Field(attribute="density", column_name="Density [density, Kg/m^3]")
    tss = fields.Field(attribute="tss", column_name="TSS [mg/L]")
    inorganic_fraction = fields.Field(attribute="inorganic_fraction", column_name="Inorganic Fraction [mg/L]")
    organic_fraction = fields.Field(attribute="organic_fraction", column_name="Organic Fraction [mg/L]")
    secchi_depth = fields.Field(column_name="Secchi Depth (m)")
    biomass = fields.Field(attribute="biomass", column_name="Biomass (mg/m3)")
    allo = fields.Field(attribute="allo", column_name="ALLO [mg/m3]")
    alpha_beta_car = fields.Field(attribute="alpha_beta_car", column_name="ALPHA_BETA_CAR [mg/m3]")
    nth = fields.Field(attribute="nth", column_name="NTH [mg/m3]")
    asta = fields.Field(attribute="asta", column_name="ASTA [mg/m3]")
    beta_beta_car = fields.Field(attribute="beta_beta_car", column_name="BETA_BETA_CAR [mg/m3]")
    beta_epi_car = fields.Field(attribute="beta_epi_car", column_name="BETA_EPI_CAR [mg/m3]")
    but_fuco = fields.Field(attribute="but_fuco", column_name="BUT_FUCO [mg/m3]")
    cantha = fields.Field(attribute="cantha", column_name="CANTHA [mg/m3]")
    cphl_a = fields.Field(attribute="cphl_a", column_name="CPHL_A [mg/m3] ")
    cphl_b = fields.Field(attribute="cphl_b", column_name="CPHL_B [mg/m3]")
    cphl_c1c2 = fields.Field(attribute="cphl_c1c2", column_name="CPHL_C1C2 [mg/m3]")
    cphl_c1 = fields.Field(attribute="cphl_c1", column_name="CPHL_C1 [mg/m3]")
    cphl_c2 = fields.Field(attribute="cphl_c2", column_name="CPHL_C2 [mg/m3]")
    cphl_c3 = fields.Field(attribute="cphl_c3", column_name="CPHL_C3 [mg/m3]")
    cphlide_a = fields.Field(attribute="cphlide_a", column_name="CPHLIDE_A [mg/m3]")
    diadchr = fields.Field(attribute="diadchr", column_name="DIADCHR [mg/m3]")
    diadino = fields.Field(attribute="diadino", column_name="DIADINO [mg/m3]")
    diato = fields.Field(attribute="diato", column_name="DIATO [mg/m3]")
    dino = fields.Field(attribute="dino", column_name="DINO [mg/m3]")
    dv_cphl_a_and_cphl_a = fields.Field(attribute="dv_cphl_a_and_cphl_a", column_name="DV_CPHL_A_and_CPHL_A [mg/m3]")
    dv_cphl_a = fields.Field(attribute="dv_cphl_a", column_name="DV_CPHL_A [mg/m3]")
    dv_cphl_b_and_cphl_b = fields.Field(attribute="dv_cphl_b_and_cphl_b", column_name="DV_CPHL_B_and_CPHL_B [mg/m3]")
    dv_cphl_b = fields.Field(attribute="dv_cphl_b", column_name="DV_CPHL_B [mg/m3]")
    echin = fields.Field(attribute="echin", column_name="ECHIN [mg/m3]")
    fuco = fields.Field(attribute="fuco", column_name="FUCO [mg/m3]")
    gyro = fields.Field(attribute="gyro", column_name="GYRO [mg/m3]")
    hex_fuco = fields.Field(attribute="hex_fuco", column_name="HEX_FUCO [mg/m3]")
    keto_hex_fuco = fields.Field(attribute="keto_hex_fuco", column_name="KETO_HEX_FUCO [mg/m3]")
    lut = fields.Field(attribute="lut", column_name="LUT [mg/m3]")
    lyco = fields.Field(attribute="lyco", column_name="LYCO [mg/m3]")
    mg_dvp = fields.Field(attribute="mg_dvp", column_name="MG_DVP [mg/m3]")
    neo = fields.Field(attribute="neo", column_name="NEO [mg/m3]")
    perid = fields.Field(attribute="perid", column_name="PERID [mg/m3]")
    phide_a = fields.Field(attribute="phide_a", column_name="PHIDE_A [mg/m3]")
    phytin_a = fields.Field(attribute="phytin_a", column_name="PHYTIN_A [mg/m3]")
    phytin_b = fields.Field(attribute="phytin_b", column_name="PHYTIN_B [mg/m3]")
    pras = fields.Field(attribute="pras", column_name="PRAS [mg/m3] ")
    pyrophide_a = fields.Field(attribute="pyrophide_a", column_name="PYROPHIDE_A [mg/m3]")
    pyrophytin_a = fields.Field(attribute="pyrophytin_a", column_name="PYROPHYTIN_A [mg/m3]")
    viola = fields.Field(attribute="viola", column_name="VIOLA [mg/m3]")
    zea = fields.Field(attribute="zea", column_name="ZEA [mg/m3]")

    class Meta:
        model = OpenWaterContextual
        import_id_fields = ('bpa_id', )

        export_order = ('bpa_id',
                        'sample_site_name',
                        'lat',
                        'lon',
                        'depth',
                        'date_sampled',
                        'time_sampled',
                        'note',
                        'host_species',
                        'ph',
                        'oxygen',
                        'oxygen_ctd',
                        'silicate',
                        'nitrate',
                        'fluorescence',
                        'tss',
                        'inorganic_fraction',
                        'biomass',
                        'allo',
                        'alpha_beta_car',
                        'nth',
                        'asta',
                        'beta_beta_car',
                        'beta_epi_car',
                        'but_fuco',
                        'cantha',
                        'cphl_a',
                        'cphl_b',
                        'cphl_c1c2',
                        'cphl_c1',
                        'cphl_c2',
                        'cphl_c3',
                        'cphlide_a',
                        'diadchr',
                        'diadino',
                        'diato',
                        'dino',
                        'dv_cphl_a_and_cphl_a',
                        'dv_cphl_a',
                        'dv_cphl_b_and_cphl_b',
                        'dv_cphl_b',
                        'echin',
                        'fuco',
                        'gyro',
                        'hex_fuco',
                        'keto_hex_fuco',
                        'lut',
                        'lyco',
                        'mg_dvp',
                        'neo',
                        'perid',
                        'phide_a',
                        'phytin_a',
                        'phytin_b',
                        'pras',
                        'pyrophide_a',
                        'pyrophytin_a',
                        'viola',
                        'zea', )


class ContextualOpenWaterAdmin(CommonAdmin):
    resource_class = ContextualOpenWaterResource

    list_filter = ('site__name', 'date_sampled', 'depth')

    _required = ('bpa_id',
                 'date_sampled',
                 'time_sampled',
                 'depth',
                 'site',
                 'host_species', )

    _extra = ('ph',
              'oxygen',
              'oxygen_ctd',
              'silicate',
              'nitrate',
              'fluorescence',
              'tss',
              'inorganic_fraction',
              'biomass',
              'allo',
              'alpha_beta_car',
              'nth',
              'asta',
              'beta_beta_car',
              'beta_epi_car',
              'but_fuco',
              'cantha',
              'cphl_a',
              'cphl_b',
              'cphl_c1c2',
              'cphl_c1',
              'cphl_c2',
              'cphl_c3',
              'cphlide_a',
              'diadchr',
              'diadino',
              'diato',
              'dino',
              'dv_cphl_a_and_cphl_a',
              'dv_cphl_a',
              'dv_cphl_b_and_cphl_b',
              'dv_cphl_b',
              'echin',
              'fuco',
              'gyro',
              'hex_fuco',
              'keto_hex_fuco',
              'lut',
              'lyco',
              'mg_dvp',
              'neo',
              'perid',
              'phide_a',
              'phytin_a',
              'phytin_b',
              'pras',
              'pyrophide_a',
              'pyrophytin_a',
              'viola',
              'zea', )

    fieldsets = ((None, {
        'fields': _required,
    }),
                 ('Detailed Contextual', {
                     'classes': ('collapse', ),
                     'fields': _extra,
                 }), )


admin.site.register(Amplicon, AmpliconAdmin)
admin.site.register(Metagenomic, MetagenomicAdmin)
admin.site.register(TransferLog, TransferLogAdmin)
admin.site.register(SampleStateTrack, SampleStateTrackAdmin)
admin.site.register(PelagicContextual, ContextualPelagicAdmin)
admin.site.register(OpenWaterContextual, ContextualOpenWaterAdmin)

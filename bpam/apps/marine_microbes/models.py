# -*- coding: utf-8 -*-

from django.db import models
from apps.common.models import TransferLog
from apps.common.models import SampleSite
from apps.common.models import SequenceFile
from apps.common.models import BPAUniqueID


class MMSite(SampleSite):

    def __str__(self):
        return 'Marine Sample Site {} ({:.4f} {:.4f})'.format(self.name, self.point.x, self.point.y)


class MMSample(models.Model):
    """ A Marine Microbes Sample """

    PELAGIC = "PL"
    COASTAL_WATER = "CW"
    SEDIMENT = "SE"
    SEAGRASS = "SG"
    SEAWEED = "SW"
    CORAL = "CO"
    SPONGE = "SP"
    SAMPLE_CHOICES = (
        (PELAGIC, "Pelagic/Open Water"),
        (COASTAL_WATER, "Coastal Water"),
        (SEDIMENT, "Sediment"),
        (SEAGRASS, "Seagrass"),
        (SEAWEED, "Seaweed"),
        (CORAL, "Coral"),
        (SPONGE, "Sponge"),
    )

    bpa_id = models.OneToOneField(BPAUniqueID,
                                  verbose_name="BPA ID",
                                  primary_key=True,
                                  help_text="Bioplatforms Australia Sample ID")
    sample_type = models.CharField("Sample Type", choices=SAMPLE_CHOICES, max_length=2, null=True, blank=True)
    site = models.ForeignKey(MMSite, null=True)
    depth = models.DecimalField("Depth", null=True, blank=True, max_digits=12, decimal_places=2)
    collection_date = models.DateTimeField("Sample Collection Date", null=True, blank=True)

    def __unicode__(self):
        return "Marine Microbes sample {}".format(self.bpa_id)

    class Meta:
        verbose_name = "Marine Microbes Sample"


class AmpliconSequenceFile(SequenceFile):
    CHOICES = (
        ("16S", "16S"),
        ("ITS", "ITS"),
        ("18S", "18S"),
        ("A16S", "A16S")
    )

    PASS_OR_FAIL = (('P', 'Pass'), ('F', 'Fail'))
    DILUTIONS = (('1:10', '1:10'), ('1:100', '1:100'), ('NEAT', 'Neat'))

    sample = models.ForeignKey(MMSample, null=True)
    extraction = models.IntegerField("Sample Extraction ID", blank=True, null=True)
    amplicon = models.CharField("Amplicon", max_length=4, choices=CHOICES)
    vendor = models.CharField("Vendor", max_length=100, default="UNKNOWN")
    index = models.CharField("Index", max_length=50, blank=True, null=True)
    flow_cell = models.CharField("Flow Cell", max_length=9, blank=True, null=True)
    runsamplenum = models.CharField("Run Sample Number", max_length=9, blank=True, null=True)
    read = models.CharField("Read", max_length=2, blank=True, null=True)

    pcr_1_to_10 = models.CharField('PCR 1:10', max_length=1, blank=True, null=True, choices=PASS_OR_FAIL)
    pcr_1_to_100 = models.CharField('PCR 1:100', max_length=1, blank=True, null=True, choices=PASS_OR_FAIL)
    pcr_neat = models.CharField('Neat PCR', max_length=1, blank=True, null=True, choices=PASS_OR_FAIL)
    dilution = models.CharField('Dilution Used', max_length=5, blank=True, null=True, choices=DILUTIONS)

    number_of_reads = models.IntegerField("Number of Reads", blank=True, null=True)
    analysis_software_version = models.CharField('Analysis Software Version', max_length=100, blank=True, null=True)

    def passed_pcr_1_to_10(self):
        return self.pcr_1_to_10 == 'P'

    def passed_pcr_1_to_100(self):
        return self.pcr_1_to_100 == 'P'

    def passed_pcr_neat(self):
        return self.pcr_neat == 'P'

    def __unicode__(self):
        return u"{0}:{1}".format(self.sample, self.amplicon)

    def get_path_parts(self):
        return ('marine_microbes', 'amplicons/{}'.format(self.amplicon).lower())

    class Meta:
        verbose_name_plural = "Amplicon Sequence Files"


class MetagenomicSequenceFile(SequenceFile):
    """ Metagenomics """

    project_name = 'marine_microbes'
    extraction = models.IntegerField("Extraction", default=1)
    vendor = models.CharField("Vendor", max_length=100, default="UNKNOWN")
    sample = models.ForeignKey(MMSample, null=True)
    library = models.CharField("Library", max_length=20, help_text="MP or PE")
    size = models.CharField("Extraction Size", max_length=100, default=1)
    flow_cell = models.CharField("Flow Cell", max_length=9, blank=True, null=True)
    index = models.CharField("Index", max_length=20, blank=True, null=True)
    read = models.CharField("Read", max_length=3, blank=True, null=True)

    def get_path_parts(self):
        return ('marine_microbes', 'metagenomics')

    class Meta:
        verbose_name_plural = "Metagenomics Sequence Files"


class TransferLog(TransferLog):
    pass


class MarineCommonContextual(models.Model):
    """ Marine Common """

    sample_type = "UNSET"
    #  BPA_ID
    bpa_id = models.IntegerField('BPA ID', primary_key=True)
    #  Date sampled (Y-M-D)
    date_sampled = models.DateField("Date Sampled", null=True, blank=True)
    #  Time sampled (hh:mm)
    time_sampled = models.TimeField("Time Sampled", null=True, blank=True)
    #  Depth (m)
    depth = models.DecimalField('Depth (m)', null=True, blank=True, max_digits=12, decimal_places=2)
    #  Notes
    note = models.TextField("Note", null=True, blank=True)
    #  Sample site
    site = models.ForeignKey(MMSite, on_delete=models.SET_NULL, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return "{} {}".format(self.bpa_id, self.sample_type)


class SampleStateTrack(models.Model):
    extraction_id = models.CharField('Sample Extraction ID', max_length=100, primary_key=True)
    quality_check_preformed = models.BooleanField("Quality Checked", default=False)
    metagenomics_data_generated = models.BooleanField("Metagenomics Data Generated", default=False)
    amplicon_16s_data_generated = models.BooleanField("Amplicon 16S Data Generated", default=False)
    amplicon_18s_data_generated = models.BooleanField("Amplicon 18S Data Generated", default=False)
    amplicon_ITS_data_generated = models.BooleanField("Amplicon ITS Data Generated", default=False)
    minimum_contextual_data_received = models.BooleanField("Minimum Contextual Data Received", default=False)
    full_contextual_data_received = models.BooleanField("Full Contextual Data Received", default=False)

    class Meta:
        verbose_name = 'Sample State Track Log'

    def __str__(self):
        return "{}".format(self.extraction_id)


class OpenWaterContextual(MarineCommonContextual):
    sample_type = "Pelagic/Open Water"
    # Host Species
    host_species = models.TextField("Host Species", null=True, blank=True)
    # pH Level (H2O) (pH)
    ph = models.IntegerField("pH Level H20", null=True, blank=True)
    # Oxygen (μmol/L) Lab
    oxygen = models.IntegerField("Oxygen (μmol/L) Lab", null=True, blank=True)
    # Oxygen (ml/L) CTD
    oxygen_ctd = models.IntegerField("Oxygen (ml/L) CDT", null=True, blank=True)
    #  Silicate (μmol/L)
    silicate = models.IntegerField("Silicate (μmol/L)", null=True, blank=True)
    # Nitrate/Nitrite (μmol/L)
    nitrate = models.IntegerField("Nitrate/Nitrite (μmol/L)", null=True, blank=True)
    # Phosphate (μmol/L)
    phosphate = models.IntegerField("Phosphate (μmol/L)", null=True, blank=True)
    # Ammonium (μmol/L)
    ammonium = models.IntegerField("Ammonium (μmol/L)", null=True, blank=True)
    # Total CO2 (μmol/kg)
    co2_total = models.IntegerField("Total CO2 (μmol/kg)", null=True, blank=True)
    # Total alkalinity (μmol/kg)
    alkalinity_total = models.IntegerField("Total alkalinity (μmol/kg)", null=True, blank=True)
    # Temperature [ITS-90, deg C]
    temperature = models.IntegerField("Temperature [ITS-90, deg C]", null=True, blank=True)
    # Conductivity [S/m]
    conductivity = models.IntegerField("Conductivity [S/m]", null=True, blank=True)
    #  Fluorescence, Wetlab ECO-AFL/FL [mg/m^3]
    fluorescence = models.IntegerField("Fluorescence, Wetlab ECO-AFL/FL [mg/m^3]", null=True, blank=True)
    # Turbidity (Upoly 0, WET Labs FLNTURT)
    turbitity = models.IntegerField("Turbidity (Upoly 0, WET Labs FLNTURT)", null=True, blank=True)
    # Salinity [PSU] CTD
    salinity = models.IntegerField("Salinity [PSU] CTD", null=True, blank=True)
    #  Density [density, Kg/m^3]
    density = models.IntegerField("Density [density, Kg/m^3]", null=True, blank=True)
    #  TSS [mg/L]
    tss = models.IntegerField("TSS [mg/L]", null=True, blank=True)
    #  Inorganic Fraction [mg/L]
    inorganic_fraction = models.IntegerField("Inorganic Fraction [mg/L]", null=True, blank=True)
    #  Organic Fraction [mg/L]
    organic_fraction = models.IntegerField("Organic Fraction [mg/L]", null=True, blank=True)
    #  Secchi Depth (m)
    secchi_depth = models.DecimalField("Secchi Depth (m)", null=True, blank=True, max_digits=12, decimal_places=2)
    #  Biomass (mg/m3)
    biomass = models.IntegerField("Biomass (mg/m3)", null=True, blank=True)
    #  ALLO [mg/m3]
    allo = models.IntegerField("ALLO [mg/m3]", null=True, blank=True)
    #  ALPHA_BETA_CAR [mg/m3]
    alpha_beta_car = models.IntegerField("ALPHA_BETA_CAR [mg/m3]", null=True, blank=True)

    # NTH [mg/m3]
    nth = models.IntegerField("NTH [mg/m3]", null=True, blank=True)
    # ASTA [mg/m3]
    asta = models.IntegerField("ASTA [mg/m3]", null=True, blank=True)
    # BETA_BETA_CAR [mg/m3]
    beta_beta_car = models.IntegerField("BETA_BETA_CAR [mg/m3]", null=True, blank=True)
    # BETA_EPI_CAR [mg/m3]
    beta_epi_car = models.IntegerField("BETA_EPI_CAR [mg/m3]", null=True, blank=True)
    # BUT_FUCO [mg/m3]
    but_fuco = models.IntegerField("BUT_FUCO [mg/m3]", null=True, blank=True)
    # CANTHA [mg/m3]
    cantha = models.IntegerField("CANTHA [mg/m3]", null=True, blank=True)
    # CPHL_A [mg/m3]
    cphl_a = models.IntegerField("CPHL_A [mg/m3] ", null=True, blank=True)
    # CPHL_B [mg/m3]
    cphl_b = models.IntegerField("CPHL_B [mg/m3]", null=True, blank=True)
    # CPHL_C1C2 [mg/m3]
    cphl_c1c2 = models.IntegerField("CPHL_C1C2 [mg/m3]", null=True, blank=True)
    # CPHL_C1 [mg/m3]
    cphl_c1 = models.IntegerField("CPHL_C1 [mg/m3]", null=True, blank=True)
    # CPHL_C2 [mg/m3]
    cphl_c2 = models.IntegerField("CPHL_C2 [mg/m3]", null=True, blank=True)
    # CPHL_C3 [mg/m3]
    cphl_c3 = models.IntegerField("CPHL_C3 [mg/m3]", null=True, blank=True)
    # CPHLIDE_A [mg/m3]
    cphlide_a = models.IntegerField("CPHLIDE_A [mg/m3]", null=True, blank=True)
    # DIADCHR [mg/m3]
    diadchr = models.IntegerField("DIADCHR [mg/m3]", null=True, blank=True)
    # DIADINO [mg/m3]
    diadino = models.IntegerField("DIADINO [mg/m3]", null=True, blank=True)
    # DIATO [mg/m3]
    diato = models.IntegerField("DIATO [mg/m3]", null=True, blank=True)
    # DINO [mg/m3]
    dino = models.IntegerField("DINO [mg/m3]", null=True, blank=True)
    # DV_CPHL_A_and_CPHL_A [mg/m3]
    dv_cphl_a_and_cphl_a = models.IntegerField("DV_CPHL_A_and_CPHL_A [mg/m3]", null=True, blank=True)
    # DV_CPHL_A [mg/m3]
    dv_cphl_a = models.IntegerField("DV_CPHL_A [mg/m3]", null=True, blank=True)
    # DV_CPHL_B_and_CPHL_B [mg/m3]
    dv_cphl_b_and_cphl_b = models.IntegerField("DV_CPHL_B_and_CPHL_B [mg/m3]", null=True, blank=True)
    # DV_CPHL_B [mg/m3]
    dv_cphl_b = models.IntegerField("DV_CPHL_B [mg/m3]", null=True, blank=True)
    # ECHIN [mg/m3]
    echin = models.IntegerField("ECHIN [mg/m3]", null=True, blank=True)
    # FUCO [mg/m3]
    fuco = models.IntegerField("FUCO [mg/m3]", null=True, blank=True)
    # GYRO [mg/m3]
    gyro = models.IntegerField("GYRO [mg/m3]", null=True, blank=True)
    # HEX_FUCO [mg/m3]
    hex_fuco = models.IntegerField("HEX_FUCO [mg/m3]", null=True, blank=True)
    # KETO_HEX_FUCO [mg/m3]
    keto_hex_fuco = models.IntegerField("KETO_HEX_FUCO [mg/m3]", null=True, blank=True)
    # LUT [mg/m3]
    lut = models.IntegerField("LUT [mg/m3]", null=True, blank=True)
    # LYCO [mg/m3]
    lyco = models.IntegerField("LYCO [mg/m3]", null=True, blank=True)
    # MG_DVP [mg/m3]
    mg_dvp = models.IntegerField("MG_DVP [mg/m3]", null=True, blank=True)
    # NEO [mg/m3]
    neo = models.IntegerField("NEO [mg/m3]", null=True, blank=True)
    # PERID [mg/m3]
    perid = models.IntegerField("PERID [mg/m3]", null=True, blank=True)
    # PHIDE_A [mg/m3]
    phide_a = models.IntegerField("PHIDE_A [mg/m3]", null=True, blank=True)
    # PHYTIN_A [mg/m3]
    phytin_a = models.IntegerField("PHYTIN_A [mg/m3]", null=True, blank=True)
    # PHYTIN_B [mg/m3]
    phytin_b = models.IntegerField("PHYTIN_B [mg/m3]", null=True, blank=True)
    # PRAS [mg/m3]
    pras = models.IntegerField("PRAS [mg/m3] ", null=True, blank=True)
    # PYROPHIDE_A [mg/m3]
    pyrophide_a = models.IntegerField("PYROPHIDE_A [mg/m3]", null=True, blank=True)
    # PYROPHYTIN_A [mg/m3]
    pyrophytin_a = models.IntegerField("PYROPHYTIN_A [mg/m3]", null=True, blank=True)
    # VIOLA [mg/m3]
    viola = models.IntegerField("VIOLA [mg/m3]", null=True, blank=True)
    # ZEA [mg/m3]
    zea = models.IntegerField("ZEA [mg/m3]", null=True, blank=True)

    class Meta:
        verbose_name = 'Open Water Contextual Data'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{} Open Water Data".format(self.bpa_id)


class CoastalContextual(MarineCommonContextual):
    """ Coastal sample contextual data"""

    sample_type = "Coastal"

    # Host Species
    host_species = models.TextField("Host Species", null=True, blank=True)
    # pH Level (H2O) (pH)
    ph = models.IntegerField("pH Level H20", null=True, blank=True)
    # Oxygen (μmol/L) Lab
    oxygen = models.IntegerField("Oxygen (μmol/L) Lab", null=True, blank=True)
    # Oxygen (ml/L) CTD
    oxygen_ctd = models.IntegerField("Oxygen (ml/L) CDT", null=True, blank=True)
    # Nitrate/Nitrite (μmol/L)
    nitrate = models.IntegerField("Nitrate/Nitrite (μmol/L)", null=True, blank=True)
    # Phosphate (μmol/L)
    phosphate = models.IntegerField("Phosphate (μmol/L)", null=True, blank=True)
    # Ammonium (μmol/L)
    ammonium = models.IntegerField("Ammonium (μmol/L)", null=True, blank=True)
    # Total CO2 (μmol/kg)
    co2_total = models.IntegerField("Total CO2 (μmol/kg)", null=True, blank=True)
    # Total alkalinity (μmol/kg)
    alkalinity_total = models.IntegerField("Total alkalinity (μmol/kg)", null=True, blank=True)
    # Temperature [ITS-90, deg C]
    temperature = models.IntegerField("Temperature [ITS-90, deg C]", null=True, blank=True)
    # Conductivity [S/m]
    conductivity = models.IntegerField("Conductivity [S/m]", null=True, blank=True)
    # Turbidity (Upoly 0, WET Labs FLNTURT)
    turbitity = models.IntegerField("Turbidity (Upoly 0, WET Labs FLNTURT)", null=True, blank=True)
    # Salinity [PSU] Laboratory
    salinity = models.IntegerField("Salinity [PSU] Laboratory", null=True, blank=True)
    # microbial abundance (cells per ml)
    microbial_abandance = models.IntegerField("Microbial abundance (cells per ml)", null=True, blank=True)
    # chlorophyll a (μg/L)
    chlorophyl = models.IntegerField("Chlorophyll a (μg/L)", null=True, blank=True)
    # %total carbon
    carbon_total = models.IntegerField("% total carbon", null=True, blank=True)
    # % total inorganc carbon
    inorganic_carbon_total = models.IntegerField("% total inorganc carbon", null=True, blank=True)
    # light intensity (lux)
    flux = models.IntegerField("Light intensity (lux)", null=True, blank=True)

    class Meta:
        verbose_name = 'Coastal Water Contextual Data'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{} Coastal Water Contextual Data".format(self.bpa_id)


class CoralWeedGrassCommonContextual(MarineCommonContextual):

    #  Pulse amplitude modulated (PAM)
    pam = models.DecimalField("Pulse amplitude modulated (PAM)", null=True, blank=True, max_digits=9, decimal_places=6)
    #  fluorometer measurement
    fluoro = models.DecimalField("Fluorometer Measurement", null=True, blank=True, max_digits=9, decimal_places=6)
    #  host state (free text field)
    host_state = models.TextField("Host State")
    #  host abundance (individuals per m2)
    host_abundance = models.DecimalField("Host Abundance", null=True, blank=True, max_digits=9, decimal_places=6)

    class Meta(MarineCommonContextual.Meta):
        abstract = True


class SeaWeedContextual(CoralWeedGrassCommonContextual):
    """ Seaweed """
    sample_type = "SeaWeed"

    class Meta(CoralWeedGrassCommonContextual.Meta):
        verbose_name = "Seaweed Contextual Data"
        verbose_name_plural = verbose_name


class SeaGrassContextual(CoralWeedGrassCommonContextual):
    """ SeaGrass """
    sample_type = "SeaGrass"

    class Meta(CoralWeedGrassCommonContextual.Meta):
        verbose_name = "Seagrass Contextual Data"
        verbose_name_plural = verbose_name


class CoralContextual(CoralWeedGrassCommonContextual):
    """ Coral"""
    sample_type = "Coral"

    class Meta(CoralWeedGrassCommonContextual.Meta):
        verbose_name = "Coral Contextual Data"
        verbose_name_plural = verbose_name


class SedimentContextual(MarineCommonContextual):
    sample_type = "Sediment"

    #  Host Species (Coastal samples only)
    host_species = models.TextField("Host Species", null=True, blank=True)
    #  %total carbon
    carbon = models.DecimalField("% total carbon", max_digits=5, decimal_places=2, null=True, blank=True)
    #  % fine sediment
    sediment = models.DecimalField("% fine sediment", max_digits=5, decimal_places=2, null=True, blank=True)
    #  % total nitrogen
    nitrogen = models.DecimalField("% total nitrogen", max_digits=5, decimal_places=2, null=True, blank=True)
    #  % total phosphorous
    phosphorous = models.DecimalField("% total phosphorous", max_digits=5, decimal_places=2, null=True, blank=True)
    #  sedimentation rate (g /(cm2 x y)r)
    sedimentation_rate = models.DecimalField("sedimentation rate (g /(cm2 x y)r)",
                                             max_digits=5,
                                             decimal_places=2,
                                             null=True,
                                             blank=True)

    class Meta(CoralWeedGrassCommonContextual.Meta):
        verbose_name = "Sediment Contextual Data"
        verbose_name_plural = verbose_name


class SpongeContextual(MarineCommonContextual):
    sample_type = "Sponge"

    #  host state (free text field)
    host_state = models.TextField("Host State")
    #  host abundance (individuals per m2)
    host_abundance = models.DecimalField("Host Abundance", null=True, blank=True, max_digits=9, decimal_places=6)

    class Meta(MarineCommonContextual.Meta):
        verbose_name = "Sponge Contextual Data"
        verbose_name_plural = verbose_name

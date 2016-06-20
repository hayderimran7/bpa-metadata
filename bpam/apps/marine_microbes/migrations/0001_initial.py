# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0007_site'),
    ]

    operations = [
        migrations.CreateModel(
            name='Amplicon',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('extraction_id', models.CharField(max_length=100, null=True, verbose_name=b'Sample Extraction ID', blank=True)),
                ('target', models.CharField(max_length=4, verbose_name=b'Type', choices=[(b'16S', b'16S'), (b'ITS', b'ITS'), (b'18S', b'18S'), (b'A16S', b'A16S')])),
                ('metadata_filename', models.CharField(max_length=100, verbose_name=b'Metadata Filename')),
                ('comments', models.TextField(null=True, verbose_name=b'Comments', blank=True)),
                ('facility', models.ForeignKey(related_name='marine_microbes_amplicon_facility', verbose_name=b'Sequencing Facility', blank=True, to='common.Facility', null=True)),
            ],
            options={
                'abstract': False,
                'verbose_name_plural': 'Amplicon Sequences',
            },
        ),
        migrations.CreateModel(
            name='ContextualOpenWater',
            fields=[
                ('bpa_id', models.IntegerField(serialize=False, verbose_name=b'BPA ID', primary_key=True)),
                ('date_sampled', models.DateField(null=True, verbose_name=b'Date Sampled', blank=True)),
                ('time_sampled', models.TimeField(null=True, verbose_name=b'Time Sampled', blank=True)),
                ('depth', models.IntegerField(null=True, verbose_name=b'Depth (m)', blank=True)),
                ('note', models.TextField(null=True, verbose_name=b'Note', blank=True)),
                ('host_species', models.TextField(null=True, verbose_name=b'Host Species', blank=True)),
                ('ph', models.IntegerField(null=True, verbose_name=b'pH Level H20', blank=True)),
                ('oxygen', models.IntegerField(null=True, verbose_name=b'Oxygen (\xce\xbcmol/L) Lab', blank=True)),
                ('oxygen_ctd', models.IntegerField(null=True, verbose_name=b'Oxygen (ml/L) CDT', blank=True)),
                ('silicate', models.IntegerField(null=True, verbose_name=b'Silicate (\xce\xbcmol/L)', blank=True)),
                ('nitrate', models.IntegerField(null=True, verbose_name=b'Nitrate/Nitrite (\xce\xbcmol/L)', blank=True)),
                ('phosphate', models.IntegerField(null=True, verbose_name=b'Phosphate (\xce\xbcmol/L)', blank=True)),
                ('ammonium', models.IntegerField(null=True, verbose_name=b'Ammonium (\xce\xbcmol/L)', blank=True)),
                ('co2_total', models.IntegerField(null=True, verbose_name=b'Total CO2 (\xce\xbcmol/kg)', blank=True)),
                ('alkalinity_total', models.IntegerField(null=True, verbose_name=b'Total alkalinity (\xce\xbcmol/kg)', blank=True)),
                ('temperature', models.IntegerField(null=True, verbose_name=b'Temperature [ITS-90, deg C]', blank=True)),
                ('conductivity', models.IntegerField(null=True, verbose_name=b'Conductivity [S/m]', blank=True)),
                ('fluorescence', models.IntegerField(null=True, verbose_name=b'Fluorescence, Wetlab ECO-AFL/FL [mg/m^3]', blank=True)),
                ('turbitity', models.IntegerField(null=True, verbose_name=b'Turbidity (Upoly 0, WET Labs FLNTURT)', blank=True)),
                ('salinity', models.IntegerField(null=True, verbose_name=b'Salinity [PSU] CTD', blank=True)),
                ('density', models.IntegerField(null=True, verbose_name=b'Density [density, Kg/m^3]', blank=True)),
                ('tss', models.IntegerField(null=True, verbose_name=b'TSS [mg/L]', blank=True)),
                ('inorganic_fraction', models.IntegerField(null=True, verbose_name=b'Inorganic Fraction [mg/L]', blank=True)),
                ('organic_fraction', models.IntegerField(null=True, verbose_name=b'Organic Fraction [mg/L]', blank=True)),
                ('secchi_depth', models.IntegerField(null=True, verbose_name=b'Secchi Depth (m)', blank=True)),
                ('biomass', models.IntegerField(null=True, verbose_name=b'Biomass (mg/m3)', blank=True)),
                ('allo', models.IntegerField(null=True, verbose_name=b'ALLO [mg/m3]', blank=True)),
                ('alpha_beta_car', models.IntegerField(null=True, verbose_name=b'ALPHA_BETA_CAR [mg/m3]', blank=True)),
                ('nth', models.IntegerField(null=True, verbose_name=b'NTH [mg/m3]', blank=True)),
                ('asta', models.IntegerField(null=True, verbose_name=b'ASTA [mg/m3]', blank=True)),
                ('beta_beta_car', models.IntegerField(null=True, verbose_name=b'BETA_BETA_CAR [mg/m3]', blank=True)),
                ('beta_epi_car', models.IntegerField(null=True, verbose_name=b'BETA_EPI_CAR [mg/m3]', blank=True)),
                ('but_fuco', models.IntegerField(null=True, verbose_name=b'BUT_FUCO [mg/m3]', blank=True)),
                ('cantha', models.IntegerField(null=True, verbose_name=b'CANTHA [mg/m3]', blank=True)),
                ('cphl_a', models.IntegerField(null=True, verbose_name=b'CPHL_A [mg/m3] ', blank=True)),
                ('cphl_b', models.IntegerField(null=True, verbose_name=b'CPHL_B [mg/m3]', blank=True)),
                ('cphl_c1c2', models.IntegerField(null=True, verbose_name=b'CPHL_C1C2 [mg/m3]', blank=True)),
                ('cphl_c1', models.IntegerField(null=True, verbose_name=b'CPHL_C1 [mg/m3]', blank=True)),
                ('cphl_c2', models.IntegerField(null=True, verbose_name=b'CPHL_C2 [mg/m3]', blank=True)),
                ('cphl_c3', models.IntegerField(null=True, verbose_name=b'CPHL_C3 [mg/m3]', blank=True)),
                ('cphlide_a', models.IntegerField(null=True, verbose_name=b'CPHLIDE_A [mg/m3]', blank=True)),
                ('diadchr', models.IntegerField(null=True, verbose_name=b'DIADCHR [mg/m3]', blank=True)),
                ('diadino', models.IntegerField(null=True, verbose_name=b'DIADINO [mg/m3]', blank=True)),
                ('diato', models.IntegerField(null=True, verbose_name=b'DIATO [mg/m3]', blank=True)),
                ('dino', models.IntegerField(null=True, verbose_name=b'DINO [mg/m3]', blank=True)),
                ('dv_cphl_a_and_cphl_a', models.IntegerField(null=True, verbose_name=b'DV_CPHL_A_and_CPHL_A [mg/m3]', blank=True)),
                ('dv_cphl_a', models.IntegerField(null=True, verbose_name=b'DV_CPHL_A [mg/m3]', blank=True)),
                ('dv_cphl_b_and_cphl_b', models.IntegerField(null=True, verbose_name=b'DV_CPHL_B_and_CPHL_B [mg/m3]', blank=True)),
                ('dv_cphl_b', models.IntegerField(null=True, verbose_name=b'DV_CPHL_B [mg/m3]', blank=True)),
                ('echin', models.IntegerField(null=True, verbose_name=b'ECHIN [mg/m3]', blank=True)),
                ('fuco', models.IntegerField(null=True, verbose_name=b'FUCO [mg/m3]', blank=True)),
                ('gyro', models.IntegerField(null=True, verbose_name=b'GYRO [mg/m3]', blank=True)),
                ('hex_fuco', models.IntegerField(null=True, verbose_name=b'HEX_FUCO [mg/m3]', blank=True)),
                ('keto_hex_fuco', models.IntegerField(null=True, verbose_name=b'KETO_HEX_FUCO [mg/m3]', blank=True)),
                ('lut', models.IntegerField(null=True, verbose_name=b'LUT [mg/m3]', blank=True)),
                ('lyco', models.IntegerField(null=True, verbose_name=b'LYCO [mg/m3]', blank=True)),
                ('mg_dvp', models.IntegerField(null=True, verbose_name=b'MG_DVP [mg/m3]', blank=True)),
                ('neo', models.IntegerField(null=True, verbose_name=b'NEO [mg/m3]', blank=True)),
                ('perid', models.IntegerField(null=True, verbose_name=b'PERID [mg/m3]', blank=True)),
                ('phide_a', models.IntegerField(null=True, verbose_name=b'PHIDE_A [mg/m3]', blank=True)),
                ('phytin_a', models.IntegerField(null=True, verbose_name=b'PHYTIN_A [mg/m3]', blank=True)),
                ('phytin_b', models.IntegerField(null=True, verbose_name=b'PHYTIN_B [mg/m3]', blank=True)),
                ('pras', models.IntegerField(null=True, verbose_name=b'PRAS [mg/m3] ', blank=True)),
                ('pyrophide_a', models.IntegerField(null=True, verbose_name=b'PYROPHIDE_A [mg/m3]', blank=True)),
                ('pyrophytin_a', models.IntegerField(null=True, verbose_name=b'PYROPHYTIN_A [mg/m3]', blank=True)),
                ('viola', models.IntegerField(null=True, verbose_name=b'VIOLA [mg/m3]', blank=True)),
                ('zea', models.IntegerField(null=True, verbose_name=b'ZEA [mg/m3]', blank=True)),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='common.Site', null=True)),
            ],
            options={
                'verbose_name': 'Open Water Contextual Data',
                'verbose_name_plural': 'Open Water Contextual Data',
            },
        ),
        migrations.CreateModel(
            name='ContextualPelagic',
            fields=[
                ('bpa_id', models.IntegerField(serialize=False, verbose_name=b'BPA ID', primary_key=True)),
                ('date_sampled', models.DateField(null=True, verbose_name=b'Date Sampled', blank=True)),
                ('time_sampled', models.TimeField(null=True, verbose_name=b'Time Sampled', blank=True)),
                ('depth', models.IntegerField(null=True, verbose_name=b'Depth (m)', blank=True)),
                ('note', models.TextField(null=True, verbose_name=b'Note', blank=True)),
                ('host_species', models.TextField(null=True, verbose_name=b'Host Species', blank=True)),
                ('ph', models.IntegerField(null=True, verbose_name=b'pH Level H20', blank=True)),
                ('oxygen', models.IntegerField(null=True, verbose_name=b'Oxygen (\xce\xbcmol/L) Lab', blank=True)),
                ('oxygen_ctd', models.IntegerField(null=True, verbose_name=b'Oxygen (ml/L) CDT', blank=True)),
                ('nitrate', models.IntegerField(null=True, verbose_name=b'Nitrate/Nitrite (\xce\xbcmol/L)', blank=True)),
                ('phosphate', models.IntegerField(null=True, verbose_name=b'Phosphate (\xce\xbcmol/L)', blank=True)),
                ('ammonium', models.IntegerField(null=True, verbose_name=b'Ammonium (\xce\xbcmol/L)', blank=True)),
                ('co2_total', models.IntegerField(null=True, verbose_name=b'Total CO2 (\xce\xbcmol/kg)', blank=True)),
                ('alkalinity_total', models.IntegerField(null=True, verbose_name=b'Total alkalinity (\xce\xbcmol/kg)', blank=True)),
                ('temperature', models.IntegerField(null=True, verbose_name=b'Temperature [ITS-90, deg C]', blank=True)),
                ('conductivity', models.IntegerField(null=True, verbose_name=b'Conductivity [S/m]', blank=True)),
                ('turbitity', models.IntegerField(null=True, verbose_name=b'Turbidity (Upoly 0, WET Labs FLNTURT)', blank=True)),
                ('salinity', models.IntegerField(null=True, verbose_name=b'Salinity [PSU] Laboratory', blank=True)),
                ('microbial_abandance', models.IntegerField(null=True, verbose_name=b'Microbial abundance (cells per ml)', blank=True)),
                ('chlorophyl', models.IntegerField(null=True, verbose_name=b'Chlorophyll a (\xce\xbcg/L)', blank=True)),
                ('carbon_total', models.IntegerField(null=True, verbose_name=b'% total carbon', blank=True)),
                ('inorganic_carbon_total', models.IntegerField(null=True, verbose_name=b'% total inorganc carbon', blank=True)),
                ('flux', models.IntegerField(null=True, verbose_name=b'Light intensity (lux)', blank=True)),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='common.Site', null=True)),
            ],
            options={
                'verbose_name': 'Pelagic Contextual Data',
                'verbose_name_plural': 'Pelagic Contextual Data',
            },
        ),
        migrations.CreateModel(
            name='CoralContextual',
            fields=[
                ('bpa_id', models.IntegerField(serialize=False, verbose_name=b'BPA ID', primary_key=True)),
                ('date_sampled', models.DateField(null=True, verbose_name=b'Date Sampled', blank=True)),
                ('time_sampled', models.TimeField(null=True, verbose_name=b'Time Sampled', blank=True)),
                ('depth', models.IntegerField(null=True, verbose_name=b'Depth (m)', blank=True)),
                ('note', models.TextField(null=True, verbose_name=b'Note', blank=True)),
                ('pam', models.DecimalField(verbose_name=b'Pulse amplitude modulated (PAM)', max_digits=9, decimal_places=6)),
                ('fluoro', models.DecimalField(verbose_name=b'Fluorometer Measurement', max_digits=9, decimal_places=6)),
                ('host_state', models.TextField(verbose_name=b'Host State')),
                ('host_abundance', models.DecimalField(verbose_name=b'Host Abundance', max_digits=9, decimal_places=6)),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='common.Site', null=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Coral Contextual Data',
                'verbose_name_plural': 'Coral Contextual Data',
            },
        ),
        migrations.CreateModel(
            name='Metagenomic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('extraction_id', models.CharField(max_length=100, null=True, verbose_name=b'Sample Extraction ID', blank=True)),
                ('metadata_filename', models.CharField(max_length=100, verbose_name=b'Metadata Filename')),
                ('comments', models.TextField(null=True, verbose_name=b'Comments', blank=True)),
                ('facility', models.ForeignKey(related_name='marine_microbes_metagenomic_facility', verbose_name=b'Sequencing Facility', blank=True, to='common.Facility', null=True)),
            ],
            options={
                'abstract': False,
                'verbose_name_plural': 'Metagenomic Sequences',
            },
        ),
        migrations.CreateModel(
            name='SampleStateTrack',
            fields=[
                ('extraction_id', models.CharField(max_length=100, serialize=False, verbose_name=b'Sample Extraction ID', primary_key=True)),
                ('quality_check_preformed', models.BooleanField(default=False, verbose_name=b'Quality Checked')),
                ('metagenomics_data_generated', models.BooleanField(default=False, verbose_name=b'Metagenomics Data Generated')),
                ('amplicon_16s_data_generated', models.BooleanField(default=False, verbose_name=b'Amplicon 16S Data Generated')),
                ('amplicon_18s_data_generated', models.BooleanField(default=False, verbose_name=b'Amplicon 18S Data Generated')),
                ('amplicon_ITS_data_generated', models.BooleanField(default=False, verbose_name=b'Amplicon ITS Data Generated')),
                ('minimum_contextual_data_received', models.BooleanField(default=False, verbose_name=b'Minimum Contextual Data Received')),
                ('full_contextual_data_received', models.BooleanField(default=False, verbose_name=b'Full Contextual Data Received')),
            ],
            options={
                'verbose_name': 'Sample State Track Log',
            },
        ),
        migrations.CreateModel(
            name='SeaGrassContextual',
            fields=[
                ('bpa_id', models.IntegerField(serialize=False, verbose_name=b'BPA ID', primary_key=True)),
                ('date_sampled', models.DateField(null=True, verbose_name=b'Date Sampled', blank=True)),
                ('time_sampled', models.TimeField(null=True, verbose_name=b'Time Sampled', blank=True)),
                ('depth', models.IntegerField(null=True, verbose_name=b'Depth (m)', blank=True)),
                ('note', models.TextField(null=True, verbose_name=b'Note', blank=True)),
                ('pam', models.DecimalField(verbose_name=b'Pulse amplitude modulated (PAM)', max_digits=9, decimal_places=6)),
                ('fluoro', models.DecimalField(verbose_name=b'Fluorometer Measurement', max_digits=9, decimal_places=6)),
                ('host_state', models.TextField(verbose_name=b'Host State')),
                ('host_abundance', models.DecimalField(verbose_name=b'Host Abundance', max_digits=9, decimal_places=6)),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='common.Site', null=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Seagrass Contextual Data',
                'verbose_name_plural': 'Seagrass Contextual Data',
            },
        ),
        migrations.CreateModel(
            name='SeaWeedContextual',
            fields=[
                ('bpa_id', models.IntegerField(serialize=False, verbose_name=b'BPA ID', primary_key=True)),
                ('date_sampled', models.DateField(null=True, verbose_name=b'Date Sampled', blank=True)),
                ('time_sampled', models.TimeField(null=True, verbose_name=b'Time Sampled', blank=True)),
                ('depth', models.IntegerField(null=True, verbose_name=b'Depth (m)', blank=True)),
                ('note', models.TextField(null=True, verbose_name=b'Note', blank=True)),
                ('pam', models.DecimalField(verbose_name=b'Pulse amplitude modulated (PAM)', max_digits=9, decimal_places=6)),
                ('fluoro', models.DecimalField(verbose_name=b'Fluorometer Measurement', max_digits=9, decimal_places=6)),
                ('host_state', models.TextField(verbose_name=b'Host State')),
                ('host_abundance', models.DecimalField(verbose_name=b'Host Abundance', max_digits=9, decimal_places=6)),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='common.Site', null=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Seaweed Contextual Data',
                'verbose_name_plural': 'Seaweed Contextual Data',
            },
        ),
        migrations.CreateModel(
            name='SedimentContextual',
            fields=[
                ('bpa_id', models.IntegerField(serialize=False, verbose_name=b'BPA ID', primary_key=True)),
                ('date_sampled', models.DateField(null=True, verbose_name=b'Date Sampled', blank=True)),
                ('time_sampled', models.TimeField(null=True, verbose_name=b'Time Sampled', blank=True)),
                ('depth', models.IntegerField(null=True, verbose_name=b'Depth (m)', blank=True)),
                ('note', models.TextField(null=True, verbose_name=b'Note', blank=True)),
                ('host_species', models.TextField(null=True, verbose_name=b'Host Species', blank=True)),
                ('carbon', models.DecimalField(null=True, verbose_name=b'% total carbon', max_digits=5, decimal_places=2, blank=True)),
                ('sediment', models.DecimalField(null=True, verbose_name=b'% fine sediment', max_digits=5, decimal_places=2, blank=True)),
                ('nitrogen', models.DecimalField(null=True, verbose_name=b'% total nitrogen', max_digits=5, decimal_places=2, blank=True)),
                ('phosphorous', models.DecimalField(null=True, verbose_name=b'% total phosphorous', max_digits=5, decimal_places=2, blank=True)),
                ('sedimentation_rate', models.DecimalField(null=True, verbose_name=b'sedimentation rate (g /(cm2 x y)r)', max_digits=5, decimal_places=2, blank=True)),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='common.Site', null=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Sediment Contextual Data',
                'verbose_name_plural': 'Sediment Contextual Data',
            },
        ),
        migrations.CreateModel(
            name='SpongeContextual',
            fields=[
                ('bpa_id', models.IntegerField(serialize=False, verbose_name=b'BPA ID', primary_key=True)),
                ('date_sampled', models.DateField(null=True, verbose_name=b'Date Sampled', blank=True)),
                ('time_sampled', models.TimeField(null=True, verbose_name=b'Time Sampled', blank=True)),
                ('depth', models.IntegerField(null=True, verbose_name=b'Depth (m)', blank=True)),
                ('note', models.TextField(null=True, verbose_name=b'Note', blank=True)),
                ('host_state', models.TextField(verbose_name=b'Host State')),
                ('host_abundance', models.DecimalField(verbose_name=b'Host Abundance', max_digits=9, decimal_places=6)),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='common.Site', null=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Sponge Contextual Data',
                'verbose_name_plural': 'Sponge Contextual Data',
            },
        ),
        migrations.CreateModel(
            name='TransferLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('transfer_to_facility_date', models.DateField(verbose_name=b'Transfer to Facility Date')),
                ('description', models.CharField(max_length=100, verbose_name=b'Description')),
                ('data_type', models.CharField(max_length=50, verbose_name=b'Data Type')),
                ('folder_name', models.CharField(max_length=100, verbose_name=b'Folder')),
                ('transfer_to_archive_date', models.DateField(verbose_name=b'Transfer to Archive Date')),
                ('notes', models.TextField(null=True, verbose_name=b'Notes', blank=True)),
                ('ticket_url', models.URLField(verbose_name=b'Dataset')),
                ('downloads_url', models.URLField(verbose_name=b'Downloads')),
                ('facility', models.ForeignKey(related_name='marine_microbes_transferlog_facility', verbose_name=b'Sequencing Facility', blank=True, to='common.Facility', null=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Transfer Log',
                'verbose_name_plural': 'Transfers',
            },
        ),
    ]
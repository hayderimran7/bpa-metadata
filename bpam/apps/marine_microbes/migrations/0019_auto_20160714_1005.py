# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('marine_microbes', '0018_auto_20160713_1316'),
    ]

    operations = [
        migrations.CreateModel(
            name='CoastalContextual',
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
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='marine_microbes.MMSite', null=True)),
            ],
            options={
                'verbose_name': 'Coastal Contextual Data',
                'verbose_name_plural': 'Coastal Contextual Data',
            },
        ),
        migrations.RemoveField(
            model_name='pelagiccontextual',
            name='site',
        ),
        migrations.DeleteModel(
            name='PelagicContextual',
        ),
    ]

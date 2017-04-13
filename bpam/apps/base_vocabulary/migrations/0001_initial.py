# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AustralianSoilClassification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('classification', models.CharField(max_length=50)),
                ('note', models.TextField(null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Australian Soil Classification',
            },
        ),
        migrations.CreateModel(
            name='BroadVegetationType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vegetation', models.CharField(unique=True, max_length=100)),
                ('note', models.TextField(null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Broad Vegetation Types',
            },
        ),
        migrations.CreateModel(
            name='DrainageClassification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('drainage', models.CharField(max_length=50)),
                ('description', models.TextField(null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Drainage Classifications',
            },
        ),
        migrations.CreateModel(
            name='FAOSoilClassification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('classification', models.CharField(max_length=50)),
                ('note', models.TextField(null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'FAO Soil Classification',
            },
        ),
        migrations.CreateModel(
            name='GeneralEcologicalZone',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(unique=True, max_length=100)),
                ('note', models.TextField(null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'General Ecological Zones',
            },
        ),
        migrations.CreateModel(
            name='HorizonClassification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('horizon', models.CharField(unique=True, max_length=100)),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'Horizon Classification',
            },
        ),
        migrations.CreateModel(
            name='LandUse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=300)),
                ('note', models.TextField(null=True, blank=True)),
                ('order', models.IntegerField()),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name='children', blank=True, to='base_vocabulary.LandUse', null=True)),
            ],
            options={
                'verbose_name_plural': 'Land Uses',
            },
        ),
        migrations.CreateModel(
            name='ProfilePosition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name_plural': 'Profile Positions',
            },
        ),
        migrations.CreateModel(
            name='SoilColour',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('colour', models.CharField(unique=True, max_length=100)),
                ('code', models.CharField(unique=True, max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='TillageType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tillage', models.CharField(unique=True, max_length=100)),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'Tillage Types',
            },
        ),
    ]

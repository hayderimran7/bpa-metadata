# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = []

    operations = [
        migrations.CreateModel(name='BPAProject',
                               fields=[
                                   ('key', models.CharField(
                                       max_length=30, serialize=False, primary_key=True)),
                                   ('name', models.CharField(max_length=200)),
                                   ('description', models.CharField(help_text=b'BPA Project description',
                                                                    max_length=2000,
                                                                    verbose_name='Description',
                                                                    blank=True)),
                                   ('note', models.TextField(blank=True)),
                               ],
                               options={
                                   'verbose_name': 'BPA Project',
                                   'verbose_name_plural': 'BPA Projects',
                               }, ),
        migrations.CreateModel(name='BPAUniqueID',
                               fields=[
                                   ('bpa_id', models.CharField(primary_key=True,
                                                               serialize=False,
                                                               max_length=200,
                                                               help_text=b'Unique BPA ID',
                                                               unique=True,
                                                               verbose_name='BPA ID')),
                                   ('note', models.TextField(blank=True)),
                                   ('project', models.ForeignKey(to='common.BPAProject')),
                               ],
                               options={
                                   'verbose_name': 'BPA Unique ID',
                                   'verbose_name_plural': "BPA Unique ID's",
                               }, ),
        migrations.CreateModel(
            name='DNASource',
            fields=[
                ('id', models.AutoField(
                    verbose_name='ID', serialize=False,
                    auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=100)),
                ('note', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': 'DNA Source',
                'verbose_name_plural': 'DNA Sources',
            }, ),
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('id', models.AutoField(
                    verbose_name='ID', serialize=False,
                    auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Facility short name',
                                          unique=True,
                                          max_length=100,
                                          verbose_name='Facility Name')),
                ('note', models.TextField(blank=True)),
            ],
            options={
                'verbose_name_plural': 'Facilities',
            }, ),
        migrations.CreateModel(
            name='Organism',
            fields=[
                ('id', models.AutoField(
                    verbose_name='ID', serialize=False,
                    auto_created=True, primary_key=True)),
                ('domain', models.CharField(max_length=100, verbose_name='Domain',
                                            blank=True)),
                ('kingdom', models.CharField(max_length=100, blank=True)),
                ('phylum', models.CharField(max_length=100, blank=True)),
                ('organism_class', models.CharField(max_length=100, verbose_name='Class',
                                                    blank=True)),
                ('order', models.CharField(max_length=100, blank=True)),
                ('family', models.CharField(max_length=100, blank=True)),
                ('genus', models.CharField(max_length=100, blank=True)),
                ('species', models.CharField(max_length=100, blank=True)),
                ('ncbi_classification', models.URLField(verbose_name=b'NCBI Organismal Classification',
                                                        blank=True)),
                ('note', models.TextField(blank=True)),
            ],
            options={
                'verbose_name_plural': 'Organisms',
            }, ),
        migrations.CreateModel(name='Sequencer',
                               fields=[
                                   ('name', models.CharField(help_text=b'The sequencer name',
                                                             max_length=100,
                                                             serialize=False,
                                                             primary_key=True)),
                                   ('description', models.TextField(blank=True)),
                               ],
                               options={
                                   'verbose_name': 'Sequencer',
                               }, ),
        migrations.CreateModel(
            name='URLVerification',
            fields=[
                ('id', models.AutoField(
                    verbose_name='ID', serialize=False,
                    auto_created=True, primary_key=True)),
                ('checked_url', models.URLField()),
                ('checked_at', models.DateTimeField()),
                ('status_ok', models.NullBooleanField(default=False)),
                ('status_note', models.TextField()),
            ], ),
    ]

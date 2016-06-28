# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [('common', '0001_initial'), ]

    operations = [
        migrations.CreateModel(
            name='Sheet',
            fields=[
                ('sheet_number', models.IntegerField(serialize=False,
                                                     verbose_name=b'Sheet Number',
                                                     primary_key=True)),
                ('name_id', models.TextField(null=True, verbose_name=b'Name ID',
                                             blank=True)),
                ('plant_description', models.TextField(null=True,
                                                       verbose_name=b'Plant Description',
                                                       blank=True)),
                ('site_description', models.TextField(null=True, verbose_name=b'Site Description',
                                                      blank=True)),
                ('vegetation', models.TextField(null=True, verbose_name=b'Vegetation',
                                                blank=True)),
                ('latitude', models.FloatField(help_text=b'Degree decimal',
                                               verbose_name=b'Latitude')),
                ('longitude', models.FloatField(help_text=b'Degree decimal',
                                                verbose_name=b'Longitude')),
                ('datum', models.CharField(max_length=50, null=True,
                                           verbose_name=b'Datum',
                                           blank=True)),
                ('geocode_accuracy', models.FloatField(
                    max_length=100, null=True, verbose_name=b'Geocode Accuracy',
                    blank=True)),
                ('geocode_method', models.CharField(
                    max_length=100, null=True, verbose_name=b'Gecode Method',
                    blank=True)),
                ('barker_coordinate_accuracy_flag', models.IntegerField(null=True,
                                                                        verbose_name=b'Barker Coordinate Accuracy Flag',
                                                                        blank=True)),
                ('family', models.CharField(max_length=100,
                                            null=True, verbose_name=b'Family',
                                            blank=True)),
                ('genus', models.CharField(max_length=100, null=True,
                                           verbose_name=b'Genus',
                                           blank=True)),
                ('species', models.CharField(max_length=100,
                                             null=True, verbose_name=b'Species',
                                             blank=True)),
                ('rank', models.CharField(max_length=100, null=True,
                                          verbose_name=b'Rank',
                                          blank=True)),
                ('infraspecies_qualifier', models.CharField(max_length=100,
                                                            null=True,
                                                            verbose_name=b'Infraspecies Qualifier',
                                                            blank=True)),
                ('infraspecies', models.CharField(
                    max_length=100, null=True, verbose_name=b'Infraspecies',
                    blank=True)),
                ('alien', models.BooleanField(default=False, verbose_name=b'Alien')),
                ('author', models.CharField(max_length=100,
                                            null=True, verbose_name=b'Author',
                                            blank=True)),
                ('manuscript', models.CharField(
                    max_length=100, null=True, verbose_name=b'Manuscript',
                    blank=True)),
                ('conservation_code', models.CharField(
                    max_length=100, null=True, verbose_name=b'Conservation Code',
                    blank=True)),
                ('determiner_name', models.CharField(
                    max_length=100, null=True, verbose_name=b'Determiner Name',
                    blank=True)),
                ('date_of_determination', models.DateField(null=True,
                                                           verbose_name=b'Date of Determination',
                                                           blank=True)),
                ('determiner_role', models.CharField(
                    max_length=100, null=True, verbose_name=b'Determiner Role',
                    blank=True)),
                ('name_comment', models.TextField(null=True, verbose_name=b'Name Comment',
                                                  blank=True)),
                ('frequency', models.CharField(
                    max_length=100, null=True, verbose_name=b'Frequency',
                    blank=True)),
                ('locality', models.TextField(null=True, verbose_name=b'Locality',
                                              blank=True)),
                ('state', models.CharField(max_length=100, null=True,
                                           verbose_name=b'State',
                                           blank=True)),
                ('collector', models.CharField(
                    max_length=100, null=True, verbose_name=b'Collector',
                    blank=True)),
                ('collector_number', models.CharField(
                    max_length=100, null=True, verbose_name=b'Collector Number',
                    blank=True)),
                ('collection_date', models.DateField(null=True, verbose_name=b'Collection Date',
                                                     blank=True)),
                ('voucher', models.TextField(null=True, verbose_name=b'Voucher',
                                             blank=True)),
                ('voucher_id', models.IntegerField(null=True, verbose_name=b'Voucher ID',
                                                   blank=True)),
                ('voucher_site', models.CharField(
                    max_length=300, null=True, verbose_name=b'Voucher Site',
                    blank=True)),
                ('type_status', models.CharField(
                    max_length=300, null=True, verbose_name=b'Type Status',
                    blank=True)),
                ('note', models.TextField(null=True, verbose_name=b'Note', blank=True)),
                ('bpa_id', models.OneToOneField(
                    null=True, blank=True, to='common.BPAUniqueID',
                    verbose_name='BPA ID')),
            ], ),
    ]

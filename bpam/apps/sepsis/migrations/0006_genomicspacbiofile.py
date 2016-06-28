# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0006_auto_20160523_1340'),
        ('sepsis', '0005_auto_20160610_1021'),
    ]

    operations = [
        migrations.CreateModel(
            name='GenomicsPacBioFile',
            fields=[
                ('id', models.AutoField(
                    verbose_name='ID', serialize=False,
                    auto_created=True, primary_key=True)),
                ('index_number', models.IntegerField(null=True, verbose_name=b'Index Number',
                                                     blank=True)),
                ('lane_number', models.IntegerField(null=True, verbose_name=b'Lane Number',
                                                    blank=True)),
                ('read_number', models.IntegerField(null=True, verbose_name=b'Read Number',
                                                    blank=True)),
                ('date_received_from_sequencing_facility', models.DateField(null=True, blank=True)),
                ('filename', models.CharField(
                    max_length=300, null=True, verbose_name=b'File Name',
                    blank=True)),
                ('md5', models.CharField(max_length=32,
                                         null=True, verbose_name=b'MD5 Checksum',
                                         blank=True)),
                ('analysed', models.NullBooleanField(default=False)),
                ('note', models.TextField(blank=True)),
                ('extraction', models.IntegerField(default=1, verbose_name=b'Extraction')),
                ('vendor', models.CharField(default=1, max_length=100, verbose_name=b'Vendor')),
                ('library', models.CharField(
                    help_text=b'MP or PE', max_length=20, verbose_name=b'Library')),
                ('size', models.CharField(default=1, max_length=100,
                                          verbose_name=b'Extraction Size')),
                ('flow_cell_id', models.CharField(max_length=6, verbose_name=b'Flow Cell ID')),
                ('index', models.CharField(max_length=20, verbose_name=b'Index')),
                ('runsamplenum', models.CharField(max_length=20, verbose_name=b'Sample Run Number')),
                ('read', models.CharField(max_length=3, verbose_name=b'Read')),
                ('method', models.ForeignKey(related_name='sepsis_genomicspacbiofile_files',
                                             to='sepsis.PacBioGenomicsMethod',
                                             help_text=b'PacBio Genomics Method',
                                             null=True)),
                ('sample', models.ForeignKey(to='sepsis.SepsisSample')),
                ('url_verification', models.ForeignKey(related_name='sepsis_genomicspacbiofile_related',
                                                       to='common.URLVerification',
                                                       null=True)),
            ],
            options={
                'abstract': False,
            }, ),
    ]

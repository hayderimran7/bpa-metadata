# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0007_site'),
        ('marine_microbes', '0007_remove_metagenomisequencefile_runsamplenum'),
    ]

    operations = [
        migrations.CreateModel(
            name='MetagenomicSequenceFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('index_number', models.IntegerField(null=True, verbose_name=b'Index Number', blank=True)),
                ('lane_number', models.IntegerField(null=True, verbose_name=b'Lane Number', blank=True)),
                ('read_number', models.IntegerField(null=True, verbose_name=b'Read Number', blank=True)),
                ('date_received_from_sequencing_facility', models.DateField(null=True, blank=True)),
                ('filename', models.CharField(max_length=300, null=True, verbose_name=b'File Name', blank=True)),
                ('md5', models.CharField(max_length=32, null=True, verbose_name=b'MD5 Checksum', blank=True)),
                ('analysed', models.NullBooleanField(default=False)),
                ('note', models.TextField(blank=True)),
                ('extraction', models.IntegerField(default=1, verbose_name=b'Extraction')),
                ('vendor', models.CharField(default=b'UNKNOWN', max_length=100, verbose_name=b'Vendor')),
                ('library', models.CharField(help_text=b'MP or PE', max_length=20, verbose_name=b'Library')),
                ('size', models.CharField(default=1, max_length=100, verbose_name=b'Extraction Size')),
                ('flow_cell_id', models.CharField(max_length=9, verbose_name=b'Flow Cell ID')),
                ('index', models.CharField(max_length=20, verbose_name=b'Index')),
                ('read', models.CharField(max_length=3, verbose_name=b'Read')),
                ('sample', models.ForeignKey(to='marine_microbes.MMSample')),
                ('url_verification', models.ForeignKey(related_name='marine_microbes_metagenomicsequencefile_related', to='common.URLVerification', null=True)),
            ],
            options={
                'verbose_name_plural': 'Metagenomics Sequence Files',
            },
        ),
        migrations.RemoveField(
            model_name='metagenomisequencefile',
            name='sample',
        ),
        migrations.RemoveField(
            model_name='metagenomisequencefile',
            name='url_verification',
        ),
        migrations.DeleteModel(
            name='MetagenomiSequenceFile',
        ),
    ]

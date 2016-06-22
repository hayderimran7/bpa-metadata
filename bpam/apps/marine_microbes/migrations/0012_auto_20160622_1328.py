# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0007_site'),
        ('marine_microbes', '0011_auto_20160621_1508'),
    ]

    operations = [
        migrations.CreateModel(
            name='AmpliconSequenceFile',
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
                ('extraction', models.IntegerField(null=True, verbose_name=b'Sample Extraction ID', blank=True)),
                ('amplicon', models.CharField(max_length=4, verbose_name=b'Amplicon', choices=[(b'16S', b'16S'), (b'ITS', b'ITS'), (b'18S', b'18S'), (b'A16S', b'A16S')])),
                ('vendor', models.CharField(default=b'UNKNOWN', max_length=100, verbose_name=b'Vendor')),
                ('index', models.CharField(max_length=50, null=True, verbose_name=b'Index', blank=True)),
                ('flow_cell', models.CharField(max_length=9, null=True, verbose_name=b'Flow Cell', blank=True)),
                ('runsamplenum', models.CharField(max_length=9, null=True, verbose_name=b'Run Sample Number', blank=True)),
                ('lane', models.CharField(max_length=5, null=True, verbose_name=b'Lane', blank=True)),
                ('read', models.CharField(max_length=2, null=True, verbose_name=b'Read', blank=True)),
                ('url_verification', models.ForeignKey(related_name='marine_microbes_ampliconsequencefile_related', to='common.URLVerification', null=True)),
            ],
            options={
                'verbose_name_plural': 'Amplicon Sequencing Metadata',
            },
        ),
        migrations.AlterModelOptions(
            name='mmsample',
            options={'verbose_name': 'Marine Microbes Sample'},
        ),
        migrations.RemoveField(
            model_name='metagenomicsequencefile',
            name='flow_cell_id',
        ),
        migrations.AddField(
            model_name='metagenomicsequencefile',
            name='flow_cell',
            field=models.CharField(max_length=9, null=True, verbose_name=b'Flow Cell', blank=True),
        ),
        migrations.AlterField(
            model_name='metagenomicsequencefile',
            name='index',
            field=models.CharField(max_length=20, null=True, verbose_name=b'Index', blank=True),
        ),
        migrations.AlterField(
            model_name='metagenomicsequencefile',
            name='read',
            field=models.CharField(max_length=3, null=True, verbose_name=b'Read', blank=True),
        ),
    ]

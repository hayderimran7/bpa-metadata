# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0010_ckanserver'),
        ('sepsis', '0021_add_last_modified'),
    ]

    operations = [
        migrations.CreateModel(
            name='GenomicsHiseqFile',
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
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('extraction', models.IntegerField(default=1, verbose_name=b'Extraction')),
                ('vendor', models.CharField(default=1, max_length=100, verbose_name=b'Vendor')),
                ('library', models.CharField(help_text=b'MP or PE', max_length=20, verbose_name=b'Library')),
                ('size', models.CharField(default=1, max_length=100, verbose_name=b'Extraction Size')),
                ('flow_cell_id', models.CharField(max_length=9, verbose_name=b'Flow Cell ID')),
                ('index', models.CharField(max_length=20, verbose_name=b'Index')),
                ('read', models.CharField(max_length=3, verbose_name=b'Read')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HiseqGenomicsMethod',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('library_construction_protocol', models.CharField(max_length=100, null=True, verbose_name=b'Library Construction Protocol', blank=True)),
                ('sequencer', models.CharField(max_length=100, null=True, verbose_name=b'Sequencer', blank=True)),
                ('casava_version', models.CharField(max_length=20, null=True, verbose_name=b'CASAVA Version', blank=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Hiseq Genomics Method',
            },
        ),
        migrations.AlterField(
            model_name='genomicsmiseqfile',
            name='method',
            field=models.ForeignKey(related_name='sepsis_genomicsmiseqfile_files', to='sepsis.MiseqGenomicsMethod', help_text=b'MiSeq Genomics Method', null=True),
        ),
        migrations.AddField(
            model_name='genomicshiseqfile',
            name='method',
            field=models.ForeignKey(related_name='sepsis_genomicshiseqfile_files', to='sepsis.HiseqGenomicsMethod', help_text=b'HiSeq Genomics Method', null=True),
        ),
        migrations.AddField(
            model_name='genomicshiseqfile',
            name='sample',
            field=models.ForeignKey(related_name='sepsis_genomicshiseqfile_files', to='sepsis.SepsisSample'),
        ),
        migrations.AddField(
            model_name='genomicshiseqfile',
            name='url_verification',
            field=models.ForeignKey(related_name='sepsis_genomicshiseqfile_related', to='common.URLVerification', null=True),
        ),
    ]

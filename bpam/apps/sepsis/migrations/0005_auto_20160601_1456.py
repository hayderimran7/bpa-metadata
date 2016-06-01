# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sepsis', '0004_auto_20160601_1427'),
    ]

    operations = [
        migrations.CreateModel(
            name='MiseqGenomicsMethod',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('library_construction_protocol', models.CharField(max_length=100, null=True, verbose_name=b'Library Construction Protocol', blank=True)),
                ('insert_size_range', models.CharField(max_length=20, null=True, verbose_name=b'Insert Size Range', blank=True)),
                ('sequencer', models.CharField(max_length=100, null=True, verbose_name=b'Sequencer', blank=True)),
                ('analysis_software_version', models.CharField(max_length=20, null=True, verbose_name=b'Analysis Software Version', blank=True)),
            ],
            options={
                'verbose_name': 'Miseq Genomics Method',
            },
        ),
        migrations.CreateModel(
            name='PacBioGenomicsMethod',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('library_construction_protocol', models.CharField(max_length=100, null=True, verbose_name=b'Library Construction Protocol', blank=True)),
                ('insert_size_range', models.CharField(max_length=20, null=True, verbose_name=b'Insert Size Range', blank=True)),
                ('sequencer', models.CharField(max_length=100, null=True, verbose_name=b'Sequencer', blank=True)),
                ('sequencer_run_id', models.CharField(max_length=20, null=True, verbose_name=b'Sequencer run ID', blank=True)),
                ('smrt_cell_id', models.CharField(max_length=60, null=True, verbose_name=b'SMRT Cell ID', blank=True)),
                ('cell_position', models.CharField(max_length=60, null=True, verbose_name=b'Cell Position', blank=True)),
                ('rs_version', models.CharField(max_length=20, null=True, verbose_name=b'RS Version', blank=True)),
            ],
            options={
                'verbose_name': 'PacBio Genomics Method',
            },
        ),
        migrations.RemoveField(
            model_name='proteomicsfile',
            name='method',
        ),
        migrations.RemoveField(
            model_name='transcriptomicsfile',
            name='method',
        ),
        migrations.AlterField(
            model_name='genomicsmiseqfile',
            name='method',
            field=models.ForeignKey(related_name='sepsis_genomicsmiseqfile_files', to='sepsis.MiseqGenomicsMethod', help_text=b'Genomics Method', null=True),
        ),
        migrations.DeleteModel(
            name='GenomicsMethod',
        ),
    ]

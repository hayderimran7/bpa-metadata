# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0009_delete_site'),
        ('sepsis', '0016_auto_20160824_0811'),
    ]

    operations = [
        migrations.CreateModel(
            name='PacBioTrack',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('taxon_or_organism', models.CharField(max_length=200, null=True, verbose_name=b'Taxon or Organism', blank=True)),
                ('strain_or_isolate', models.CharField(max_length=200, null=True, verbose_name=b'Strain Or Isolate', blank=True)),
                ('serovar', models.CharField(max_length=500, null=True, verbose_name=b'Serovar', blank=True)),
                ('growth_media', models.CharField(max_length=500, null=True, verbose_name=b'Growth Media', blank=True)),
                ('replicate', models.IntegerField(null=True, verbose_name=b'Replicate', blank=True)),
                ('omics', models.CharField(max_length=50, null=True, verbose_name=b'Omics Type', blank=True)),
                ('analytical_platform', models.CharField(max_length=100, null=True, verbose_name=b'Analytical Platform', blank=True)),
                ('facility', models.CharField(max_length=100, null=True, verbose_name=b'Facility', blank=True)),
                ('work_order', models.CharField(max_length=50, null=True, verbose_name=b'Work Order', blank=True)),
                ('contextual_data_submission_date', models.DateField(help_text=b'YYYY-MM-DD', null=True, verbose_name=b'Contextual Data Submission Date', blank=True)),
                ('sample_submission_date', models.DateField(help_text=b'YYYY-MM-DD', null=True, verbose_name=b'Sample Submission Date', blank=True)),
                ('data_generated', models.NullBooleanField(default=False, verbose_name=b'Data Generated')),
                ('archive_ingestion_date', models.DateField(help_text=b'YYYY-MM-DD', null=True, verbose_name=b'Archive Ingestion Date', blank=True)),
                ('curation_url', models.URLField(null=True, verbose_name=b'Curation URL', blank=True)),
                ('dataset_url', models.URLField(null=True, verbose_name=b'Download URL', blank=True)),
                ('bpa_id', models.ForeignKey(verbose_name=b'BPA ID', to='common.BPAUniqueID', help_text=b'Bioplatforms Australia Sample ID', null=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Sample Tracking Information',
                'verbose_name_plural': 'Sample Tracking',
            },
        ),
        migrations.RemoveField(
            model_name='sepsissample',
            name='sample_track',
        ),
        migrations.DeleteModel(
            name='SampleTrack',
        ),
    ]

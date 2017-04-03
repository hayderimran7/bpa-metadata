# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0013_auto_20170328_1527'),
        ('marine_microbes', '0028_auto_20170403_1403'),
    ]

    operations = [
        migrations.CreateModel(
            name='AmpliconA16STrack',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data_type', models.IntegerField(blank=True, null=True, verbose_name=b'Data Type', choices=[(1, b'Pre-pilot'), (2, b'Pilot'), (3, b'Main dataset')])),
                ('description', models.CharField(max_length=1024, null=True, verbose_name=b'Description', blank=True)),
                ('omics', models.CharField(max_length=50, null=True, verbose_name=b'Omics Type', blank=True)),
                ('analytical_platform', models.CharField(max_length=100, null=True, verbose_name=b'Analytical Platform', blank=True)),
                ('facility', models.CharField(max_length=100, null=True, verbose_name=b'Facility', blank=True)),
                ('work_order', models.CharField(max_length=50, null=True, verbose_name=b'Work Order', blank=True)),
                ('contextual_data_submission_date', models.DateField(help_text=b'YYYY-MM-DD', null=True, verbose_name=b'Contextual Data Submission Date', blank=True)),
                ('sample_submission_date', models.DateField(help_text=b'YYYY-MM-DD', null=True, verbose_name=b'Sample Submission Date', blank=True)),
                ('data_generated', models.NullBooleanField(default=False, verbose_name=b'Data Generated')),
                ('dataset_url', models.URLField(null=True, verbose_name=b'Download URL', blank=True)),
                ('in_data_portal', models.BooleanField(verbose_name=b'Data ingested into data portal')),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('bpa_id', models.ForeignKey(verbose_name=b'BPA ID', to='common.BPAUniqueID', help_text=b'Bioplatforms Australia Sample ID', null=True)),
            ],
            options={
                'verbose_name': 'Track Amplicon A16S',
                'verbose_name_plural': 'Track Amplicon A16S',
            },
        ),
        migrations.CreateModel(
            name='MetatranscriptomeTrack',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data_type', models.IntegerField(blank=True, null=True, verbose_name=b'Data Type', choices=[(1, b'Pre-pilot'), (2, b'Pilot'), (3, b'Main dataset')])),
                ('description', models.CharField(max_length=1024, null=True, verbose_name=b'Description', blank=True)),
                ('omics', models.CharField(max_length=50, null=True, verbose_name=b'Omics Type', blank=True)),
                ('analytical_platform', models.CharField(max_length=100, null=True, verbose_name=b'Analytical Platform', blank=True)),
                ('facility', models.CharField(max_length=100, null=True, verbose_name=b'Facility', blank=True)),
                ('work_order', models.CharField(max_length=50, null=True, verbose_name=b'Work Order', blank=True)),
                ('contextual_data_submission_date', models.DateField(help_text=b'YYYY-MM-DD', null=True, verbose_name=b'Contextual Data Submission Date', blank=True)),
                ('sample_submission_date', models.DateField(help_text=b'YYYY-MM-DD', null=True, verbose_name=b'Sample Submission Date', blank=True)),
                ('data_generated', models.NullBooleanField(default=False, verbose_name=b'Data Generated')),
                ('dataset_url', models.URLField(null=True, verbose_name=b'Download URL', blank=True)),
                ('in_data_portal', models.BooleanField(verbose_name=b'Data ingested into data portal')),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('bpa_id', models.ForeignKey(verbose_name=b'BPA ID', to='common.BPAUniqueID', help_text=b'Bioplatforms Australia Sample ID', null=True)),
            ],
            options={
                'verbose_name': 'Track Metatranscriptome',
                'verbose_name_plural': 'Track Metatranscriptome',
            },
        ),
        migrations.RemoveField(
            model_name='amplicon16strack',
            name='archive_ingestion_date',
        ),
        migrations.RemoveField(
            model_name='amplicon16strack',
            name='curation_url',
        ),
        migrations.RemoveField(
            model_name='amplicon16strack',
            name='growth_media',
        ),
        migrations.RemoveField(
            model_name='amplicon16strack',
            name='replicate',
        ),
        migrations.RemoveField(
            model_name='amplicon16strack',
            name='serovar',
        ),
        migrations.RemoveField(
            model_name='amplicon16strack',
            name='strain_or_isolate',
        ),
        migrations.RemoveField(
            model_name='amplicon16strack',
            name='taxon_or_organism',
        ),
        migrations.RemoveField(
            model_name='amplicon18strack',
            name='archive_ingestion_date',
        ),
        migrations.RemoveField(
            model_name='amplicon18strack',
            name='curation_url',
        ),
        migrations.RemoveField(
            model_name='amplicon18strack',
            name='growth_media',
        ),
        migrations.RemoveField(
            model_name='amplicon18strack',
            name='replicate',
        ),
        migrations.RemoveField(
            model_name='amplicon18strack',
            name='serovar',
        ),
        migrations.RemoveField(
            model_name='amplicon18strack',
            name='strain_or_isolate',
        ),
        migrations.RemoveField(
            model_name='amplicon18strack',
            name='taxon_or_organism',
        ),
        migrations.RemoveField(
            model_name='metagenomicstrack',
            name='archive_ingestion_date',
        ),
        migrations.RemoveField(
            model_name='metagenomicstrack',
            name='curation_url',
        ),
        migrations.RemoveField(
            model_name='metagenomicstrack',
            name='growth_media',
        ),
        migrations.RemoveField(
            model_name='metagenomicstrack',
            name='replicate',
        ),
        migrations.RemoveField(
            model_name='metagenomicstrack',
            name='serovar',
        ),
        migrations.RemoveField(
            model_name='metagenomicstrack',
            name='strain_or_isolate',
        ),
        migrations.RemoveField(
            model_name='metagenomicstrack',
            name='taxon_or_organism',
        ),
        migrations.AddField(
            model_name='amplicon16strack',
            name='description',
            field=models.CharField(max_length=1024, null=True, verbose_name=b'Description', blank=True),
        ),
        migrations.AddField(
            model_name='amplicon16strack',
            name='in_data_portal',
            field=models.BooleanField(default=False, verbose_name=b'Data ingested into data portal'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='amplicon18strack',
            name='description',
            field=models.CharField(max_length=1024, null=True, verbose_name=b'Description', blank=True),
        ),
        migrations.AddField(
            model_name='amplicon18strack',
            name='in_data_portal',
            field=models.BooleanField(default=False, verbose_name=b'Data ingested into data portal'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='metagenomicstrack',
            name='description',
            field=models.CharField(max_length=1024, null=True, verbose_name=b'Description', blank=True),
        ),
        migrations.AddField(
            model_name='metagenomicstrack',
            name='in_data_portal',
            field=models.BooleanField(default=False, verbose_name=b'Data ingested into data portal'),
            preserve_default=False,
        ),
    ]

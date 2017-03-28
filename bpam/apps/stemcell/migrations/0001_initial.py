# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0012_auto_20170324_1555'),
    ]

    operations = [
        migrations.CreateModel(
            name='MetabolomicTrack',
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
                ('archive_ingestion_date', models.DateField(help_text=b'YYYY-MM-DD', null=True, verbose_name=b'Archive Ingestion Date', blank=True)),
                ('dataset_url', models.URLField(null=True, verbose_name=b'Download URL', blank=True)),
                ('in_data_portal', models.BooleanField(verbose_name=b'Data ingested into data portal')),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('bpa_id', models.ForeignKey(verbose_name=b'BPA ID', to='common.BPAUniqueID', help_text=b'Bioplatforms Australia Sample ID', null=True)),
            ],
            options={
                'verbose_name': 'Track Metabolomic',
                'verbose_name_plural': 'Track Metabolomic',
            },
        ),
        migrations.CreateModel(
            name='ProteomicTrack',
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
                ('archive_ingestion_date', models.DateField(help_text=b'YYYY-MM-DD', null=True, verbose_name=b'Archive Ingestion Date', blank=True)),
                ('dataset_url', models.URLField(null=True, verbose_name=b'Download URL', blank=True)),
                ('in_data_portal', models.BooleanField(verbose_name=b'Data ingested into data portal')),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('bpa_id', models.ForeignKey(verbose_name=b'BPA ID', to='common.BPAUniqueID', help_text=b'Bioplatforms Australia Sample ID', null=True)),
            ],
            options={
                'verbose_name': 'Track Proteomic',
                'verbose_name_plural': 'Track Proteomic',
            },
        ),
        migrations.CreateModel(
            name='SingleCellRNASeqTrack',
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
                ('archive_ingestion_date', models.DateField(help_text=b'YYYY-MM-DD', null=True, verbose_name=b'Archive Ingestion Date', blank=True)),
                ('dataset_url', models.URLField(null=True, verbose_name=b'Download URL', blank=True)),
                ('in_data_portal', models.BooleanField(verbose_name=b'Data ingested into data portal')),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('bpa_id', models.ForeignKey(verbose_name=b'BPA ID', to='common.BPAUniqueID', help_text=b'Bioplatforms Australia Sample ID', null=True)),
            ],
            options={
                'verbose_name': 'Track SingleCellRNA',
                'verbose_name_plural': 'Track SingleCellRNA',
            },
        ),
        migrations.CreateModel(
            name='SmallRNATrack',
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
                ('archive_ingestion_date', models.DateField(help_text=b'YYYY-MM-DD', null=True, verbose_name=b'Archive Ingestion Date', blank=True)),
                ('dataset_url', models.URLField(null=True, verbose_name=b'Download URL', blank=True)),
                ('in_data_portal', models.BooleanField(verbose_name=b'Data ingested into data portal')),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('bpa_id', models.ForeignKey(verbose_name=b'BPA ID', to='common.BPAUniqueID', help_text=b'Bioplatforms Australia Sample ID', null=True)),
            ],
            options={
                'verbose_name': 'Track SmallRNA',
                'verbose_name_plural': 'Track SmallRNA',
            },
        ),
        migrations.CreateModel(
            name='TranscriptomeTrack',
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
                ('archive_ingestion_date', models.DateField(help_text=b'YYYY-MM-DD', null=True, verbose_name=b'Archive Ingestion Date', blank=True)),
                ('dataset_url', models.URLField(null=True, verbose_name=b'Download URL', blank=True)),
                ('in_data_portal', models.BooleanField(verbose_name=b'Data ingested into data portal')),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('bpa_id', models.ForeignKey(verbose_name=b'BPA ID', to='common.BPAUniqueID', help_text=b'Bioplatforms Australia Sample ID', null=True)),
            ],
            options={
                'verbose_name': 'Track Transcriptome',
                'verbose_name_plural': 'Track Transcriptome',
            },
        ),
    ]

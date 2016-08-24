# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sepsis', '0012_auto_20160823_1021'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sampletrack',
            name='allocation_date',
        ),
        migrations.RemoveField(
            model_name='sampletrack',
            name='given_to',
        ),
        migrations.AddField(
            model_name='sampletrack',
            name='growth_media',
            field=models.CharField(max_length=500, null=True, verbose_name=b'Growth Media', blank=True),
        ),
        migrations.AddField(
            model_name='sampletrack',
            name='serovar',
            field=models.CharField(max_length=500, null=True, verbose_name=b'Serovar', blank=True),
        ),
        migrations.AddField(
            model_name='sampletrack',
            name='strain_or_isolate',
            field=models.CharField(max_length=200, null=True, verbose_name=b'Strain Or Isolate', blank=True),
        ),
        migrations.AddField(
            model_name='sampletrack',
            name='taxon_or_organism',
            field=models.CharField(max_length=200, null=True, verbose_name=b'Taxon or Organism', blank=True),
        ),
        migrations.AlterField(
            model_name='sampletrack',
            name='archive_ingestion_date',
            field=models.DateField(help_text=b'YYYY-MM-DD', null=True, verbose_name=b'Archive Ingestion Date', blank=True),
        ),
        migrations.AlterField(
            model_name='sampletrack',
            name='bpa_id',
            field=models.ForeignKey(verbose_name=b'BPA ID', to='common.BPAUniqueID', help_text=b'Bioplatforms Australia Sample ID', null=True),
        ),
        migrations.AlterField(
            model_name='sampletrack',
            name='contextual_data_submission_date',
            field=models.DateField(help_text=b'YYYY-MM-DD', null=True, verbose_name=b'Contextual Data Submission Date', blank=True),
        ),
        migrations.AlterField(
            model_name='sampletrack',
            name='sample_submission_date',
            field=models.DateField(help_text=b'YYYY-MM-DD', null=True, verbose_name=b'Sample Submission Date', blank=True),
        ),
    ]

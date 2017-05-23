# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sepsis', '0028_auto_20161119_1707'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='genomicsmiseqfile',
            name='method',
        ),
        migrations.RemoveField(
            model_name='genomicsmiseqfile',
            name='sample',
        ),
        migrations.RemoveField(
            model_name='genomicsmiseqfile',
            name='url_verification',
        ),
        migrations.RemoveField(
            model_name='genomicspacbiofile',
            name='method',
        ),
        migrations.RemoveField(
            model_name='genomicspacbiofile',
            name='sample',
        ),
        migrations.RemoveField(
            model_name='genomicspacbiofile',
            name='url_verification',
        ),
        migrations.RemoveField(
            model_name='proteomicsfile',
            name='sample',
        ),
        migrations.RemoveField(
            model_name='proteomicsfile',
            name='url_verification',
        ),
        migrations.DeleteModel(
            name='ProteomicsMethod',
        ),
        migrations.RemoveField(
            model_name='sepsissample',
            name='bpa_id',
        ),
        migrations.RemoveField(
            model_name='sepsissample',
            name='growth_method',
        ),
        migrations.RemoveField(
            model_name='sepsissample',
            name='host',
        ),
        migrations.RemoveField(
            model_name='transcriptomicsfile',
            name='sample',
        ),
        migrations.RemoveField(
            model_name='transcriptomicsfile',
            name='url_verification',
        ),
        migrations.RemoveField(
            model_name='transcriptomicshiseqfile',
            name='method',
        ),
        migrations.RemoveField(
            model_name='transcriptomicshiseqfile',
            name='sample',
        ),
        migrations.RemoveField(
            model_name='transcriptomicshiseqfile',
            name='url_verification',
        ),
        migrations.DeleteModel(
            name='TranscriptomicsMethod',
        ),
        migrations.DeleteModel(
            name='GenomicsMiseqFile',
        ),
        migrations.DeleteModel(
            name='GenomicsPacBioFile',
        ),
        migrations.DeleteModel(
            name='GrowthMethod',
        ),
        migrations.DeleteModel(
            name='HiseqTranscriptomicsMethod',
        ),
        migrations.DeleteModel(
            name='Host',
        ),
        migrations.DeleteModel(
            name='MiseqGenomicsMethod',
        ),
        migrations.DeleteModel(
            name='PacBioGenomicsMethod',
        ),
        migrations.DeleteModel(
            name='ProteomicsFile',
        ),
        migrations.DeleteModel(
            name='SepsisSample',
        ),
        migrations.DeleteModel(
            name='TranscriptomicsFile',
        ),
        migrations.DeleteModel(
            name='TranscriptomicsHiseqFile',
        ),
    ]

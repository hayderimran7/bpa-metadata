# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sepsis', '0023_rename_sepsis_hiseq'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hiseqtranscriptomicsmethod',
            options={'verbose_name': 'Hiseq Transcriptomics Method'},
        ),
        migrations.AlterModelOptions(
            name='miseqgenomicsmethod',
            options={'verbose_name': 'Miseq Transcriptomics Method'},
        ),
        migrations.AlterField(
            model_name='transcriptomicshiseqfile',
            name='method',
            field=models.ForeignKey(related_name='sepsis_transcriptomicshiseqfile_files', to='sepsis.HiseqTranscriptomicsMethod', help_text=b'HiSeq Transcriptomics Method', null=True),
        ),
        migrations.AlterField(
            model_name='transcriptomicshiseqfile',
            name='sample',
            field=models.ForeignKey(related_name='sepsis_transcriptomicshiseqfile_files', to='sepsis.SepsisSample'),
        ),
        migrations.AlterField(
            model_name='transcriptomicshiseqfile',
            name='url_verification',
            field=models.ForeignKey(related_name='sepsis_transcriptomicshiseqfile_related', to='common.URLVerification', null=True),
        ),
    ]

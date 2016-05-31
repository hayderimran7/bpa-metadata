# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sepsis', '0012_auto_20160531_1039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genomicsfile',
            name='method',
            field=models.ForeignKey(related_name='sepsis_genomicsfile_genomicsfile', to='sepsis.GenomicsMethod', null=True),
        ),
        migrations.AlterField(
            model_name='transcriptomicsfile',
            name='method',
            field=models.ForeignKey(related_name='sepsis_transcriptomicsfile_transcriptomicsfile', to='sepsis.TranscriptomicsMethod', null=True),
        ),
    ]

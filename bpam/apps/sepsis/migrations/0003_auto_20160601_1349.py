# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sepsis', '0002_auto_20160531_1501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genomicsmiseqfile',
            name='method',
            field=models.ForeignKey(related_name='sepsis_genomicsmiseqfile_sepsis_sequence_files', to='sepsis.GenomicsMethod', help_text=b'Genomics Method', null=True),
        ),
        migrations.AlterField(
            model_name='proteomicsfile',
            name='method',
            field=models.ForeignKey(related_name='sepsis_proteomicsfile_sepsis_sequence_files', to='sepsis.GenomicsMethod', help_text=b'Genomics Method', null=True),
        ),
        migrations.AlterField(
            model_name='transcriptomicsfile',
            name='method',
            field=models.ForeignKey(related_name='sepsis_transcriptomicsfile_sepsis_sequence_files', to='sepsis.GenomicsMethod', help_text=b'Genomics Method', null=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0010_ckanserver'),
        ('sepsis', '0022_auto_20160929_1114'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='GenomicsHiseqFile',
            new_name='TranscriptomicsHiseqFile',
        ),
        migrations.RenameModel(
            old_name='HiseqGenomicsMethod',
            new_name='HiseqTranscriptomicsMethod',
        ),
    ]

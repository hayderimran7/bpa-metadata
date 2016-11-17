# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sepsis', '0025_auto_20161012_1151'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PacBioTrack',
            new_name='GenomicsPacBioTrack',
        ),
        migrations.RenameModel(
            old_name='MiSeqTrack',
            new_name='GenomicsMiSeqTrack',
        ),
        migrations.RenameModel(
            old_name='RNAHiSeqTrack',
            new_name='TranscriptomicsHiSeqTrack',
        ),
        migrations.RenameModel(
            old_name='MetabolomicsTrack',
            new_name='MetabolomicsLCMSTrack',
        ),
        migrations.RenameModel(
            old_name='DeepLCMSTrack',
            new_name='ProteomicsMS1QuantificationTrack',
        ),
        migrations.RenameModel(
            old_name='SWATHMSTrack',
            new_name='ProteomicsSwathMSTrack',
        ),
    ]

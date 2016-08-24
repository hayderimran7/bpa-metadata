# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sepsis', '0019_auto_20160824_1306'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='deeplcmstrack',
            options={'verbose_name': 'Track Deep LC-MS (Monash)', 'verbose_name_plural': 'Track Deep LC-MS (Monash)'},
        ),
        migrations.AlterModelOptions(
            name='metabolomicstrack',
            options={'verbose_name': 'Track Metabolomics', 'verbose_name_plural': 'Track Metabolomics'},
        ),
        migrations.AlterModelOptions(
            name='miseqtrack',
            options={'verbose_name': 'Track MiSeq', 'verbose_name_plural': 'Track MiSeq'},
        ),
        migrations.AlterModelOptions(
            name='pacbiotrack',
            options={'verbose_name': 'Track PacBio', 'verbose_name_plural': 'Track PacBio'},
        ),
        migrations.AlterModelOptions(
            name='rnahiseqtrack',
            options={'verbose_name': 'Track RNA (HiSeq)', 'verbose_name_plural': 'Track RNA (HiSeq)'},
        ),
        migrations.AlterModelOptions(
            name='swathmstrack',
            options={'verbose_name': 'Track SWATH-MS (APAF)', 'verbose_name_plural': 'Track SWATH-MS (APAF)'},
        ),
    ]

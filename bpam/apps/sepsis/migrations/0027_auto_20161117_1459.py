# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sepsis', '0026_renamemodels'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='genomicsmiseqtrack',
            options={'verbose_name': 'Track Genomics MiSeq', 'verbose_name_plural': 'Track Genomics MiSeq'},
        ),
        migrations.AlterModelOptions(
            name='genomicspacbiotrack',
            options={'verbose_name': 'Track Genomics PacBio', 'verbose_name_plural': 'Track Genomics PacBio'},
        ),
        migrations.AlterModelOptions(
            name='metabolomicslcmstrack',
            options={'verbose_name': 'Track Metabolomics LCMS', 'verbose_name_plural': 'Track Metabolomics LCMS'},
        ),
        migrations.AlterModelOptions(
            name='proteomicsms1quantificationtrack',
            options={'verbose_name': 'Track Proteomics MS1-Quantification', 'verbose_name_plural': 'Track Proteomics MS1-Quantification'},
        ),
        migrations.AlterModelOptions(
            name='proteomicsswathmstrack',
            options={'verbose_name': 'Track Proteomics Swath-MS', 'verbose_name_plural': 'Track Proteomics Swath-MS'},
        ),
        migrations.AlterModelOptions(
            name='transcriptomicshiseqtrack',
            options={'verbose_name': 'Track Transcriptomics HiSeq', 'verbose_name_plural': 'Track Transcriptomics HiSeq'},
        ),
    ]

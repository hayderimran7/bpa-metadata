# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marine_microbes', '0017_auto_20160701_0912'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='amplicon',
            name='facility',
        ),
        migrations.RemoveField(
            model_name='metagenomic',
            name='facility',
        ),
        migrations.AlterModelOptions(
            name='ampliconsequencefile',
            options={'verbose_name_plural': 'Amplicon Sequence Files'},
        ),
        migrations.DeleteModel(
            name='Amplicon',
        ),
        migrations.DeleteModel(
            name='Metagenomic',
        ),
    ]

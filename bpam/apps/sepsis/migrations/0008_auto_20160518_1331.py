# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sepsis', '0007_auto_20160518_1040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sepsissample',
            name='strain_description',
            field=models.CharField(max_length=300, null=True, verbose_name=b'Strain Description', blank=True),
        ),
        migrations.AlterField(
            model_name='sepsissample',
            name='strain_or_isolate',
            field=models.CharField(max_length=200, null=True, verbose_name=b'Strain Or Isolate', blank=True),
        ),
        migrations.AlterField(
            model_name='sepsissample',
            name='taxon_or_organism',
            field=models.CharField(max_length=200, null=True, verbose_name=b'Taxon or Organism', blank=True),
        ),
    ]

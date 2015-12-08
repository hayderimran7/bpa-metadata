# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('wheat_cultivars', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cultivarsample',
            name='contact_scientist',
            field=models.ForeignKey(related_name='wheat_cultivars_cultivarsample_sample', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='cultivarsample',
            name='dna_source',
            field=models.ForeignKey(related_name='wheat_cultivars_cultivarsample_sample', verbose_name='DNA Source', blank=True, to='common.DNASource', null=True),
        ),
    ]

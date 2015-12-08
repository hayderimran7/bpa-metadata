# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basesample',
            name='contact_scientist',
            field=models.ForeignKey(related_name='base_basesample_sample', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='basesample',
            name='dna_source',
            field=models.ForeignKey(related_name='base_basesample_sample', verbose_name='DNA Source', blank=True, to='common.DNASource', null=True),
        ),
    ]

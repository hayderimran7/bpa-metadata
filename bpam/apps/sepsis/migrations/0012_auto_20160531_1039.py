# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sepsis', '0011_auto_20160527_1438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proteomicsfile',
            name='method',
            field=models.ForeignKey(related_name='sepsis_proteomicsfile_proteomicsfile', to='sepsis.ProteomicsMethod', null=True),
        ),
    ]

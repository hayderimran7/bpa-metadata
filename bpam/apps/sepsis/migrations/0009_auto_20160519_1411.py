# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sepsis', '0008_auto_20160518_1331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sepsissample',
            name='host',
            field=models.ForeignKey(related_name='samples', blank=True, to='sepsis.Host', null=True),
        ),
    ]

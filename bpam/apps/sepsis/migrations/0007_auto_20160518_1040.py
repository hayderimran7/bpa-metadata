# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sepsis', '0006_auto_20160518_0657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sampletrack',
            name='sample',
            field=models.ForeignKey(related_name='sepsis_sampletrack_track', to='sepsis.SepsisSample'),
        ),
    ]

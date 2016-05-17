# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sepsis', '0005_auto_20160517_0845'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sampletrack',
            options={'verbose_name': 'Sample Tracking Information'},
        ),
    ]

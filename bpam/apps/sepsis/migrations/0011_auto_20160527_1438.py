# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sepsis', '0010_host_strain_or_isolate'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sampletrack',
            options={'verbose_name': 'Sample Tracking Information', 'verbose_name_plural': 'Sample Tracking'},
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marine_microbes', '0012_auto_20160622_1328'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ampliconsequencefile',
            name='lane',
        ),
    ]

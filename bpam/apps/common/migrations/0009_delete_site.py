# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marine_microbes', '0017_auto_20160701_0912'),
        ('common', '0008_auto_20160630_1010'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Site',
        ),
    ]

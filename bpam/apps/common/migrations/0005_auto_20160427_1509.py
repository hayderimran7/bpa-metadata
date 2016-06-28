# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [('common', '0004_bpamirror_order'), ]

    operations = [
        migrations.AlterModelOptions(name='bpamirror',
                                     options={'ordering': ['order']}, ),
    ]

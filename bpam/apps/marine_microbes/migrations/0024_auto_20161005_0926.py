# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marine_microbes', '0023_auto_20160906_2158'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='coastalcontextual',
            options={'verbose_name': 'Coastal Water Contextual Data', 'verbose_name_plural': 'Coastal Water Contextual Data'},
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marine_microbes', '0022_auto_20160901_1258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spongecontextual',
            name='host_abundance',
            field=models.DecimalField(null=True, verbose_name=b'Host Abundance', max_digits=9, decimal_places=6, blank=True),
        ),
    ]

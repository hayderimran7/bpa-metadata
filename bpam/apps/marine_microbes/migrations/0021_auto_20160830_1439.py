# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marine_microbes', '0020_auto_20160829_2353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coastalcontextual',
            name='depth',
            field=models.DecimalField(null=True, verbose_name=b'Depth (m)', max_digits=12, decimal_places=2, blank=True),
        ),
        migrations.AlterField(
            model_name='coralcontextual',
            name='depth',
            field=models.DecimalField(null=True, verbose_name=b'Depth (m)', max_digits=12, decimal_places=2, blank=True),
        ),
        migrations.AlterField(
            model_name='mmsample',
            name='depth',
            field=models.DecimalField(null=True, verbose_name=b'Depth', max_digits=12, decimal_places=2, blank=True),
        ),
        migrations.AlterField(
            model_name='openwatercontextual',
            name='depth',
            field=models.DecimalField(null=True, verbose_name=b'Depth (m)', max_digits=12, decimal_places=2, blank=True),
        ),
        migrations.AlterField(
            model_name='openwatercontextual',
            name='secchi_depth',
            field=models.DecimalField(null=True, verbose_name=b'Secchi Depth (m)', max_digits=12, decimal_places=2, blank=True),
        ),
        migrations.AlterField(
            model_name='seagrasscontextual',
            name='depth',
            field=models.DecimalField(null=True, verbose_name=b'Depth (m)', max_digits=12, decimal_places=2, blank=True),
        ),
        migrations.AlterField(
            model_name='seaweedcontextual',
            name='depth',
            field=models.DecimalField(null=True, verbose_name=b'Depth (m)', max_digits=12, decimal_places=2, blank=True),
        ),
        migrations.AlterField(
            model_name='sedimentcontextual',
            name='depth',
            field=models.DecimalField(null=True, verbose_name=b'Depth (m)', max_digits=12, decimal_places=2, blank=True),
        ),
        migrations.AlterField(
            model_name='spongecontextual',
            name='depth',
            field=models.DecimalField(null=True, verbose_name=b'Depth (m)', max_digits=12, decimal_places=2, blank=True),
        ),
    ]

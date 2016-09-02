# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marine_microbes', '0019_auto_20160714_1005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coralcontextual',
            name='fluoro',
            field=models.DecimalField(null=True, verbose_name=b'Fluorometer Measurement', max_digits=9, decimal_places=6, blank=True),
        ),
        migrations.AlterField(
            model_name='coralcontextual',
            name='host_abundance',
            field=models.DecimalField(null=True, verbose_name=b'Host Abundance', max_digits=9, decimal_places=6, blank=True),
        ),
        migrations.AlterField(
            model_name='coralcontextual',
            name='pam',
            field=models.DecimalField(null=True, verbose_name=b'Pulse amplitude modulated (PAM)', max_digits=9, decimal_places=6, blank=True),
        ),
        migrations.AlterField(
            model_name='seagrasscontextual',
            name='fluoro',
            field=models.DecimalField(null=True, verbose_name=b'Fluorometer Measurement', max_digits=9, decimal_places=6, blank=True),
        ),
        migrations.AlterField(
            model_name='seagrasscontextual',
            name='host_abundance',
            field=models.DecimalField(null=True, verbose_name=b'Host Abundance', max_digits=9, decimal_places=6, blank=True),
        ),
        migrations.AlterField(
            model_name='seagrasscontextual',
            name='pam',
            field=models.DecimalField(null=True, verbose_name=b'Pulse amplitude modulated (PAM)', max_digits=9, decimal_places=6, blank=True),
        ),
        migrations.AlterField(
            model_name='seaweedcontextual',
            name='fluoro',
            field=models.DecimalField(null=True, verbose_name=b'Fluorometer Measurement', max_digits=9, decimal_places=6, blank=True),
        ),
        migrations.AlterField(
            model_name='seaweedcontextual',
            name='host_abundance',
            field=models.DecimalField(null=True, verbose_name=b'Host Abundance', max_digits=9, decimal_places=6, blank=True),
        ),
        migrations.AlterField(
            model_name='seaweedcontextual',
            name='pam',
            field=models.DecimalField(null=True, verbose_name=b'Pulse amplitude modulated (PAM)', max_digits=9, decimal_places=6, blank=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marine_microbes', '0003_auto_20160617_1022'),
    ]

    operations = [
        migrations.AddField(
            model_name='metagenomisequencefile',
            name='flow_cell_id',
            field=models.CharField(default=0, max_length=6, verbose_name=b'Flow Cell ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='metagenomisequencefile',
            name='index',
            field=models.CharField(default=0, max_length=20, verbose_name=b'Index'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='metagenomisequencefile',
            name='library',
            field=models.CharField(default=1, help_text=b'MP or PE', max_length=20, verbose_name=b'Library'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='metagenomisequencefile',
            name='read',
            field=models.CharField(default=1, max_length=3, verbose_name=b'Read'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='metagenomisequencefile',
            name='runsamplenum',
            field=models.CharField(default=1, max_length=20, verbose_name=b'Sample Run Number'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='metagenomisequencefile',
            name='size',
            field=models.CharField(default=1, max_length=100, verbose_name=b'Extraction Size'),
        ),
    ]

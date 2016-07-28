# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sepsis', '0007_auto_20160613_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sepsissample',
            name='culture_collection_date',
            field=models.DateField(help_text=b'YYYY-MM-DD', null=True, verbose_name=b'Collection Date', blank=True),
        ),
        migrations.AlterField(
            model_name='sepsissample',
            name='isolation_source',
            field=models.CharField(max_length=500, null=True, verbose_name=b'Isolation Source', blank=True),
        ),
        migrations.AlterField(
            model_name='sepsissample',
            name='key_virulence_genes',
            field=models.CharField(max_length=500, null=True, verbose_name=b'Key Virulence Genes', blank=True),
        ),
        migrations.AlterField(
            model_name='sepsissample',
            name='serovar',
            field=models.CharField(max_length=500, null=True, verbose_name=b'Serovar', blank=True),
        ),
    ]

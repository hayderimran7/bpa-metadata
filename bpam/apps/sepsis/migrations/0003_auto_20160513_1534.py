# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sepsis', '0002_auto_20160513_1514'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='genomicsmethod',
            options={'verbose_name': 'Genomics Method'},
        ),
        migrations.AlterModelOptions(
            name='host',
            options={'verbose_name': 'Host'},
        ),
        migrations.AlterModelOptions(
            name='proteomicsmethod',
            options={'verbose_name': 'Proteomics Method'},
        ),
        migrations.AlterModelOptions(
            name='transcriptomicsmethod',
            options={'verbose_name': 'Growth Method'},
        ),
        migrations.RenameField(
            model_name='host',
            old_name='host_age',
            new_name='age',
        ),
        migrations.RenameField(
            model_name='host',
            old_name='host_description',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='host',
            old_name='host_disease_outcome',
            new_name='disease_outcome',
        ),
        migrations.RenameField(
            model_name='host',
            old_name='host_dob',
            new_name='dob',
        ),
        migrations.RenameField(
            model_name='host',
            old_name='host_location',
            new_name='location',
        ),
        migrations.RenameField(
            model_name='host',
            old_name='host_sex',
            new_name='sex',
        ),
    ]

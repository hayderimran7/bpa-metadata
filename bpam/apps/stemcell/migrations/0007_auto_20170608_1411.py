# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stemcell', '0006_auto_20170515_1607'),
    ]

    operations = [
        migrations.RenameField(
            model_name='metabolomictrack',
            old_name='data_set_id',
            new_name='dataset_id',
        ),
        migrations.RenameField(
            model_name='proteomictrack',
            old_name='data_set_id',
            new_name='dataset_id',
        ),
        migrations.RenameField(
            model_name='singlecellrnaseqtrack',
            old_name='data_set_id',
            new_name='dataset_id',
        ),
        migrations.RenameField(
            model_name='smallrnatrack',
            old_name='data_set_id',
            new_name='dataset_id',
        ),
        migrations.RenameField(
            model_name='transcriptometrack',
            old_name='data_set_id',
            new_name='dataset_id',
        ),
    ]

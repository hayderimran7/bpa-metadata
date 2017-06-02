# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marine_microbes', '0029_auto_20170403_1437'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ampliconsequencefile',
            name='sample',
        ),
        migrations.RemoveField(
            model_name='ampliconsequencefile',
            name='url_verification',
        ),
        migrations.RemoveField(
            model_name='metagenomicsequencefile',
            name='sample',
        ),
        migrations.RemoveField(
            model_name='metagenomicsequencefile',
            name='url_verification',
        ),
        migrations.DeleteModel(
            name='AmpliconSequenceFile',
        ),
        migrations.DeleteModel(
            name='MetagenomicSequenceFile',
        ),
    ]

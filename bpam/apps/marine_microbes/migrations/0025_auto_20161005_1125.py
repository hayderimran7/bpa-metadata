# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marine_microbes', '0024_auto_20161005_0926'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='samplestatetrack',
            name='amplicon_ITS_data_generated',
        ),
        migrations.AddField(
            model_name='samplestatetrack',
            name='amplicon_a16s_data_generated',
            field=models.BooleanField(default=False, verbose_name=b'Amplicon A16S Data Generated'),
        ),
        migrations.AlterField(
            model_name='ampliconsequencefile',
            name='amplicon',
            field=models.CharField(max_length=4, verbose_name=b'Amplicon', choices=[(b'16S', b'16S'), (b'18S', b'18S'), (b'A16S', b'A16S')]),
        ),
    ]

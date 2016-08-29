# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('sepsis', '0020_auto_20160824_1322'),
    ]

    operations = [
        migrations.AddField(
            model_name='deeplcmstrack',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 25, 14, 4, 7, 555198, tzinfo=utc), auto_now=True), preserve_default=False,),
        migrations.AddField(
            model_name='genomicsmiseqfile',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 25, 14, 4, 14, 893113, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='genomicspacbiofile',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 25, 14, 4, 18, 948512, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='growthmethod',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 25, 14, 4, 24, 894584, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='host',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 25, 14, 4, 33, 447192, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='metabolomicstrack',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 25, 14, 4, 38, 487932, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='miseqgenomicsmethod',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 25, 14, 4, 45, 932, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='miseqtrack',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 25, 14, 4, 50, 395851, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pacbiogenomicsmethod',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 25, 14, 4, 55, 959789, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pacbiotrack',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 25, 14, 5, 2, 782599, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='proteomicsfile',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 25, 14, 5, 7, 472949, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='proteomicsmethod',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 25, 14, 5, 24, 658140, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rnahiseqtrack',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 25, 14, 5, 27, 973797, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sepsissample',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 25, 13, 59, 32, 954419, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='swathmstrack',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 25, 14, 5, 35, 163558, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transcriptomicsfile',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 25, 14, 5, 37, 850430, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transcriptomicsmethod',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 25, 14, 5, 40, 393353, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]

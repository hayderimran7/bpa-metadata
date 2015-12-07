# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('base_454', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sample454',
            name='submitter',
            field=models.ForeignKey(verbose_name='Submitter', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]

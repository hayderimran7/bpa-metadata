# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0005_auto_20160427_1509'),
        ('sepsis', '0003_auto_20160516_1526'),
    ]

    operations = [
        migrations.CreateModel(
            name='SampleTrack',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('given_to', models.CharField(help_text=b'Sample was delivered to', max_length=200, null=True, verbose_name=b'Given To', blank=True)),
                ('date_allocated', models.DateField(help_text=b'DD/MM/YY', null=True, verbose_name=b'Allocation Date', blank=True)),
                ('work_order', models.CharField(max_length=50, null=True, verbose_name=b'Work Order', blank=True)),
                ('replicate', models.IntegerField(null=True, verbose_name=b'Replicate', blank=True)),
                ('omics', models.CharField(max_length=50, null=True, verbose_name=b'Omics Type', blank=True)),
                ('analytical_platform', models.CharField(max_length=100, null=True, verbose_name=b'Analytical Platform', blank=True)),
                ('sample_submission_date', models.DateField(help_text=b'DD/MM/YY', null=True, verbose_name=b'Sample Submission Date', blank=True)),
                ('contextual_data_submission_date', models.DateField(help_text=b'DD/MM/YY', null=True, verbose_name=b'Contextual Data Submission Date', blank=True)),
                ('data_generated', models.BooleanField(default=False, verbose_name=b'Data generated')),
                ('facility', models.ForeignKey(blank=True, to='common.Facility', null=True)),
                ('sample', models.ForeignKey(to='sepsis.SepsisSample')),
            ],
        ),
    ]

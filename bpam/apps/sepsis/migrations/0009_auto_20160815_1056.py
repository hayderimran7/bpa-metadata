# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sepsis', '0008_auto_20160728_1606'),
    ]

    operations = [
        migrations.AddField(
            model_name='host',
            name='host_associated',
            field=models.CharField(max_length=200, null=True, verbose_name=b'Host Associated', blank=True),
        ),
        migrations.AddField(
            model_name='host',
            name='host_disease_status',
            field=models.CharField(max_length=200, null=True, verbose_name=b'Host Disease Status', blank=True),
        ),
        migrations.AddField(
            model_name='host',
            name='host_health_state',
            field=models.CharField(max_length=200, null=True, verbose_name=b'Host Health State', blank=True),
        ),
        migrations.AddField(
            model_name='sepsissample',
            name='collected_by',
            field=models.CharField(max_length=200, null=True, verbose_name=b'Collected By', blank=True),
        ),
        migrations.AddField(
            model_name='sepsissample',
            name='estimated_size',
            field=models.CharField(max_length=200, null=True, verbose_name=b'Estimated Size', blank=True),
        ),
        migrations.AddField(
            model_name='sepsissample',
            name='investigation_type',
            field=models.CharField(max_length=200, null=True, verbose_name=b'Investigation Type', blank=True),
        ),
        migrations.AddField(
            model_name='sepsissample',
            name='isolation_growth_conditions',
            field=models.CharField(max_length=500, null=True, verbose_name=b'Isolation Growth Conditions', blank=True),
        ),
        migrations.AddField(
            model_name='sepsissample',
            name='num_replicons',
            field=models.CharField(max_length=200, null=True, verbose_name=b'Number of Replicons', blank=True),
        ),
        migrations.AddField(
            model_name='sepsissample',
            name='ploidy',
            field=models.CharField(max_length=200, null=True, verbose_name=b'Ploidy', blank=True),
        ),
        migrations.AddField(
            model_name='sepsissample',
            name='project_name',
            field=models.CharField(max_length=200, null=True, verbose_name=b'Project Name', blank=True),
        ),
        migrations.AddField(
            model_name='sepsissample',
            name='propagation',
            field=models.CharField(max_length=200, null=True, verbose_name=b'Propagation', blank=True),
        ),
        migrations.AddField(
            model_name='sepsissample',
            name='sample_title',
            field=models.CharField(max_length=200, null=True, verbose_name=b'Sample Title', blank=True),
        ),
        migrations.AddField(
            model_name='sepsissample',
            name='study_title',
            field=models.CharField(max_length=200, null=True, verbose_name=b'Study Title', blank=True),
        ),
    ]

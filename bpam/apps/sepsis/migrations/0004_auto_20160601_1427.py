# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sepsis', '0003_auto_20160601_1349'),
    ]

    operations = [
        migrations.CreateModel(
            name='GrowthMethod',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('note', models.TextField(max_length=200, null=True, verbose_name=b'Note', blank=True)),
                ('growth_condition_temperature', models.IntegerField(help_text=b'Degrees Centigrade', null=True, verbose_name=b'Growth condition temperature', blank=True)),
                ('growth_condition_time', models.IntegerField(help_text=b'Hours', null=True, verbose_name=b'Growth condition time', blank=True)),
                ('growth_condition_media', models.CharField(max_length=200, null=True, verbose_name=b'Growth condition media', blank=True)),
            ],
            options={
                'verbose_name': 'Growth Method',
            },
        ),
        migrations.AlterModelOptions(
            name='transcriptomicsmethod',
            options={},
        ),
        migrations.RemoveField(
            model_name='genomicsmethod',
            name='growth_condition_media',
        ),
        migrations.RemoveField(
            model_name='genomicsmethod',
            name='growth_condition_temperature',
        ),
        migrations.RemoveField(
            model_name='genomicsmethod',
            name='growth_condition_time',
        ),
        migrations.RemoveField(
            model_name='genomicsmethod',
            name='note',
        ),
        migrations.RemoveField(
            model_name='proteomicsmethod',
            name='growth_condition_media',
        ),
        migrations.RemoveField(
            model_name='proteomicsmethod',
            name='growth_condition_temperature',
        ),
        migrations.RemoveField(
            model_name='proteomicsmethod',
            name='growth_condition_time',
        ),
        migrations.RemoveField(
            model_name='proteomicsmethod',
            name='note',
        ),
        migrations.RemoveField(
            model_name='transcriptomicsmethod',
            name='growth_condition_media',
        ),
        migrations.RemoveField(
            model_name='transcriptomicsmethod',
            name='growth_condition_temperature',
        ),
        migrations.RemoveField(
            model_name='transcriptomicsmethod',
            name='growth_condition_time',
        ),
        migrations.RemoveField(
            model_name='transcriptomicsmethod',
            name='note',
        ),
        migrations.AddField(
            model_name='genomicsmethod',
            name='analysis_software_version',
            field=models.CharField(max_length=20, null=True, verbose_name=b'RS Version', blank=True),
        ),
        migrations.AlterField(
            model_name='sepsissample',
            name='bpa_id',
            field=models.OneToOneField(verbose_name=b'BPA ID', to='common.BPAUniqueID', help_text=b'Bioplatforms Australia Sample ID'),
        ),
        migrations.AlterField(
            model_name='sepsissample',
            name='host',
            field=models.ForeignKey(related_name='samples', blank=True, to='sepsis.Host', help_text=b'Sample donor host', null=True),
        ),
        migrations.AddField(
            model_name='sepsissample',
            name='growt_method',
            field=models.ForeignKey(related_name='samples', blank=True, to='sepsis.GrowthMethod', help_text=b'Sample Growth Method', null=True),
        ),
    ]

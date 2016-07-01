# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('marine_microbes', '0016_ampliconsequencefile_number_of_reads'),
    ]

    operations = [
        migrations.CreateModel(
            name='MMSite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField(unique=True, verbose_name=b'Location Description')),
                ('point', django.contrib.gis.db.models.fields.PointField(help_text=b'Represented as (longitude, latitude)', srid=4326, verbose_name=b'Position')),
                ('note', models.TextField(null=True, verbose_name=b'Note', blank=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Sample Collection Site',
                'verbose_name_plural': 'Sample Collection Sites',
            },
        ),
        migrations.AlterField(
            model_name='coralcontextual',
            name='site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='marine_microbes.MMSite', null=True),
        ),
        migrations.AlterField(
            model_name='mmsample',
            name='site',
            field=models.ForeignKey(to='marine_microbes.MMSite', null=True),
        ),
        migrations.AlterField(
            model_name='openwatercontextual',
            name='site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='marine_microbes.MMSite', null=True),
        ),
        migrations.AlterField(
            model_name='pelagiccontextual',
            name='site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='marine_microbes.MMSite', null=True),
        ),
        migrations.AlterField(
            model_name='seagrasscontextual',
            name='site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='marine_microbes.MMSite', null=True),
        ),
        migrations.AlterField(
            model_name='seaweedcontextual',
            name='site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='marine_microbes.MMSite', null=True),
        ),
        migrations.AlterField(
            model_name='sedimentcontextual',
            name='site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='marine_microbes.MMSite', null=True),
        ),
        migrations.AlterField(
            model_name='spongecontextual',
            name='site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='marine_microbes.MMSite', null=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [('base', '0001_initial'), ]

    operations = [
        migrations.CreateModel(
            name='OperationalTaxonomicUnit',
            fields=[
                ('id', models.AutoField(
                    verbose_name='ID', serialize=False,
                    auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('kingdom', models.CharField(db_index=True,
                                             max_length=100,
                                             verbose_name='Kingdom',
                                             choices=[(b'Bacteria', b'Bacteria'), (b'Archaea', b'Archaea'), (
                                                 b'Eukaryota', b'Eukaryota'), (b'Fungi', b'Fungi')])),
                ('phylum', models.CharField(
                    default=b'undefined', max_length=100,
                    verbose_name='Phylum', db_index=True)),
                ('otu_class', models.CharField(
                    default=b'undefined', max_length=100,
                    verbose_name='Class', db_index=True)),
                ('order', models.CharField(
                    default=b'undefined', max_length=100,
                    verbose_name='Order', db_index=True)),
                ('family', models.CharField(
                    default=b'undefined', max_length=100,
                    verbose_name='Family', db_index=True)),
                ('genus', models.CharField(
                    default=b'undefined', max_length=100,
                    verbose_name='Genus', db_index=True)),
                ('species', models.CharField(
                    default=b'undefined', max_length=100,
                    verbose_name='Species', db_index=True)),
            ],
            options={
                'verbose_name_plural': 'OTU',
            }, ),
        migrations.CreateModel(
            name='SampleOTU',
            fields=[
                ('id', models.AutoField(
                    verbose_name='ID', serialize=False,
                    auto_created=True, primary_key=True)),
                ('count', models.IntegerField(verbose_name='OTU Count')),
                ('otu', models.ForeignKey(to='base_otu.OperationalTaxonomicUnit')),
                ('sample', models.ForeignKey(to='base.BASESample')),
            ],
            options={
                'verbose_name_plural': 'OTU to Sample Links',
            }, ),
        migrations.AlterUniqueTogether(name='operationaltaxonomicunit',
                                       unique_together=set([('kingdom', 'name')]), ),
    ]

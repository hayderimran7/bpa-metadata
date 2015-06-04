# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '__first__'),
        ('common', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='MetagenomicsRun',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('DNA_extraction_protocol', models.CharField(max_length=200, verbose_name='DNA Extraction Protocol', blank=True)),
                ('passage_number', models.IntegerField(null=True, verbose_name='Passage Number', blank=True)),
                ('run_number', models.IntegerField(null=True, blank=True)),
                ('flow_cell_id', models.CharField(max_length=10, verbose_name='Flow Cell ID', blank=True)),
                ('array_analysis_facility', models.ForeignKey(related_name='+', verbose_name='Array Analysis', blank=True, to='common.Facility', null=True)),
            ],
            options={
                'verbose_name_plural': 'Metagenomics Run',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MetagenomicsSample',
            fields=[
                ('basesample_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='base.BASESample')),
            ],
            options={
                'verbose_name_plural': 'Metagenomics Sample',
            },
            bases=('base.basesample',),
        ),
        migrations.CreateModel(
            name='MetagenomicsSequenceFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('index_number', models.IntegerField(null=True, verbose_name='Index', blank=True)),
                ('lane_number', models.IntegerField(null=True, verbose_name='Lane', blank=True)),
                ('date_received_from_sequencing_facility', models.DateField(null=True, blank=True)),
                ('filename', models.CharField(max_length=300, null=True, verbose_name='File Name', blank=True)),
                ('md5', models.CharField(max_length=32, null=True, verbose_name='MD5 Checksum', blank=True)),
                ('analysed', models.NullBooleanField(default=False)),
                ('note', models.TextField(blank=True)),
                ('run', models.ForeignKey(to='base_metagenomics.MetagenomicsRun', null=True)),
                ('sample', models.ForeignKey(to='base_metagenomics.MetagenomicsSample')),
                ('url_verification', models.ForeignKey(to='common.URLVerification', null=True)),
            ],
            options={
                'verbose_name_plural': 'Metagenomics Sequence Files',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='metagenomicsrun',
            name='sample',
            field=models.ForeignKey(to='base_metagenomics.MetagenomicsSample'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='metagenomicsrun',
            name='sequencer',
            field=models.ForeignKey(blank=True, to='common.Sequencer', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='metagenomicsrun',
            name='sequencing_facility',
            field=models.ForeignKey(related_name='+', verbose_name='Sequencing', blank=True, to='common.Facility', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='metagenomicsrun',
            name='whole_genome_sequencing_facility',
            field=models.ForeignKey(related_name='+', verbose_name='Whole Genome', blank=True, to='common.Facility', null=True),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Extraction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('extraction_id', models.CharField(max_length=64, verbose_name='Extraction ID')),
                ('library_construction_protocol', models.CharField(max_length=64, null=True, verbose_name='Library Construction Protocol', blank=True)),
                ('sequencer', models.CharField(max_length=64, null=True, verbose_name='Sequencer', blank=True)),
                ('casava_version', models.CharField(max_length=16, null=True, verbose_name='Casava Version', blank=True)),
                ('insert_size_range', models.CharField(max_length=64, null=True, verbose_name='Insert Size Range', blank=True)),
                ('note', models.TextField(blank=True)),
            ],
            options={
                'verbose_name_plural': 'Metagenomics Extractions',
            },
        ),
        migrations.CreateModel(
            name='MetagenomicsProtocol',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('library_type', models.CharField(max_length=2, verbose_name='Type', choices=[(b'PE', b'Paired End'), (b'SE', b'Single End'), (b'MP', b'Mate Pair'), (b'UN', b'Unknown')])),
                ('library_construction', models.CharField(max_length=200, null=True, verbose_name='Construction', blank=True)),
                ('base_pairs', models.IntegerField(null=True, verbose_name='Base Pairs', blank=True)),
                ('library_construction_protocol', models.TextField(verbose_name='Construction Protocol')),
                ('note', models.TextField(blank=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Protocol',
                'verbose_name_plural': 'Protocol',
            },
        ),
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
                ('read_number', models.IntegerField(null=True, verbose_name='Read', blank=True)),
                ('date_received_from_sequencing_facility', models.DateField(null=True, blank=True)),
                ('filename', models.CharField(max_length=300, null=True, verbose_name='File Name', blank=True)),
                ('md5', models.CharField(max_length=32, null=True, verbose_name='MD5 Checksum', blank=True)),
                ('analysed', models.NullBooleanField(default=False)),
                ('note', models.TextField(blank=True)),
                ('index', models.CharField(max_length=32, null=True, verbose_name='Index', blank=True)),
                ('extraction', models.ForeignKey(to='base_metagenomics.Extraction', null=True)),
                ('protocol', models.ForeignKey(to='base_metagenomics.MetagenomicsProtocol', null=True)),
                ('run', models.ForeignKey(to='base_metagenomics.MetagenomicsRun', null=True)),
                ('sample', models.ForeignKey(to='base_metagenomics.MetagenomicsSample')),
                ('url_verification', models.ForeignKey(related_name='base_metagenomics_metagenomicssequencefile_related', to='common.URLVerification', null=True)),
            ],
            options={
                'verbose_name_plural': 'Metagenomics Sequence Files',
            },
        ),
        migrations.AddField(
            model_name='metagenomicsrun',
            name='sample',
            field=models.ForeignKey(to='base_metagenomics.MetagenomicsSample'),
        ),
        migrations.AddField(
            model_name='metagenomicsrun',
            name='sequencer',
            field=models.ForeignKey(blank=True, to='common.Sequencer', null=True),
        ),
        migrations.AddField(
            model_name='metagenomicsrun',
            name='sequencing_facility',
            field=models.ForeignKey(related_name='+', verbose_name='Sequencing', blank=True, to='common.Facility', null=True),
        ),
        migrations.AddField(
            model_name='metagenomicsrun',
            name='whole_genome_sequencing_facility',
            field=models.ForeignKey(related_name='+', verbose_name='Whole Genome', blank=True, to='common.Facility', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='metagenomicsprotocol',
            unique_together=set([('library_type', 'base_pairs', 'library_construction_protocol')]),
        ),
        migrations.AddField(
            model_name='extraction',
            name='sample',
            field=models.ForeignKey(to='base_metagenomics.MetagenomicsSample'),
        ),
        migrations.AlterUniqueTogether(
            name='extraction',
            unique_together=set([('sample', 'extraction_id')]),
        ),
    ]

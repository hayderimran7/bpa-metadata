# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BASESample',
            fields=[
                ('bpa_id', models.OneToOneField(primary_key=True, serialize=False, to='common.BPAUniqueID', verbose_name='BPA ID')),
                ('name', models.CharField(max_length=200, verbose_name='Sample Name')),
                ('dna_extraction_protocol', models.TextField(null=True, verbose_name='DNA Extraction Protocol', blank=True)),
                ('requested_sequence_coverage', models.CharField(max_length=50, blank=True)),
                ('collection_date', models.DateField(null=True, verbose_name='Collection Date', blank=True)),
                ('date_sent_to_sequencing_facility', models.DateField(null=True, verbose_name='Date sent to sequencing facility', blank=True)),
                ('note', models.TextField(null=True, verbose_name='Note', blank=True)),
                ('debug_note', models.TextField(null=True, verbose_name='Original Data', blank=True)),
                ('contact_scientist', models.ForeignKey(related_name='base_basesample_sample', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('dna_source', models.ForeignKey(related_name='base_basesample_sample', verbose_name='DNA Source', blank=True, to='common.DNASource', null=True)),
            ],
            options={
                'verbose_name_plural': 'Biome of Australia Soil Environment Samples',
            },
        ),
    ]

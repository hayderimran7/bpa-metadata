# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wheat_pathogens', '0002_auto_20160531_1501'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='pathogenprotocol',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='pathogenprotocol',
            name='run',
        ),
        migrations.RemoveField(
            model_name='pathogenrun',
            name='array_analysis_facility',
        ),
        migrations.RemoveField(
            model_name='pathogenrun',
            name='protocol',
        ),
        migrations.RemoveField(
            model_name='pathogenrun',
            name='sample',
        ),
        migrations.RemoveField(
            model_name='pathogenrun',
            name='sequencer',
        ),
        migrations.RemoveField(
            model_name='pathogenrun',
            name='sequencing_facility',
        ),
        migrations.RemoveField(
            model_name='pathogenrun',
            name='whole_genome_sequencing_facility',
        ),
        migrations.RemoveField(
            model_name='pathogensample',
            name='bpa_id',
        ),
        migrations.RemoveField(
            model_name='pathogensample',
            name='contact_scientist',
        ),
        migrations.RemoveField(
            model_name='pathogensample',
            name='dna_source',
        ),
        migrations.RemoveField(
            model_name='pathogensample',
            name='organism',
        ),
        migrations.RemoveField(
            model_name='pathogensequencefile',
            name='run',
        ),
        migrations.RemoveField(
            model_name='pathogensequencefile',
            name='sample',
        ),
        migrations.RemoveField(
            model_name='pathogensequencefile',
            name='url_verification',
        ),
        migrations.DeleteModel(
            name='PathogenProtocol',
        ),
        migrations.DeleteModel(
            name='PathogenRun',
        ),
        migrations.DeleteModel(
            name='PathogenSample',
        ),
        migrations.DeleteModel(
            name='PathogenSequenceFile',
        ),
    ]

# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TumorStage'
        db.create_table(u'melanoma_tumorstage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'melanoma', ['TumorStage'])

        # Adding model 'Array'
        db.create_table(u'melanoma_array', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bpa_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.BPAUniqueID'])),
            ('array_id', self.gf('django.db.models.fields.CharField')(max_length=17)),
            ('batch_number', self.gf('django.db.models.fields.IntegerField')()),
            ('well_id', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('mia_id', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('call_rate', self.gf('django.db.models.fields.FloatField')()),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'melanoma', ['Array'])

        # Adding model 'MelanomaSample'
        db.create_table(u'melanoma_melanomasample', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bpa_id', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['common.BPAUniqueID'], unique=True)),
            ('contact_scientist', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bpaauth.BPAUser'], null=True, blank=True)),
            ('dna_source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.DNASource'], null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('dna_extraction_protocol', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('requested_sequence_coverage', self.gf('django.db.models.fields.CharField')(max_length=6, blank=True)),
            ('collection_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('date_sent_to_sequencing_facility', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('debug_note', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('organism', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Organism'])),
            ('passage_number', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
            ('tumor_stage', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['melanoma.TumorStage'], null=True)),
            ('histological_subtype', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
        ))
        db.send_create_signal(u'melanoma', ['MelanomaSample'])

        # Adding model 'MelanomaRun'
        db.create_table(u'melanoma_melanomarun', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('DNA_extraction_protocol', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('passage_number', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('sequencing_facility', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['common.Facility'])),
            ('whole_genome_sequencing_facility', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['common.Facility'])),
            ('array_analysis_facility', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['common.Facility'])),
            ('sequencer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Sequencer'])),
            ('run_number', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('flow_cell_id', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('sample', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['melanoma.MelanomaSample'])),
        ))
        db.send_create_signal(u'melanoma', ['MelanomaRun'])

        # Adding model 'MelanomaProtocol'
        db.create_table(u'melanoma_melanomaprotocol', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('library_type', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('base_pairs', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('library_construction_protocol', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('run', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['melanoma.MelanomaRun'], unique=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'melanoma', ['MelanomaProtocol'])

        # Adding unique constraint on 'MelanomaProtocol', fields ['library_type', 'base_pairs', 'library_construction_protocol']
        db.create_unique(u'melanoma_melanomaprotocol', ['library_type', 'base_pairs', 'library_construction_protocol'])

        # Adding model 'MelanomaSequenceFile'
        db.create_table(u'melanoma_melanomasequencefile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('index_number', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('lane_number', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('date_received_from_sequencing_facility', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('filename', self.gf('django.db.models.fields.CharField')(max_length=300, null=True, blank=True)),
            ('md5', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('analysed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('sample', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['melanoma.MelanomaSample'])),
            ('run', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['melanoma.MelanomaRun'])),
            ('url_verification', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['common.URLVerification'], unique=True, null=True)),
        ))
        db.send_create_signal(u'melanoma', ['MelanomaSequenceFile'])


    def backwards(self, orm):
        # Removing unique constraint on 'MelanomaProtocol', fields ['library_type', 'base_pairs', 'library_construction_protocol']
        db.delete_unique(u'melanoma_melanomaprotocol', ['library_type', 'base_pairs', 'library_construction_protocol'])

        # Deleting model 'TumorStage'
        db.delete_table(u'melanoma_tumorstage')

        # Deleting model 'Array'
        db.delete_table(u'melanoma_array')

        # Deleting model 'MelanomaSample'
        db.delete_table(u'melanoma_melanomasample')

        # Deleting model 'MelanomaRun'
        db.delete_table(u'melanoma_melanomarun')

        # Deleting model 'MelanomaProtocol'
        db.delete_table(u'melanoma_melanomaprotocol')

        # Deleting model 'MelanomaSequenceFile'
        db.delete_table(u'melanoma_melanomasequencefile')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'bpaauth.bpauser': {
            'Meta': {'object_name': 'BPAUser'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interest': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lab': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'organisation': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'project': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'common.bpaproject': {
            'Meta': {'object_name': 'BPAProject'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'blank': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '30', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'note': ('tinymce.models.HTMLField', [], {'blank': 'True'})
        },
        u'common.bpauniqueid': {
            'Meta': {'object_name': 'BPAUniqueID'},
            'bpa_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200', 'primary_key': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.BPAProject']"})
        },
        u'common.dnasource': {
            'Meta': {'object_name': 'DNASource'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'common.facility': {
            'Meta': {'object_name': 'Facility'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'common.organism': {
            'Meta': {'object_name': 'Organism'},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'family': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'genus': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kingdom': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'ncbi_classification': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'order': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'organism_class': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'phylum': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'species': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'common.sequencer': {
            'Meta': {'object_name': 'Sequencer'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'primary_key': 'True'})
        },
        u'common.urlverification': {
            'Meta': {'object_name': 'URLVerification'},
            'checked_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'checked_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status_note': ('django.db.models.fields.TextField', [], {}),
            'status_ok': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'melanoma.array': {
            'Meta': {'object_name': 'Array'},
            'array_id': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'batch_number': ('django.db.models.fields.IntegerField', [], {}),
            'bpa_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.BPAUniqueID']"}),
            'call_rate': ('django.db.models.fields.FloatField', [], {}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mia_id': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'well_id': ('django.db.models.fields.CharField', [], {'max_length': '4'})
        },
        u'melanoma.melanomaprotocol': {
            'Meta': {'unique_together': "(('library_type', 'base_pairs', 'library_construction_protocol'),)", 'object_name': 'MelanomaProtocol'},
            'base_pairs': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'library_construction_protocol': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'library_type': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'run': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['melanoma.MelanomaRun']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'melanoma.melanomarun': {
            'DNA_extraction_protocol': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'Meta': {'object_name': 'MelanomaRun'},
            'array_analysis_facility': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['common.Facility']"}),
            'flow_cell_id': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'passage_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'run_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sample': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['melanoma.MelanomaSample']"}),
            'sequencer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.Sequencer']"}),
            'sequencing_facility': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['common.Facility']"}),
            'whole_genome_sequencing_facility': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['common.Facility']"})
        },
        u'melanoma.melanomasample': {
            'Meta': {'object_name': 'MelanomaSample'},
            'bpa_id': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['common.BPAUniqueID']", 'unique': 'True'}),
            'collection_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'contact_scientist': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bpaauth.BPAUser']", 'null': 'True', 'blank': 'True'}),
            'date_sent_to_sequencing_facility': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'debug_note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'dna_extraction_protocol': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'dna_source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.DNASource']", 'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'histological_subtype': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'organism': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.Organism']"}),
            'passage_number': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'requested_sequence_coverage': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            'tumor_stage': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['melanoma.TumorStage']", 'null': 'True'})
        },
        u'melanoma.melanomasequencefile': {
            'Meta': {'object_name': 'MelanomaSequenceFile'},
            'analysed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date_received_from_sequencing_facility': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'lane_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'md5': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'run': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['melanoma.MelanomaRun']"}),
            'sample': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['melanoma.MelanomaSample']"}),
            'url_verification': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['common.URLVerification']", 'unique': 'True', 'null': 'True'})
        },
        u'melanoma.tumorstage': {
            'Meta': {'object_name': 'TumorStage'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['melanoma']
# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CultivarSample'
        db.create_table(u'wheat_cultivars_cultivarsample', (
            ('bpa_id', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['common.BPAUniqueID'], unique=True, primary_key=True)),
            ('contact_scientist', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bpaauth.BPAUser'], null=True, blank=True)),
            ('dna_source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.DNASource'], null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('dna_extraction_protocol', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('requested_sequence_coverage', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('collection_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('date_sent_to_sequencing_facility', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('debug_note', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('organism', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Organism'])),
            ('sample_label', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('cultivar_code', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
            ('extract_name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('protocol_reference', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('casava_version', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
        ))
        db.send_create_signal(u'wheat_cultivars', ['CultivarSample'])

        # Adding model 'CultivarProtocol'
        db.create_table(u'wheat_cultivars_cultivarprotocol', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('library_type', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('library_construction', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('base_pairs', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('library_construction_protocol', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('run', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wheat_cultivars.CultivarRun'], null=True, blank=True)),
        ))
        db.send_create_signal(u'wheat_cultivars', ['CultivarProtocol'])

        # Adding unique constraint on 'CultivarProtocol', fields ['library_type', 'base_pairs', 'library_construction_protocol']
        db.create_unique(u'wheat_cultivars_cultivarprotocol', ['library_type', 'base_pairs', 'library_construction_protocol'])

        # Adding model 'CultivarRun'
        db.create_table(u'wheat_cultivars_cultivarrun', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('DNA_extraction_protocol', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('passage_number', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('sequencing_facility', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['common.Facility'])),
            ('whole_genome_sequencing_facility', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['common.Facility'])),
            ('array_analysis_facility', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['common.Facility'])),
            ('sequencer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Sequencer'], null=True, blank=True)),
            ('run_number', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('flow_cell_id', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('sample', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wheat_cultivars.CultivarSample'])),
            ('protocol', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wheat_cultivars.CultivarProtocol'], null=True, blank=True)),
        ))
        db.send_create_signal(u'wheat_cultivars', ['CultivarRun'])

        # Adding model 'CultivarSequenceFile'
        db.create_table(u'wheat_cultivars_cultivarsequencefile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('index_number', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('lane_number', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('date_received_from_sequencing_facility', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('filename', self.gf('django.db.models.fields.CharField')(max_length=300, null=True, blank=True)),
            ('md5', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('analysed', self.gf('django.db.models.fields.NullBooleanField')(default=False, null=True, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('url_verification', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['common.URLVerification'], unique=True, null=True)),
            ('sample', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wheat_cultivars.CultivarSample'])),
            ('run', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wheat_cultivars.CultivarRun'])),
            ('original_sequence_filename', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal(u'wheat_cultivars', ['CultivarSequenceFile'])


    def backwards(self, orm):
        # Removing unique constraint on 'CultivarProtocol', fields ['library_type', 'base_pairs', 'library_construction_protocol']
        db.delete_unique(u'wheat_cultivars_cultivarprotocol', ['library_type', 'base_pairs', 'library_construction_protocol'])

        # Deleting model 'CultivarSample'
        db.delete_table(u'wheat_cultivars_cultivarsample')

        # Deleting model 'CultivarProtocol'
        db.delete_table(u'wheat_cultivars_cultivarprotocol')

        # Deleting model 'CultivarRun'
        db.delete_table(u'wheat_cultivars_cultivarrun')

        # Deleting model 'CultivarSequenceFile'
        db.delete_table(u'wheat_cultivars_cultivarsequencefile')


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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
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
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'common.bpaproject': {
            'Meta': {'object_name': 'BPAProject'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'blank': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '30', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'})
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
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
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
            'status_ok': ('django.db.models.fields.BooleanField', [], {})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'wheat_cultivars.cultivarprotocol': {
            'Meta': {'unique_together': "(('library_type', 'base_pairs', 'library_construction_protocol'),)", 'object_name': 'CultivarProtocol'},
            'base_pairs': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'library_construction': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'library_construction_protocol': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'library_type': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'run': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['wheat_cultivars.CultivarRun']", 'null': 'True', 'blank': 'True'})
        },
        u'wheat_cultivars.cultivarrun': {
            'DNA_extraction_protocol': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'Meta': {'object_name': 'CultivarRun'},
            'array_analysis_facility': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['common.Facility']"}),
            'flow_cell_id': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'passage_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'protocol': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['wheat_cultivars.CultivarProtocol']", 'null': 'True', 'blank': 'True'}),
            'run_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sample': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['wheat_cultivars.CultivarSample']"}),
            'sequencer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.Sequencer']", 'null': 'True', 'blank': 'True'}),
            'sequencing_facility': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['common.Facility']"}),
            'whole_genome_sequencing_facility': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['common.Facility']"})
        },
        u'wheat_cultivars.cultivarsample': {
            'Meta': {'object_name': 'CultivarSample'},
            'bpa_id': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['common.BPAUniqueID']", 'unique': 'True', 'primary_key': 'True'}),
            'casava_version': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'collection_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'contact_scientist': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bpaauth.BPAUser']", 'null': 'True', 'blank': 'True'}),
            'cultivar_code': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'date_sent_to_sequencing_facility': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'debug_note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'dna_extraction_protocol': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'dna_source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.DNASource']", 'null': 'True', 'blank': 'True'}),
            'extract_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'organism': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.Organism']"}),
            'protocol_reference': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'requested_sequence_coverage': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'sample_label': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'wheat_cultivars.cultivarsequencefile': {
            'Meta': {'object_name': 'CultivarSequenceFile'},
            'analysed': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'date_received_from_sequencing_facility': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'lane_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'md5': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'original_sequence_filename': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'run': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['wheat_cultivars.CultivarRun']"}),
            'sample': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['wheat_cultivars.CultivarSample']"}),
            'url_verification': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['common.URLVerification']", 'unique': 'True', 'null': 'True'})
        }
    }

    complete_apps = ['wheat_cultivars']
# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BPAProject'
        db.create_table(u'common_bpaproject', (
            ('key', self.gf('django.db.models.fields.CharField')(max_length=30, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=2000, blank=True)),
            ('note', self.gf('tinymce.models.HTMLField')(blank=True)),
        ))
        db.send_create_signal(u'common', ['BPAProject'])

        # Adding model 'BPAUniqueID'
        db.create_table(u'common_bpauniqueid', (
            ('bpa_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200, primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.BPAProject'])),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'common', ['BPAUniqueID'])

        # Adding model 'Facility'
        db.create_table(u'common_facility', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'common', ['Facility'])

        # Adding model 'Organism'
        db.create_table(u'common_organism', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('domain', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('kingdom', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('phylum', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('organism_class', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('order', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('family', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('genus', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('species', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('ncbi_classification', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'common', ['Organism'])

        # Adding model 'DNASource'
        db.create_table(u'common_dnasource', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'common', ['DNASource'])

        # Adding model 'Sequencer'
        db.create_table(u'common_sequencer', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, primary_key=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'common', ['Sequencer'])

        # Adding model 'URLVerification'
        db.create_table(u'common_urlverification', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('checked_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('checked_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('status_ok', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('status_note', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'common', ['URLVerification'])


    def backwards(self, orm):
        # Deleting model 'BPAProject'
        db.delete_table(u'common_bpaproject')

        # Deleting model 'BPAUniqueID'
        db.delete_table(u'common_bpauniqueid')

        # Deleting model 'Facility'
        db.delete_table(u'common_facility')

        # Deleting model 'Organism'
        db.delete_table(u'common_organism')

        # Deleting model 'DNASource'
        db.delete_table(u'common_dnasource')

        # Deleting model 'Sequencer'
        db.delete_table(u'common_sequencer')

        # Deleting model 'URLVerification'
        db.delete_table(u'common_urlverification')


    models = {
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
        }
    }

    complete_apps = ['common']
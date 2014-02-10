# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Institution'
        db.create_table(u'activities_institution', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'activities', ['Institution'])

        # Adding model 'Author'
        db.create_table(u'activities_author', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=255)),
            ('affiliation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['activities.Institution'])),
        ))
        db.send_create_signal(u'activities', ['Author'])

        # Adding model 'MetadataOption'
        db.create_table(u'activities_metadataoption', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('group', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('position', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
        ))
        db.send_create_signal(u'activities', ['MetadataOption'])

        # Adding unique constraint on 'MetadataOption', fields ['group', 'code']
        db.create_unique(u'activities_metadataoption', ['group', 'code'])

        # Adding model 'Attachment'
        db.create_table(u'activities_attachment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
            ('main_visual', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('show', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('position', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('hostmodel', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['activities.Activity'])),
        ))
        db.send_create_signal(u'activities', ['Attachment'])

        # Adding model 'Collection'
        db.create_table(u'activities_collection', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'activities', ['Collection'])

        # Adding M2M table for field activities on 'Collection'
        m2m_table_name = db.shorten_name(u'activities_collection_activities')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('collection', models.ForeignKey(orm[u'activities.collection'], null=False)),
            ('activity', models.ForeignKey(orm[u'activities.activity'], null=False))
        ))
        db.create_unique(m2m_table_name, ['collection_id', 'activity_id'])

        # Adding model 'Activity'
        db.create_table(u'activities_activity', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('featured', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('release_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('embargo_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('lang', self.gf('django.db.models.fields.CharField')(default='en', max_length=5)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('uuid', self.gf('astroedu.django_ext.models.UUIDField')(max_length=64, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['activities.Author'])),
            ('institution', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['activities.Institution'])),
            ('age', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('time', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['activities.MetadataOption'])),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['activities.MetadataOption'])),
            ('supervised', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['activities.MetadataOption'])),
            ('cost', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['activities.MetadataOption'])),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['activities.MetadataOption'])),
            ('learning', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['activities.MetadataOption'])),
            ('theme', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('teaser', self.gf('django.db.models.fields.TextField')(max_length=140)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('keywords', self.gf('django.db.models.fields.TextField')()),
            ('materials', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('goals', self.gf('django.db.models.fields.TextField')()),
            ('objectives', self.gf('django.db.models.fields.TextField')()),
            ('background', self.gf('django.db.models.fields.TextField')()),
            ('fulldesc', self.gf('django.db.models.fields.TextField')()),
            ('evaluation', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('curriculum', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('additional_information', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('conclusion', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'activities', ['Activity'])

        # Adding M2M table for field level on 'Activity'
        m2m_table_name = db.shorten_name(u'activities_activity_level')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('activity', models.ForeignKey(orm[u'activities.activity'], null=False)),
            ('metadataoption', models.ForeignKey(orm[u'activities.metadataoption'], null=False))
        ))
        db.create_unique(m2m_table_name, ['activity_id', 'metadataoption_id'])

        # Adding M2M table for field skills on 'Activity'
        m2m_table_name = db.shorten_name(u'activities_activity_skills')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('activity', models.ForeignKey(orm[u'activities.activity'], null=False)),
            ('metadataoption', models.ForeignKey(orm[u'activities.metadataoption'], null=False))
        ))
        db.create_unique(m2m_table_name, ['activity_id', 'metadataoption_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'MetadataOption', fields ['group', 'code']
        db.delete_unique(u'activities_metadataoption', ['group', 'code'])

        # Deleting model 'Institution'
        db.delete_table(u'activities_institution')

        # Deleting model 'Author'
        db.delete_table(u'activities_author')

        # Deleting model 'MetadataOption'
        db.delete_table(u'activities_metadataoption')

        # Deleting model 'Attachment'
        db.delete_table(u'activities_attachment')

        # Deleting model 'Collection'
        db.delete_table(u'activities_collection')

        # Removing M2M table for field activities on 'Collection'
        db.delete_table(db.shorten_name(u'activities_collection_activities'))

        # Deleting model 'Activity'
        db.delete_table(u'activities_activity')

        # Removing M2M table for field level on 'Activity'
        db.delete_table(db.shorten_name(u'activities_activity_level'))

        # Removing M2M table for field skills on 'Activity'
        db.delete_table(db.shorten_name(u'activities_activity_skills'))


    models = {
        u'activities.activity': {
            'Meta': {'ordering': "['title']", 'object_name': 'Activity'},
            'additional_information': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'age': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['activities.Author']"}),
            'background': ('django.db.models.fields.TextField', [], {}),
            'conclusion': ('django.db.models.fields.TextField', [], {}),
            'cost': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['activities.MetadataOption']"}),
            'curriculum': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'embargo_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'evaluation': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fulldesc': ('django.db.models.fields.TextField', [], {}),
            'goals': ('django.db.models.fields.TextField', [], {}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['activities.MetadataOption']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['activities.Institution']"}),
            'keywords': ('django.db.models.fields.TextField', [], {}),
            'lang': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '5'}),
            'learning': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['activities.MetadataOption']"}),
            'level': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'level+'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['activities.MetadataOption']"}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['activities.MetadataOption']"}),
            'materials': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'objectives': ('django.db.models.fields.TextField', [], {}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'release_date': ('django.db.models.fields.DateTimeField', [], {}),
            'skills': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'skills+'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['activities.MetadataOption']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'supervised': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['activities.MetadataOption']"}),
            'teaser': ('django.db.models.fields.TextField', [], {'max_length': '140'}),
            'theme': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'time': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['activities.MetadataOption']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'uuid': ('astroedu.django_ext.models.UUIDField', [], {'max_length': '64', 'blank': 'True'})
        },
        u'activities.attachment': {
            'Meta': {'ordering': "['position', 'id']", 'object_name': 'Attachment'},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'hostmodel': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['activities.Activity']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_visual': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'show': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'activities.author': {
            'Meta': {'ordering': "['name']", 'object_name': 'Author'},
            'affiliation': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['activities.Institution']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'activities.collection': {
            'Meta': {'object_name': 'Collection'},
            'activities': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['activities.Activity']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'activities.institution': {
            'Meta': {'ordering': "['name']", 'object_name': 'Institution'},
            'country': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'activities.metadataoption': {
            'Meta': {'ordering': "['group', 'position']", 'unique_together': "(('group', 'code'),)", 'object_name': 'MetadataOption'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'group': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['activities']
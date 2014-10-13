# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing index on 'Activity', fields ['code']
        db.delete_index(u'activities_activity', ['code'])


    def backwards(self, orm):
        # Adding index on 'Activity', fields ['code']
        db.create_index(u'activities_activity', ['code'])


    models = {
        u'activities.activity': {
            'Meta': {'ordering': "['-slug']", 'object_name': 'Activity'},
            'acknowledgement': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'additional_information': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'age': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'age+'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['activities.MetadataOption']"}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['activities.Author']"}),
            'background': ('django.db.models.fields.TextField', [], {}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '4'}),
            'conclusion': ('django.db.models.fields.TextField', [], {}),
            'cost': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['activities.MetadataOption']"}),
            'curriculum': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'doi': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
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
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'supervised': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['activities.MetadataOption']"}),
            'teaser': ('django.db.models.fields.TextField', [], {'max_length': '140'}),
            'theme': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'time': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['activities.MetadataOption']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'uuid': ('astroedu.django_ext.models.UUIDField', [], {'max_length': '64', 'blank': 'True'})
        },
        u'activities.attachment': {
            'Meta': {'ordering': "['-show', 'position', 'id']", 'object_name': 'Attachment'},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'hostmodel': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['activities.Activity']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_visual': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'show': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'activities.author': {
            'Meta': {'ordering': "['name']", 'object_name': 'Author'},
            'affiliation': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['activities.Institution']"}),
            'citable_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'activities.collection': {
            'Meta': {'object_name': 'Collection'},
            'activities': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['activities.Activity']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'embargo_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['filemanager.File']", 'null': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'release_date': ('django.db.models.fields.DateTimeField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'activities.institution': {
            'Meta': {'ordering': "['name']", 'object_name': 'Institution'},
            'country': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['filemanager.File']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'False'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'activities.metadataoption': {
            'Meta': {'ordering': "['group', 'position']", 'unique_together': "(('group', 'code'),)", 'object_name': 'MetadataOption'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'group': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'activities.repositoryentry': {
            'Meta': {'ordering': "['repo']", 'object_name': 'RepositoryEntry'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['activities.Activity']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'repo': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '255'})
        },
        u'filemanager.file': {
            'Meta': {'ordering': "['title']", 'object_name': 'File'},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'folder': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['filemanager.Folder']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'filemanager.folder': {
            'Meta': {'ordering': "['title']", 'object_name': 'Folder'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        }
    }

    complete_apps = ['activities']
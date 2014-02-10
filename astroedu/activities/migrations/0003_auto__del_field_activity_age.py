# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Activity.age'
        db.delete_column(u'activities_activity', 'age')

        # Adding M2M table for field age on 'Activity'
        m2m_table_name = db.shorten_name(u'activities_activity_age')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('activity', models.ForeignKey(orm[u'activities.activity'], null=False)),
            ('metadataoption', models.ForeignKey(orm[u'activities.metadataoption'], null=False))
        ))
        db.create_unique(m2m_table_name, ['activity_id', 'metadataoption_id'])


    def backwards(self, orm):
        # Adding field 'Activity.age'
        db.add_column(u'activities_activity', 'age',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=10, blank=True),
                      keep_default=False)

        # Removing M2M table for field age on 'Activity'
        db.delete_table(db.shorten_name(u'activities_activity_age'))


    models = {
        u'activities.activity': {
            'Meta': {'ordering': "['title']", 'object_name': 'Activity'},
            'additional_information': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'age': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'age+'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['activities.MetadataOption']"}),
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
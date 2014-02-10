# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Folder'
        db.create_table(u'filemanager_folder', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'filemanager', ['Folder'])

        # Adding field 'File.folder'
        db.add_column(u'filemanager_file', 'folder',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['filemanager.Folder'], null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Folder'
        db.delete_table(u'filemanager_folder')

        # Deleting field 'File.folder'
        db.delete_column(u'filemanager_file', 'folder_id')


    models = {
        u'filemanager.file': {
            'Meta': {'ordering': "['title']", 'object_name': 'File'},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'folder': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['filemanager.Folder']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'filemanager.folder': {
            'Meta': {'ordering': "['title']", 'object_name': 'Folder'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['filemanager']
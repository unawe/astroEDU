# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType

def _populate_creation_modification(cls):
    content_type = ContentType.objects.get_for_model(cls)  #, for_concrete_model=False
    for obj in cls.objects.all():
        creation_date = LogEntry.objects.filter(
            object_id=obj.id,
            content_type=content_type
        ).order_by('action_time')[0].action_time
        modification_date = LogEntry.objects.filter(
            object_id=obj.id,
            content_type=content_type
        ).order_by('-action_time')[0].action_time
        obj.creation_date = creation_date
        obj.modification_date = modification_date
        obj.save()

def populate_creation_modification(apps, schema_editor):
    Activity = apps.get_model('activities', 'Activity')
    _populate_creation_modification(Activity)
    Collection = apps.get_model('activities', 'Collection')
    _populate_creation_modification(Collection)


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('activities', '0002_auto_20150103_1848'),
    ]

    operations = [
        migrations.RunPython(populate_creation_modification),
    ]

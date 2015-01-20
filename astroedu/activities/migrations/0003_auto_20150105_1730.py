# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations, connection
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType

def _populate_creation_modification(klass):
    content_type = ContentType.objects.get_for_model(klass)  #, for_concrete_model=False
    update_sql = 'UPDATE ' + klass._meta.db_table + ' SET creation_date=%s, modification_date=%s WHERE id = %s'
    for obj in klass.objects.all():
        creation_date = LogEntry.objects.filter(
            object_id=obj.id,
            content_type=content_type
        ).order_by('action_time')[0].action_time
        modification_date = LogEntry.objects.filter(
            object_id=obj.id,
            content_type=content_type
        ).order_by('-action_time')[0].action_time

        with connection.cursor() as c:
            c.execute(update_sql, [creation_date, modification_date, obj.id])
        # obj.creation_date = creation_date
        # obj.modification_date = modification_date
        # obj.save()

def populate_creation_modification(apps, schema_editor):
    '''
    Populate creation modification datetime fields with data from the django admin logs.
    Need to use raw SQL, or else modification_date would be set to now :)
    '''
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

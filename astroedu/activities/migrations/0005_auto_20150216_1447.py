# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def populate_author_institution(apps, schema_editor):
    Activity = apps.get_model('activities', 'Activity')
    AuthorInstitution = apps.get_model('activities', 'AuthorInstitution')
    for activity in Activity.objects.order_by('id'):
        obj = AuthorInstitution(activity=activity, author=activity.author, institution=activity.institution)
        obj.save()


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0004_auto_20150216_1446'),
    ]

    operations = [
        migrations.RunPython(populate_author_institution),
    ]


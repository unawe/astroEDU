# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0005_auto_20150216_1447'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='author',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='institution',
        ),
        migrations.RemoveField(
            model_name='author',
            name='affiliation',
        ),
    ]

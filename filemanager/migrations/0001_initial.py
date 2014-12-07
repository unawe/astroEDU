# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import filemanager.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text=b'Leave blank to use filename', max_length=255, blank=True)),
                ('file', models.FileField(upload_to=filemanager.models.upload_to)),
            ],
            options={
                'ordering': ['title'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text=b'Please use only alphabetic characters, numbers, and "-", "_" and "/"', unique=True, max_length=255, validators=[django.core.validators.RegexValidator(regex=b'^[-a-zA-Z0-9_/]+$')])),
            ],
            options={
                'ordering': ['title'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='file',
            name='folder',
            field=models.ForeignKey(blank=True, to='filemanager.Folder', null=True),
            preserve_default=True,
        ),
    ]

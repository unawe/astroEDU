# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0003_auto_20150105_1730'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthorInstitution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('activity', models.ForeignKey(related_name='authors', to='activities.Activity')),
                ('author', models.ForeignKey(to='activities.Author')),
                ('institution', models.ForeignKey(to='activities.Institution')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='activity',
            name='keywords',
            field=models.TextField(help_text='List of keywords, separated by commas'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='metadataoption',
            name='group',
            field=models.CharField(max_length=50, choices=[(b'age', 'Age'), (b'level', 'Level'), (b'time', 'Time'), (b'group', 'Group'), (b'supervised', 'Supervised'), (b'cost', 'Cost'), (b'location', 'Location'), (b'skills', 'Core skills'), (b'learning', 'Type of learning activity')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='repositoryentry',
            name='repo',
            field=models.CharField(max_length=50),
            preserve_default=True,
        ),
    ]

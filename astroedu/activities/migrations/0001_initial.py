# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import astroedu.activities.models
import astroedu.django_ext.models


class Migration(migrations.Migration):

    dependencies = [
        ('filemanager', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('featured', models.BooleanField(default=False)),
                ('published', models.BooleanField(default=True)),
                ('release_date', models.DateTimeField()),
                ('embargo_date', models.DateTimeField(null=True, blank=True)),
                ('lang', models.CharField(default=b'en', max_length=5)),
                ('code', models.CharField(help_text='Slug identifies the Activity; .', unique=True, max_length=4)),
                ('slug', models.SlugField(help_text='The Slug must be unique, and closely match the title for better SEO; it is used as part of the URL.', unique=True, max_length=255)),
                ('uuid', astroedu.django_ext.models.UUIDField(editable=False)),
                ('title', models.CharField(help_text='Title is shown in browser window. Use a good informative title, since search engines normally display the title on their result pages.', max_length=255, db_index=True)),
                ('acknowledgement', models.CharField(max_length=255, blank=True)),
                ('doi', models.CharField(help_text='Digital Object Identifier, in the format XXXX/YYYY. See http://www.doi.org/', max_length=50, verbose_name=b'DOI', blank=True)),
                ('theme', models.CharField(help_text='Use top level AVM metadata', max_length=40)),
                ('teaser', models.TextField(help_text='Maximum 140 characters', max_length=140)),
                ('description', models.TextField(help_text='Maximum 2 sentences! Maybe what and how?', verbose_name=b'brief description')),
                ('keywords', models.TextField(help_text='List of keywords, one per line')),
                ('materials', models.TextField(help_text='Please indicate costs and/or suppliers if possible', blank=True)),
                ('goals', models.TextField()),
                ('objectives', models.TextField(verbose_name=b'Learning Objectives')),
                ('background', models.TextField(verbose_name=b'Background Information')),
                ('fulldesc', models.TextField(verbose_name='Full Activity Description')),
                ('evaluation', models.TextField(help_text='If the teacher/educator wants to evaluate the impact of the activity, how can she/he do it?', blank=True)),
                ('curriculum', models.TextField(help_text='Please indicate which country', verbose_name=b'Connection to school curriculum', blank=True)),
                ('additional_information', models.TextField(help_text='Notes, Tips, Resources, Follow-up, Questions, Safety Requirements, Variations', blank=True)),
                ('conclusion', models.TextField()),
            ],
            options={
                'ordering': ['-code'],
                'abstract': False,
                'verbose_name_plural': 'activities',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, blank=True)),
                ('file', models.FileField(upload_to=astroedu.activities.models.get_file_path_step, blank=True)),
                ('main_visual', models.BooleanField(default=False, help_text='The main visual is used as the cover image.')),
                ('show', models.BooleanField(default=False, help_text='Include in attachment list.', verbose_name='Show')),
                ('position', models.PositiveSmallIntegerField(default=0, help_text='Used to define the order of attachments in the attachment list.', verbose_name=b'Position')),
                ('hostmodel', models.ForeignKey(to='activities.Activity')),
            ],
            options={
                'ordering': ['-show', 'position', 'id'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('citable_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('featured', models.BooleanField(default=False)),
                ('published', models.BooleanField(default=True)),
                ('release_date', models.DateTimeField()),
                ('embargo_date', models.DateTimeField(null=True, blank=True)),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(help_text='Slug identifies the Collection; it is used as part of the URL. Use only lowercase characters.', unique=True)),
                ('description', models.TextField(verbose_name=b'brief description', blank=True)),
                ('activities', models.ManyToManyField(related_name='+', null=True, to='activities.Activity', blank=True)),
                ('image', models.ForeignKey(to='filemanager.File', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, db_index=False)),
                ('name', models.CharField(max_length=255)),
                ('url', models.URLField(max_length=255, blank=True)),
                ('country', models.CharField(max_length=255, blank=True)),
                ('logo', models.ForeignKey(blank=True, to='filemanager.File', null=True)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MetadataOption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group', models.CharField(max_length=50, choices=[(b'age', 'Age'), (b'time', 'Time'), (b'level', 'Level'), (b'group', 'Group'), (b'supervised', 'Supervised'), (b'cost', 'Cost'), (b'location', 'Location'), (b'skills', 'Core skills'), (b'learning', 'Type of learning activity')])),
                ('code', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=255)),
                ('position', models.PositiveSmallIntegerField(default=0)),
            ],
            options={
                'ordering': ['group', 'position'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RepositoryEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('repo', models.CharField(max_length=50, blank=True)),
                ('url', models.URLField(max_length=255)),
                ('activity', models.ForeignKey(to='activities.Activity')),
            ],
            options={
                'ordering': ['repo'],
                'verbose_name_plural': 'repository entries',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='metadataoption',
            unique_together=set([('group', 'code')]),
        ),
        migrations.AddField(
            model_name='author',
            name='affiliation',
            field=models.ForeignKey(to='activities.Institution'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activity',
            name='age',
            field=models.ManyToManyField(related_name='age+', null=True, to='activities.MetadataOption', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activity',
            name='author',
            field=models.ForeignKey(to='activities.Author'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activity',
            name='cost',
            field=models.ForeignKey(related_name='+', blank=True, to='activities.MetadataOption', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activity',
            name='group',
            field=models.ForeignKey(related_name='+', blank=True, to='activities.MetadataOption', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activity',
            name='institution',
            field=models.ForeignKey(to='activities.Institution'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activity',
            name='learning',
            field=models.ForeignKey(related_name='+', verbose_name='type of learning activity', to='activities.MetadataOption', help_text='Enquiry-based learning model'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activity',
            name='level',
            field=models.ManyToManyField(help_text='Specify at least one of "Age" and "Level". ', related_name='level+', null=True, to='activities.MetadataOption', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activity',
            name='location',
            field=models.ForeignKey(related_name='+', blank=True, to='activities.MetadataOption', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activity',
            name='skills',
            field=models.ManyToManyField(related_name='skills+', null=True, verbose_name='core skills', to='activities.MetadataOption', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activity',
            name='supervised',
            field=models.ForeignKey(related_name='+', blank=True, to='activities.MetadataOption', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activity',
            name='time',
            field=models.ForeignKey(related_name='+', to='activities.MetadataOption'),
            preserve_default=True,
        ),
    ]

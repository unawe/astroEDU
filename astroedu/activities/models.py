import os
import re

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.redirects.models import Redirect
from django.contrib.sites.models import Site
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
# from tinymce.models import HTMLField
# from markupfield.fields import MarkupField
# from markupmirror.fields import MarkupMirrorField

from astroedu.django_ext.models import ArchivalModel, TranslationModel, MediaAttachedModel, UUIDField
from astroedu.activities import utils, tasks
from filemanager.models import File as ManagedFile


def get_file_path(instance, filename):
    return os.path.join('activities/attach', instance.uuid, filename)

def get_file_path_step(instance, filename):
    return os.path.join('activities/attach', instance.hostmodel.uuid, filename)


# class Richtext(ArchivalModel, TranslationModel):
#     field1 = HTMLField(blank=False, help_text=_(u'tinymce HTMLField'))
#     field2 = MarkupField(default_markup_type='html')
#     field3 = MarkupMirrorField(default_markup_type='markdown')
#     field4 = models.TextField()

#     def get_absolute_url(self):
#         from django.core.urlresolvers import reverse
#         return reverse('activities:rich', args=[self.id])



ACTIVITY_SECTIONS = (
    ('description', u'Brief Description'),
    ('goals', u'Goals'),
    ('objectives', u'Learning Objectives'),
    ('evaluation', u'Evaluation'),
    ('materials', u'Materials'),
    ('background', u'Background Information'),
    ('fulldesc', u'Full Activity Description'),
    ('curriculum', u'Curriculum'),
    ('additional_information', u'Additional Information'),
    ('conclusion', u'Conclusion'),
)

ACTIVITY_METADATA = (
    ('age', u'Age', 
            {'display': 'age_range', }),
    ('level', u'Level', 
            {'multiple': True, }),
    ('time', u'Time',
            {'display': 'time', }),
    ('group', u'Group',
            {'display': 'group', }),
    ('supervised', u'Supervised',
            {'display': 'supervised', }),
    ('cost', u'Cost',
            {'display': 'cost', }),
    ('location', u'Location',
            {'display': 'location', }),
    ('skills', u'Core skills', 
            {'multiple': True, }),
    ('learning', u'Type of learning activity',
            {'display': 'learning', }),
)

METADATA_OPTION_CHOICES = [(x[0], x[1]) for x in ACTIVITY_METADATA]

class MetadataOption(models.Model):
    group = models.CharField(max_length=50, blank=False, choices=METADATA_OPTION_CHOICES)
    code = models.CharField(max_length=50, blank=False)
    title = models.CharField(max_length=255, blank=False)
    position = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['group', 'position']
        unique_together = (('group', 'code'),)

    def __unicode__(self):
        return self.title

class MetadataOptionsManager(models.Manager):
    def get_queryset(self):
        return super(MetadataOptionsManager, self).get_queryset().order_by('position')


class Institution(MediaAttachedModel):
    slug = models.SlugField(unique=True, db_index=False, )
    name = models.CharField(blank=False, max_length=255, )
    url = models.URLField(blank=True, max_length=255, )
    country = models.CharField(blank=True, max_length=255, )
    logo = models.ForeignKey(ManagedFile, blank=True, null=True,)

    class Meta:
        ordering = ['name']

    @property
    def main_visual(self):
        return self.logo.file if self.logo else None

    def save(self, *args, **kwargs):
        super(Institution, self).save(*args, **kwargs)
        tasks.make_thumbnail.delay(self)

    def __unicode__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(blank=False, max_length=255, )
    citable_name = models.CharField(blank=False, max_length=255, )
    email = models.EmailField(blank=False, max_length=255, )
    affiliation = models.ForeignKey(Institution)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class Activity(ArchivalModel, TranslationModel):

    code = models.CharField(unique=True, max_length=4, help_text=_(u'The 4 digit code that identifies the Activity, in the format "YY##": year, folowed by sequential number.'))
    slug = models.SlugField(unique=True, max_length=255, help_text=_(u'The Slug must be unique, and closely match the title for better SEO; it is used as part of the URL.'))
    uuid = UUIDField(editable=False)
    doi = models.CharField(blank=True, max_length=50, verbose_name='DOI', help_text=_(u'Digital Object Identifier, in the format XXXX/YYYY. See http://www.doi.org/'))

    title = models.CharField(max_length=255, db_index=True, help_text=_(u'Title is shown in browser window. Use a good informative title, since search engines normally display the title on their result pages.'))
    teaser = models.TextField(blank=False, max_length=140, help_text=_(u'Maximum 140 characters'))
    theme = models.CharField(blank=False, max_length=40, help_text=_(u'Use top level AVM metadata'))
    keywords = models.TextField(blank=False, help_text=_(u'List of keywords, separated by commas'))

    acknowledgement = models.CharField(blank=True, max_length=255)

    age = models.ManyToManyField(MetadataOption, limit_choices_to={'group': 'age'}, related_name='age+', blank=True, null=True, )
    level = models.ManyToManyField(MetadataOption, limit_choices_to={'group': 'level'}, related_name='level+', blank=True, null=True, help_text=_(u'Specify at least one of "Age" and "Level". '), )
    time = models.ForeignKey(MetadataOption, limit_choices_to={'group': 'time'}, related_name='+', blank=False, null=False, )
    group = models.ForeignKey(MetadataOption, limit_choices_to={'group': 'group'}, related_name='+', blank=True, null=True, )
    supervised = models.ForeignKey(MetadataOption, limit_choices_to={'group': 'supervised'}, related_name='+', blank=True, null=True, )
    cost = models.ForeignKey(MetadataOption, limit_choices_to={'group': 'cost'}, related_name='+', blank=True, null=True, )
    location = models.ForeignKey(MetadataOption, limit_choices_to={'group': 'location'}, related_name='+', blank=True, null=True, )
    skills = models.ManyToManyField(MetadataOption, limit_choices_to={'group': 'skills'}, related_name='skills+', blank=True, null=True, verbose_name=u'core skills', )
    learning = models.ForeignKey(MetadataOption, limit_choices_to={'group': 'learning'}, related_name='+', blank=False, null=False, verbose_name=u'type of learning activity', help_text=_(u'Enquiry-based learning model'), )

    description = models.TextField(blank=False, verbose_name='brief description', help_text=_(u'Maximum 2 sentences! Maybe what and how?'))
    goals = models.TextField(blank=False, )
    objectives = models.TextField(blank=False, verbose_name='Learning Objectives', )
    evaluation = models.TextField(blank=True, help_text=_(u'If the teacher/educator wants to evaluate the impact of the activity, how can she/he do it?'))
    materials = models.TextField(blank=True, help_text=_(u'Please indicate costs and/or suppliers if possible'))
    background = models.TextField(blank=False, verbose_name='Background Information', )
    fulldesc = models.TextField(blank=False, verbose_name=u'Full Activity Description')
    curriculum = models.TextField(blank=True, verbose_name='Connection to school curriculum', help_text=_(u'Please indicate which country'))
    additional_information = models.TextField(blank=True, help_text=_(u'Notes, Tips, Resources, Follow-up, Questions, Safety Requirements, Variations'))
    conclusion = models.TextField(blank=False, )

    def age_range(self):
        # return ' '.join(obj.title for obj in self.age.all())
        age_ranges = [obj.title for obj in self.age.all()]
        return utils.beautify_age_range(age_ranges)

    def author_list(self):
        result = []
        for item in self.authors.all():
            result.append(item.display_name())
        return '; '.join(result)

    def citable_author_list(self):
        result = []
        for item in self.authors.all():
            result.append(item.author.citable_name)
        return '; '.join(result)

    @property
    def main_visual(self):
        result = None
        images = self.attachment_set.filter(main_visual=True)
        if images:
            result = images[0].file
        return result

    def attachment_list(self):
        return self.attachment_set.filter(show=True)

    # def generate_thumbnails(self, blocking=False):
    #     if blocking:
    #         tasks.make_thumbnail(self)
    #     else:
    #         tasks.make_thumbnail.delay(self)

    def download_key(self):
        return self.slug + '-astroEDU-' + self.code

    def zip_url(self):
        return self.download_url('zip')
    def pdf_url(self):
        return self.download_url('pdf')
    def epub_url(self):
        return self.download_url('epub')
    def rtf_url(self):
        return self.download_url('rtf')

    def download_url(self, resource):
        return os.path.join(settings.MEDIA_URL, self.media_key(), 'download', self.download_key() + '.' + resource)
    def download_path(self, resource):
        return os.path.join(settings.MEDIA_ROOT, self.media_key(), 'download', self.download_key() + '.' + resource)

    def __unicode__(self):
        return u'%s - %s' % (self.code, self.title)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('activities:detail', args=[self.slug])

    class Meta(ArchivalModel.Meta):
        ordering = ['-code']
        verbose_name_plural = 'activities'


@receiver(pre_save, sender=Activity)
def activity_pre_save(sender, instance, **kwargs):
    if instance.pk:
        old = Activity.objects.get(pk=instance.pk)
        redirect_activity(old, instance)

@receiver(post_save, sender=LogEntry)
def activity_post_save_delayed(sender, **kwargs):
    # The normal post_save signal is fired before the dependant objects are saved;
    # so instead we are listening to LogEntry post_save
    # In this case, we need the attachments to be up-to-date
    logentry = kwargs['instance']
    ct = ContentType.objects.get_for_model(Activity)
    if ct.id == logentry.content_type.id:
        instance = logentry.get_edited_object()
        tasks.make_thumbnail.delay(instance)
        tasks.zip_attachments.delay(instance)
        tasks.make_epub.delay(instance)
        tasks.make_pdf.delay(instance)
        tasks.make_rtf.delay(instance)

def redirect_activity(old, new):
    if old.slug != new.slug:
        current_site = Site.objects.get_current()

        # new redirect
        r = Redirect()
        r.site = current_site
        r.old_path = old.get_absolute_url()
        r.new_path = new.get_absolute_url()
        r.save()

        #update any old redirects
        for r in Redirect.objects.filter(new_path=old.get_absolute_url()):
            r.new_path = new.get_absolute_url()


class AuthorInstitution(models.Model):
    activity = models.ForeignKey(Activity, related_name='authors', )
    author = models.ForeignKey(Author)
    institution = models.ForeignKey(Institution)

    def display_name(self):
        return self.author.name + ', ' + self.institution.name

    def __unicode__(self):
        return unicode(self.display_name())


class Attachment(models.Model):
    title = models.CharField(max_length=255, blank=True)
    file = models.FileField(blank=True, upload_to=get_file_path_step, )
    main_visual = models.BooleanField(default=False, help_text=_(u'The main visual is used as the cover image.'))
    show = models.BooleanField(default=False, verbose_name=u'Show', help_text=_(u'Include in attachment list.'))
    position = models.PositiveSmallIntegerField(default=0, verbose_name='Position', help_text=_(u'Used to define the order of attachments in the attachment list.'))
    hostmodel = models.ForeignKey(Activity)

    def display_name(self):
        if self.title:
            return self.title
        else:
            return os.path.basename(self.file.name)

    def __unicode__(self):
        return unicode(self.display_name())

    class Meta:
        ordering = ['-show', 'position', 'id']


class Collection(ArchivalModel):
    title = models.CharField(blank=False, max_length=255)
    slug = models.SlugField(unique=True, db_index=True, help_text=_(u'Slug identifies the Collection; it is used as part of the URL. Use only lowercase characters.'))
    description = models.TextField(blank=True, verbose_name='brief description', )
    activities = models.ManyToManyField(Activity, related_name='+', blank=True, null=True, )
    image = models.ForeignKey(ManagedFile, null=True)

    @property
    def code(self):
        return self.slug

    @property
    def main_visual(self):
        return self.image.file if self.image else None

    def save(self, *args, **kwargs):
        super(Collection, self).save(*args, **kwargs)
        tasks.make_thumbnail.delay(self)

    def __unicode__(self):
        return unicode(self.title)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('collections:detail', args=[self.slug])

    class Meta(ArchivalModel.Meta):
        pass


class RepositoryEntry(models.Model):
    repo = models.CharField(max_length=50, blank=False)
    url = models.URLField(blank=False, max_length=255, )
    activity = models.ForeignKey(Activity)

    def repo_title(self):
        result = settings.REPOSITORIES[self.repo][0]
        return result

    def clean(self, *args, **kwargs):
        self.repo = None
        for name, value in settings.REPOSITORIES.items():
            url_pattern = value[1]
            if re.match(url_pattern, self.url):
                self.repo = name
        if not self.repo:
            raise ValidationError('Unknown repository URL. Known repositories are: ' + ', '.join(settings.REPOSITORIES.keys()))
        # super(RepositoryEntry, self).clean(*args, **kwargs)

    def __unicode__(self):
        return unicode(self.url)

    class Meta:
        ordering = ['repo']
        verbose_name_plural = 'repository entries'


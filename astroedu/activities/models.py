import os

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext as _
from django.db.models.signals import post_save
from django.dispatch import receiver
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


METADATA_OPTION_CHOICES = (
    ('age', u'Age'),
    ('time', u'Time'),
    ('level', u'Level'),
    ('group', u'Group'),
    ('supervised', u'Supervised'),
    ('cost', u'Cost'),
    ('location', u'Location'),
    ('skills', u'Core skills'),
    ('learning', u'Type of learning activity'),
)

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

    slug = models.SlugField(unique=True, db_index=True, help_text=_(u'Slug identifies the Activity; it is used as part of the URL. Use the following format: astroeduYY## (YY=year, ##=number).'))
    uuid = UUIDField(editable=False)

    title = models.CharField(max_length=255, db_index=True, help_text=_(u'Title is shown in browser window. Use a good informative title, since search engines normally display the title on their result pages.'))
    ''' Title of of the activity '''

    author = models.ForeignKey(Author)
    institution = models.ForeignKey(Institution)
    doi = models.CharField(blank=True, max_length=50, verbose_name='DOI', help_text=_(u'Digital Object Identifier, in the format XXXX/YYYY. See http://www.doi.org/'))
    ''' Digital Object Identifier '''

    # age = models.CharField(blank=True, max_length=10, help_text=_(u'Use the format min_age > max_age, or min_age+'))
    age = models.ManyToManyField(MetadataOption, limit_choices_to={'group': 'age'}, related_name='age+', blank=True, null=True, )
    # level = models.CharField(blank=True, max_length=10, choices=LEVEL_CHOICES, help_text=_(u'Specify at least one of "Age" and "Level"'))
    level = models.ManyToManyField(MetadataOption, limit_choices_to={'group': 'level'}, related_name='level+', blank=True, null=True, help_text=_(u'Specify at least one of "Age" and "Level". '))
    # time = models.CharField(blank=False, max_length=10, choices=TIME_CHOICES)
    time = models.ForeignKey(MetadataOption, limit_choices_to={'group': 'time'}, related_name='+', blank=False, null=False)
    # group = models.CharField(blank=True, max_length=10, choices=GROUP_CHOICES)
    group = models.ForeignKey(MetadataOption, limit_choices_to={'group': 'group'}, related_name='+', blank=True, null=True, )
    # supervised = models.CharField(blank=True, max_length=12, choices=SUPERVISED_CHOICES)
    supervised = models.ForeignKey(MetadataOption, limit_choices_to={'group': 'supervised'}, related_name='+', blank=True, null=True, )
    # cost = models.CharField(blank=True, max_length=10, choices=COST_CHOICES)
    cost = models.ForeignKey(MetadataOption, limit_choices_to={'group': 'cost'}, related_name='+', blank=True, null=True)
    # location = models.CharField(blank=True, max_length=10, choices=LOCATION_CHOICES)
    location = models.ForeignKey(MetadataOption, limit_choices_to={'group': 'location'}, related_name='+', blank=True, null=True)
    # skills = models.CharField(blank=True, max_length=30, verbose_name=u'core skills', choices=SKILLS_CHOICES)
    skills = models.ManyToManyField(MetadataOption, limit_choices_to={'group': 'skills'}, related_name='skills+', blank=True, null=True, verbose_name=u'core skills')
    # learning = models.CharField(blank=False, max_length=30, verbose_name=u'type of learning activity', help_text=_(u'Enquiry-based learning model'), choices=LEARNING_CHOICES)
    learning = models.ForeignKey(MetadataOption, limit_choices_to={'group': 'learning'}, related_name='+', blank=False, null=False, verbose_name=u'type of learning activity', help_text=_(u'Enquiry-based learning model'))

    theme = models.CharField(blank=False, max_length=40, help_text=_(u'Use top level AVM metadata'))

    teaser = models.TextField(blank=False, max_length=140, help_text=_(u'Maximum 140 characters'))
    ''' '''

    description = models.TextField(blank=False, verbose_name='brief description', help_text=_(u'Maximum 2 sentences! Maybe what and how?'))
    ''' '''

    keywords = models.TextField(blank=False, help_text=_(u'List of keywords, one per line'))
    ''' '''

    materials = models.TextField(blank=True, help_text=_(u'Please indicate costs and/or suppliers if possible'))
    '''  '''

    goals = models.TextField(blank=False, )
    ''' '''

    objectives = models.TextField(blank=False, verbose_name='Learning Objectives', )
    ''' '''

    background = models.TextField(blank=False, verbose_name='Background Information', )
    ''' '''

    fulldesc = models.TextField(blank=False, verbose_name=u'Full Activity Description')
    ''' '''

    evaluation = models.TextField(blank=True, help_text=_(u'If the teacher/educator wants to evaluate the impact of the activity, how can she/he do it?'))

    curriculum = models.TextField(blank=True, verbose_name='Connection to school curriculum', help_text=_(u'Please indicate which country'))

    additional_information = models.TextField(blank=True, help_text=_(u'Notes, Tips, Resources, Follow-up, Questions, Safety Requirements, Variations'))
    ''' '''

    conclusion = models.TextField(blank=False, )
    ''' '''

    def age_display(self):
        # return ' '.join(obj.title for obj in self.age.all())
        age_ranges = [obj.title for obj in self.age.all()]
        return utils.beautify_age_range(age_ranges)

    def main_visual(self):
        images = self.attachment_set.filter(main_visual=True)
        if images:
            return images[0].file
        else:
            return None

    def attachment_list(self):
        return self.attachment_set.filter(show=True)

    # def generate_thumbnails(self, blocking=False):
    #     if blocking:
    #         tasks.make_thumbnail(self)
    #     else:
    #         tasks.make_thumbnail.delay(self)

    def generate_downloads(self, blocking=False):
        if blocking:
            tasks.zip_attachments(self)
            # tasks.make_epub(self)
            tasks.make_pdf(self)
        else:
            tasks.zip_attachments.delay(self)
            tasks.make_epub.delay(self)
            tasks.make_pdf.delay(self)

    # def save(self, *args, **kwargs):
    #     super(Activity, self).save(*args, **kwargs)
    #     tasks.make_thumbnail.delay(self)
    #     self.generate_downloads()

    def __unicode__(self):
        return u'%s - %s' % (self.slug, self.title)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('activities:detail', args=[self.slug])

    class Meta(ArchivalModel.Meta):
        ordering = ['-slug']
        verbose_name_plural = 'activities'


@receiver(post_save, sender=Activity)
def activity_post_save(sender, instance, **kwargs):
    tasks.make_thumbnail.delay(instance)
    instance.generate_downloads()


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
    slug = models.SlugField(unique=True, db_index=True, help_text=_(u'Slug identifies the Collection; it is used as part of the URL. Use only lowercase characters.'))
    title = models.CharField(blank=False, max_length=255)
    description = models.TextField(blank=True, verbose_name='brief description', )
    activities = models.ManyToManyField(Activity, related_name='+', blank=True, null=True, )
    image = models.ForeignKey(ManagedFile, null=True)

    def main_visual(self):
        return self.image.file if self.image else None

    def save(self, *args, **kwargs):
        super(Collection, self).save(*args, **kwargs)
        tasks.make_thumbnail.delay(self)

    def __unicode__(self):
        return unicode(self.title)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('activities:collections_detail', args=[self.slug])

    class Meta(ArchivalModel.Meta):
        pass


class RepositoryEntry(models.Model):
    repo = models.CharField(max_length=50, blank=True)
    url = models.URLField(blank=False, max_length=255, )
    activity = models.ForeignKey(Activity)

    def repo_title(self):
        resul = None
        if self.repo:
            result = settings.REPOSITORIES[self.repo][0]
        return result

    def save(self, *args, **kwargs):
        self.repo = self.get_repository_name()
        super(RepositoryEntry, self).save(*args, **kwargs)

    def get_repository_name(self):
        result = None
        for name, value in settings.REPOSITORIES.items():
            if self.url.startswith(value[1]):
                result = name
        return result

    def __unicode__(self):
        return unicode(self.url)

    class Meta:
        ordering = ['repo']
        verbose_name_plural = 'repository entries'


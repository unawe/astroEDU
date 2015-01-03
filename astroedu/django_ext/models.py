import os
import uuid

from django.db import models
from django.db.models import query, Q
from django.utils.timezone import now
from django.core.urlresolvers import reverse
from django.conf import settings

# deprecation warning: django 1.8 supports UUIDField fields natively!
class UUIDField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 64)
        kwargs['blank'] = True
        #kwargs['default'] = str(uuid.uuid4())
        models.CharField.__init__(self, *args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(UUIDField, self).deconstruct()
        del kwargs['blank']
        if kwargs['max_length'] == 64:
            del kwargs['max_length']
        return name, path, args, kwargs

    def pre_save(self, model_instance, add):
        if add:
            value = str(uuid.uuid4())
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super(models.CharField, self).pre_save(model_instance, add)

# from south.modelsinspector import add_introspection_rules
# add_introspection_rules([], ["^astroedu\.django_ext\.models\.UUIDField"])


models.Model._admin_url_name = lambda self, type: 'admin:%s_%s_%s' % (
    self._meta.app_label, self._meta.model_name, type)


def get_admin_change_url(self):
    return reverse(self._admin_url_name('change'), args=(self.pk, ))
models.Model.get_admin_change_url = get_admin_change_url


def get_admin_delete_url(self):
    return reverse(self._admin_url_name('delete'), args=(self.pk, ))
models.Model.get_admin_delete_url = get_admin_delete_url


def get_admin_history_url(self):
    return reverse(self._admin_url_name('history'), args=(self.pk, ))
models.Model.get_admin_history_url = get_admin_history_url


def get_admin_changelist_url(self):
    return reverse(self._admin_url_name('changelist'))
models.Model.get_admin_changelist_url = get_admin_changelist_url


def get_admin_add_url(self):
    return reverse(self._admin_url_name('add'))
models.Model.get_admin_add_url = get_admin_add_url

models.Model.get_verbose_name = lambda self: self._meta.verbose_name
models.Model.get_verbose_name_plural = lambda self: self._meta.verbose_name_plural


class ArchivalQuerySet(query.QuerySet):
    def featured(self):
        return self.filter(featured=True).order_by('-release_date')


class ArchivalManager(models.Manager):
    def get_queryset(self):
        return ArchivalQuerySet(self.model)

    def all_super(self):
        return super(ArchivalManager, self).all()

    # def filter(self, *args, **kwargs):
    #     self.all().filter(*args, **kwargs)

    def all(self, user=None):
        '''filter for "visible" items if there is no logged in user'''
        if user and user.is_authenticated():
            return super(ArchivalManager, self).all()
        else:
            q = Q(published=True)
            # q = q & Q(release_date__gte=date) 
            q = q & Q(release_date__lte=now)
            q = q & (Q(embargo_date__isnull=True) | Q(embargo_date__lte=now))
            return self.get_queryset().filter(q)

    ## 'import' attributes from ArchivalQuerySet
    # def __getattr__(self, name):  
    #     return getattr(self.get_queryset(), name)
    def featured(self, *args, **kwargs):
        # return self.get_queryset().featured(*args, **kwargs)
        return self.all().featured(*args, **kwargs)


class MediaAttachedModel(models.Model):
    def media_key(self):
        return unicode(self._meta.verbose_name_plural)

    def thumb(self):
        return self.media_url('thumb')

    def media_url(self, resource):
        if self.main_visual:
            return os.path.join(settings.MEDIA_URL, self.media_key(), resource, self.code + '.jpg')

    class Meta:
        abstract = True


class ArchivalModel(MediaAttachedModel):
    featured = models.BooleanField(default=False)
    published = models.BooleanField(default=True)
    release_date = models.DateTimeField(blank=False)
    embargo_date = models.DateTimeField(blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True, null=True)
    modification_date = models.DateTimeField(auto_now=True, null=True)

    objects = ArchivalManager()

    def is_visible(self):
        return self.published and self.release_date < now() and (self.embargo_date is None or self.embargo_date < now())
    is_visible.short_description = u'visible?'
    is_visible.boolean = True

    @classmethod 
    def sitemap(cls, priority=None):
        from django.contrib.sitemaps import GenericSitemap
        object_list = {
            'queryset': cls.objects.all(),
            'date_field': 'modification_date',
        } 
        return GenericSitemap(object_list, priority=priority)

    class Meta:
        abstract = True


class TranslationModel(models.Model):
    lang = models.CharField(blank=False, max_length=5, default='en')

    class Meta:
        abstract = True

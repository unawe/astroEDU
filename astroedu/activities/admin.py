import re

from django.contrib import admin
from django import forms
from django.db import models
from django.utils.translation import ugettext as _

from contrib.remainingcharacters.admin import CounterAdmin

from astroedu.activities.models import Activity, Attachment, Author, Institution, MetadataOption, Collection, RepositoryEntry
# from astroedu.activities.models import Richtext
from filemanager.models import File as ManagedFile


# class RichtextAdminForm(forms.ModelForm):
#     from pagedown.widgets import AdminPagedownWidget
#     field4 = forms.CharField(widget=AdminPagedownWidget())        

#     class Meta:
#         model = Richtext


# class RichtextAdmin(admin.ModelAdmin):
#     # from django.db import models
    
#     # import django_markdown.widgets
#     # formfield_overrides = {
#     #     models.TextField: {'widget': django_markdown.widgets.MarkdownWidget()},
#     # }

#     # from pagedown.widgets import AdminPagedownWidget
#     # formfield_overrides = {
#     #     models.TextField: {'widget': AdminPagedownWidget },
#     # }
#     form = RichtextAdminForm


class MetadataOptionAdmin(admin.ModelAdmin):
    model = MetadataOption
    list_display = ('code', 'title', 'group', 'position', )
    list_editable = ('position', ) 
    list_filter = ('group',)

    def has_add_permission(self, request):
        return False


class ActivityAttachmentInline(admin.TabularInline):
    model = Attachment
    fields = ('title', 'file', 'main_visual', 'show', 'position', )


class RepositoryEntryInline(admin.TabularInline):
    model = RepositoryEntry
    readonly_fields = ('repo',)
    # fields = ('url', )

class ActivityAdminForm(forms.ModelForm):
    
    class Meta:
        model = Activity
        widgets = {
            'time': forms.RadioSelect,
            'group': forms.RadioSelect,
            'supervised': forms.RadioSelect,
            'cost': forms.RadioSelect,
            'location': forms.RadioSelect,
            'learning': forms.RadioSelect,
            # 'log': forms.Textarea(attrs={'disabled': True}),
        }

    def clean(self):
        cleaned_data = super(ActivityAdminForm, self).clean()
        slug = cleaned_data.get('slug')
        age = cleaned_data.get('age')
        level = cleaned_data.get('level')
        if not re.match('^\w*\d{4}$', slug):
            raise forms.ValidationError(_(u'The slug should be in the format: astroeduYY##'))
        if not age and not level:
            raise forms.ValidationError(_(u'Please fill in at least one of these fields: "Age", "Level"'))
        return cleaned_data


class ActivityAdmin(CounterAdmin):
    def view_link(self, obj):
        return u"<a href='%s'>View</a>" % obj.get_absolute_url()
    view_link.short_description = ''
    view_link.allow_tags = True

    counted_fields = ('teaser', )
    
    form = ActivityAdminForm
    list_display = ('slug', 'title', 'author', 'institution', 'published', 'release_date', 'embargo_date', 'is_visible', 'featured', 'view_link')  # , 'list_link_thumbnail', view_link('activities'))
    list_editable = ('title', 'published', 'featured', )
    ordering = ('-release_date', )
    date_hierarchy = 'release_date'
    list_filter = ('age', 'level', 'time', 'group', 'supervised', 'cost', 'location', )

    inlines = [ActivityAttachmentInline, RepositoryEntryInline]
    
    fieldsets = [
        (None, {'fields': ('slug', 'title', 'author', 'institution', 'acknowledgement', 'doi', ('age', 'level', ), ('time', 'group', 'supervised', 'cost',), ('location', 'skills', 'learning',) )}),
        # ('Language', {'fields': ('lang',)}),
        ('Publishing', {'fields': ('published', 'featured', ('release_date', 'embargo_date'), ), }),
        # ('Publishing', {'fields': ('published', ('release_date', 'embargo_date'), ), }),
        ('Description', {'fields': ('theme', 'teaser', 'description', 'keywords', 'materials', 'goals', 'objectives', 'background', )}),
        (None, {'fields': ('fulldesc', )}),
        (None, {'fields': ('conclusion', 'additional_information', 'evaluation', 'curriculum', )}),

    ]
    readonly_fields = ('is_visible', )
    # richtext_fields = ('description', 'materials', 'objectives', 'background', 'fulldesc_intro', 'fulldesc_outro', 'additional_information', 'evaluation', 'curriculum', 'credit', )
    formfield_overrides = {
        models.ManyToManyField: {'widget': forms.CheckboxSelectMultiple},
        models.ManyToManyField: {'widget': forms.CheckboxSelectMultiple},
    }

    class Media:
        js = [
            # '/static/js/jquery-1.7.2.min',
            'http://ajax.googleapis.com/ajax/libs/jquery/1.7/jquery.min.js',
            '/static/js/admin.js',
            # '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            # '/static/grappelli/tinymce_setup/tinymce_setup.js',
        ]

    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == 'institution':
    #         # kwargs['queryset'] = Institution.objects.all()
    #         kwargs['initial'] = Author.objects.get(kwargs['author']).affiliation
    #         return db_field.formfield(**kwargs)
    #     return super(ActivityAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs) 


class CollectionAdminForm(forms.ModelForm):
    class Meta:
        model = Collection
    
    def __init__(self, *args, **kwargs):
        super(CollectionAdminForm, self).__init__(*args, **kwargs)
        # the line below replaces     limit_choices_to={'folder__title': self.media_key()}
        # in the model field definition. self isn't defined there, so this is the solution 
        self.fields['image'].queryset = ManagedFile.objects.filter(folder__title=Collection().media_key())
        
    def clean(self):
        cleaned_data = super(CollectionAdminForm, self).clean()
        slug = cleaned_data.get('slug')
        if not re.match('^[a-z]+$', slug):
            raise forms.ValidationError(_(u'The slug should contain olny lowercase characters'))
        return cleaned_data


class CollectionAdmin(admin.ModelAdmin):
    form = CollectionAdminForm

    def view_link(self, obj):
        return u"<a href='%s'>View</a>" % obj.get_absolute_url()
    view_link.short_description = ''
    view_link.allow_tags = True

    def thumb_embed(self, obj):
        if obj.image:
            return '<img src="%s" style="height:50px" />' % obj.thumb()
    thumb_embed.short_description = 'Thumbnail'
    thumb_embed.allow_tags = True

    list_display = ('slug', 'title', 'thumb_embed', 'view_link', )

    filter_horizontal = ['activities']


class InstitutionAdminForm(forms.ModelForm):
    class Meta:
        model = Institution
    
    def __init__(self, *args, **kwargs):
        super(InstitutionAdminForm, self).__init__(*args, **kwargs)
        # the line below replaces     limit_choices_to={'folder__title': self.media_key()}
        # in the model field definition. self isn't defined there, so this is the solution 
        self.fields['logo'].queryset = ManagedFile.objects.filter(folder__title=Institution().media_key())


class InstitutionAdmin(admin.ModelAdmin):
    form = InstitutionAdminForm

    def logo_embed(self, obj):
        if obj.logo:
            return '<img src="%s" style="height:50px" />' % obj.media_url('logo')
    logo_embed.short_description = 'Logo'
    logo_embed.allow_tags = True

    list_display = ('slug', 'name', 'url', 'country', 'logo_embed', )


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'citable_name', 'email', )
    list_editable = ('citable_name', 'email', ) 


# class RepositoryEntryAdminForm(forms.ModelForm):
#     class Meta:
#         model = RepositoryEntry

# class RepositoryEntryAdmin(admin.ModelAdmin):
#     form = RepositoryEntryAdminForm
#     list_display = ('url', 'repo', )


# admin.site.register(Richtext, RichtextAdmin)
# admin.site.register(RepositoryEntry)#, RepositoryEntryAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(Institution, InstitutionAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(MetadataOption, MetadataOptionAdmin)
admin.site.register(Activity, ActivityAdmin)


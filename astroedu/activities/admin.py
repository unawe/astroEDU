import re

from django_mistune import markdown

from django.contrib import admin
from django import forms
from django.db import models
from django.utils.translation import ugettext as _

from contrib.remainingcharacters.admin import CounterAdmin
from contrib.adminutils import download_csv

from astroedu.activities.models import Activity, Attachment, Author, Institution, AuthorInstitution, MetadataOption, Collection, RepositoryEntry
# from astroedu.activities.models import Richtext
from filemanager.models import File as ManagedFile
from astroedu.activities.utils import bleach_clean

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


class ActivityAttachmentInlineFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        # There can be only one "main visual"
        if any(self.errors):
            # Don't bother validating the formset unless each form is valid on its own
            return
        
        main_visual_count = 0
        for form in self.forms:
            if form.cleaned_data:
                main_visual = form.cleaned_data['main_visual']
                if main_visual:
                    main_visual_count += 1

        if main_visual_count > 1:
            raise forms.ValidationError('There can be only one "main visual".')


class AuthorInstitutionInline(admin.TabularInline):
    model = AuthorInstitution
    verbose_name = 'author'
    verbose_name_plural = 'authors'
    min_num = 1
    extra = 1


class ActivityAttachmentInline(admin.TabularInline):
    model = Attachment
    formset = ActivityAttachmentInlineFormset
    fields = ('title', 'file', 'main_visual', 'show', 'position', )


class RepositoryEntryInline(admin.TabularInline):
    model = RepositoryEntry
    readonly_fields = ('repo',)
    # fields = ('url', )


class ActivityAdminForm(forms.ModelForm):
    
    class Meta:
        # model = Activity
        widgets = {
            'time': forms.RadioSelect,
            'group': forms.RadioSelect,
            'supervised': forms.RadioSelect,
            'cost': forms.RadioSelect,
            'location': forms.RadioSelect,
            'learning': forms.RadioSelect,
            # 'log': forms.Textarea(attrs={'disabled': True}),
            'teaser': forms.TextInput(attrs={'class': 'vTextField'}),
        }

    def clean_code(self):
        code = self.cleaned_data['code']
        if not re.match('^\w*\d{4}$', code):
            raise forms.ValidationError(_(u'The code should be four digits, in the format: YY##'))
        return code

    def clean_teaser(self):
        teaser = self.cleaned_data['teaser']
        teaser = teaser.replace('\n', ' ').strip()
        return teaser

    def clean(self):
        cleaned_data = super(ActivityAdminForm, self).clean()

        age = cleaned_data.get('age')
        level = cleaned_data.get('level')
        if not age and not level:
            raise forms.ValidationError(_(u'Please fill in at least one of these fields: "Age", "Level"'))

        for fieldname in ('description', 'materials', 'goals', 'objectives', 'background', 'fulldesc', 'evaluation', 'curriculum', 'additional_information', 'conclusion', ):
            value = cleaned_data.get(fieldname)
            value = bleach_clean(value)  # sanitize html embed in markdown
            cleaned_data[fieldname] = value
            try:
                markdown(value)
            except:
                # TODO: test error logging!
                import sys
                e = sys.exc_info()[0]
                print e
                self.add_error(fieldname, _(u'Markdown error'))

        return cleaned_data


class ActivityAdmin(CounterAdmin):

    def view_on_site(self, obj):
        return obj.get_absolute_url()

    def view_link(self, obj):
        return u'<a href="%s">View</a>' % obj.get_absolute_url()
    view_link.short_description = ''
    view_link.allow_tags = True

    def thumb_embed(self, obj):
        if obj.main_visual:
            return u'<img src="%s" style="height:50px" />' % obj.thumb_url()
    thumb_embed.short_description = 'Thumbnail'
    thumb_embed.allow_tags = True

    counted_fields = ('teaser', )
    prepopulated_fields = {'slug': ('title',)}

    form = ActivityAdminForm
    list_display = ('code', 'title', 'author_list', 'published', 'release_date', 'is_visible', 'featured', 'doi', 'thumb_embed', 'view_link')  # , 'list_link_thumbnail', view_link('activities'))
    list_editable = ('title', 'published', 'featured', )
    ordering = ('-release_date', )
    date_hierarchy = 'release_date'
    list_filter = ('age', 'level', 'time', 'group', 'supervised', 'cost', 'location', )
    actions = (download_csv, )

    inlines = [AuthorInstitutionInline, ActivityAttachmentInline, RepositoryEntryInline, ]
    
    fieldsets = [
        (None, {'fields': ('code', 'title', 'slug', 'acknowledgement', 'doi', )}),
        ('Publishing', {'fields': ('published', 'featured', ('release_date', 'embargo_date'), ), }),
        (None, {'fields': (('age', 'level', ), ('time', 'group', 'supervised', 'cost',), ('location', 'skills', 'learning',), 'keywords', )}),
        # ('Language', {'fields': ('lang',)}),
        ('Description', {'fields': ('theme', 'teaser', 'description', 'goals', 'objectives', 'evaluation', 'materials', 'background', )}),
        (None, {'fields': ('fulldesc', )}),
        (None, {'fields': ('curriculum', 'additional_information', 'conclusion', )}),
    ]
    readonly_fields = ('is_visible', )
    # richtext_fields = ('description', 'materials', 'objectives', 'background', 'fulldesc_intro', 'fulldesc_outro', 'additional_information', 'evaluation', 'curriculum', 'credit', )
    formfield_overrides = {
        models.ManyToManyField: {'widget': forms.CheckboxSelectMultiple},
    }

    fieldsets_and_inlines_order = ('f', 'f', 'i', )  # order of fields: first fieldset, then first inline, then everything else as usual

    class Media:
        js = [
            # '/static/js/jquery-1.7.2.min',
            'http://ajax.googleapis.com/ajax/libs/jquery/1.7/jquery.min.js',
            '/static/js/admin.js',
            # '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            # '/static/grappelli/tinymce_setup/tinymce_setup.js',
        ]


class CollectionAdminForm(forms.ModelForm):
    # class Meta:
    #     model = Collection
    
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

    prepopulated_fields = {"slug": ("title",)}

    def view_link(self, obj):
        return u'<a href="%s">View</a>' % obj.get_absolute_url()
    view_link.short_description = ''
    view_link.allow_tags = True

    def thumb_embed(self, obj):
        if obj.image:
            return '<img src="%s" style="height:50px" />' % obj.thumb_url()
    thumb_embed.short_description = 'Thumbnail'
    thumb_embed.allow_tags = True

    list_display = ('title', 'slug', 'thumb_embed', 'view_link', )

    fieldsets = [
        (None, {'fields': ('title', 'slug', )}),
        ('Publishing', {'fields': ('published', 'featured', ('release_date', 'embargo_date'), ), }),
        ('Contents', {'fields': ('description', 'image', 'activities', )}),

    ]
    filter_horizontal = ['activities']


class InstitutionAdminForm(forms.ModelForm):
    # class Meta:
    #     model = Institution
    
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


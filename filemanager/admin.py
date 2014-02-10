from django.contrib import admin
from django import forms

from filemanager.models import File, Folder
from django.core import validators

class FolderAdminForm(forms.ModelForm):
    
    class Meta:
        model = Folder

    def clean(self):
        cleaned_data = super(FolderAdminForm, self).clean()
        # cleaned_data['title'] = cleaned_data['title'].lowercase
        return cleaned_data


class FolderAdmin(admin.ModelAdmin):
	form = FolderAdminForm


class FileAdmin(admin.ModelAdmin):
    list_display = ('title', 'folder', )
    ordering = ('folder', 'title', )


admin.site.register(File, FileAdmin)
admin.site.register(Folder, FolderAdmin)

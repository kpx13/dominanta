# -*- coding: utf-8 -*-
from django.contrib import admin
import models
from django.db import models as django_models
from django.forms import CheckboxSelectMultiple
from mptt.admin import MPTTModelAdmin

class FileInline(admin.TabularInline): 
    model = models.ArchiveFile
    extra = 3

class SpecialtyAdmin(MPTTModelAdmin):
    inlines = [FileInline, ]
    list_display = ( 'name', 'id' , 'show', 'order', 'slug')
    search_fields = ('name', )
    mptt_level_indent = 20

class FileTypeAdmin(admin.ModelAdmin):
    inlines = [FileInline, ]
    list_display = ( 'name', 'id' , 'show', 'order')
    search_fields = ('name', )
    mptt_level_indent = 20

admin.site.register(models.Specialty, SpecialtyAdmin)
admin.site.register(models.FileType, FileTypeAdmin)
admin.site.register(models.ArchiveFile)

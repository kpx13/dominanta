# -*- coding: utf-8 -*-
from django.contrib import admin
import models
from django.db import models as django_models
from django.forms import CheckboxSelectMultiple
from mptt.admin import MPTTModelAdmin

class CommentInline(admin.StackedInline): 
    model = models.Comment
    extra = 0

class CategoryAdmin(MPTTModelAdmin):
    list_display = (  'name', 'id' , 'show', 'order', 'slug')
    search_fields = ('name', )
    mptt_level_indent = 20

admin.site.register(models.Category, CategoryAdmin)

class ArticleAdmin(admin.ModelAdmin):
    inlines = [CommentInline, ]
    list_display = ('name', 'date', 'text')
    search_fields = ('name', 'text')
    formfield_overrides = {
        django_models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

class CommentsAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'text')


admin.site.register(models.Article, ArticleAdmin)
admin.site.register(models.Comment, CommentsAdmin)
admin.site.register(models.ArticleTag)

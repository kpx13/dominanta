# -*- coding: utf-8 -*-
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from ckeditor.fields import RichTextField
import pytils
from taggit.managers import TaggableManager
from taggit.models import Tag, TaggedItem
import datetime


class Specialty(MPTTModel):
    name = models.CharField(max_length=50, unique=True, verbose_name=u'название')
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', verbose_name=u'родитель')
    show = models.BooleanField(default=True, verbose_name=u'показывать на сайте')
    order = models.IntegerField(default=0, verbose_name=u'порядок')
    slug = models.SlugField(verbose_name=u'slug', blank=True, help_text=u'Заполнять не нужно')
    icon = models.FileField(upload_to= 'uploads/icons', blank=True, max_length=256, verbose_name=u'иконка', help_text=u'Размер 85x87')
    
    class MPTTMeta:
        order_insertion_by = ['name']
    
    def __unicode__(self):
        return '%s%s' % (' -- ' * self.level, self.name)
    
    class Meta:
        verbose_name = u'категория'
        verbose_name_plural = u'категории'
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=pytils.translit.slugify(self.name)
        super(Category, self).save(*args, **kwargs)
        
    @staticmethod
    def get_by_slug(slug):
        try:
            return Category.objects.get(slug=slug)
        except:
            return None
        
class FileType(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name=u'название')
    show = models.BooleanField(default=True, verbose_name=u'показывать на сайте')
    order = models.IntegerField(default=0, verbose_name=u'порядок')
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = u'тип файла'
        verbose_name_plural = u'типы файлов'
        ordering=['order']


class ArchiveFile(models.Model):
    category = models.ForeignKey(Specialty, verbose_name=u'категория')
    name = models.CharField(max_length=128, verbose_name=u'название')
    date = models.DateField(auto_now=True, verbose_name=u'дата')
    desc = models.CharField(max_length=512, blank=True, verbose_name=u'описание')
    filetype = models.ForeignKey(FileType, verbose_name=u'тип файла')
    file = models.FileField(upload_to= 'uploads/archive', blank=True, max_length=256, verbose_name=u'иконка', help_text=u'')
    slug = models.SlugField(verbose_name=u'slug', blank=True, help_text=u'Заполнять не нужно')
    
    class Meta:
        verbose_name = u'файл'
        verbose_name_plural = u'файлы'
        ordering = ['-date']
    
    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=pytils.translit.slugify(self.name)
        super(Article, self).save(*args, **kwargs)
        
    @staticmethod
    def get_by_slug(slug):
        try:
            return ArchiveFile.objects.get(slug=slug)
        except:
            return None
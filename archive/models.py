# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from mptt.models import MPTTModel, TreeForeignKey
from ckeditor.fields import RichTextField
import pytils
from taggit.managers import TaggableManager
from taggit.models import Tag, TaggedItem
import datetime
from pyPdf import PdfFileReader
import os.path
import subprocess


class Specialty(MPTTModel):
    name = models.CharField(max_length=50, unique=True, verbose_name=u'название')
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', verbose_name=u'родитель')
    show = models.BooleanField(default=True, verbose_name=u'показывать на сайте')
    order = models.IntegerField(default=0, verbose_name=u'порядок')
    slug = models.SlugField(max_length=128, verbose_name=u'slug', blank=True, help_text=u'Заполнять не нужно')
    icon = models.FileField(upload_to= 'uploads/icons', default='uploads/icons/default_icon.jpg', blank=True, max_length=256, verbose_name=u'иконка', help_text=u'Размер 85x87')
    
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
        super(Specialty, self).save(*args, **kwargs)
        
    @staticmethod
    def get_by_slug(slug):
        try:
            return Specialty.objects.get(slug=slug)
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


def get_page_content(file_name):
    out = open('temp.txt', 'w')
    exec_str = 'pdftotext ' + file_name + ' temp.txt'
    p = subprocess.Popen(exec_str, shell=True, stdout=out, stderr=open('/dev/null', 'w'))
    p.wait()
    out.close()
    
    result = open('temp.txt', 'r').read()
    return result

class ArchiveFile(models.Model):
    category = models.ForeignKey(Specialty, verbose_name=u'категория')
    name = models.CharField(max_length=128, verbose_name=u'название')
    date = models.DateField(auto_now=True, verbose_name=u'дата')
    text = models.CharField(max_length=512, blank=True, verbose_name=u'описание')
    filetype = models.ForeignKey(FileType, verbose_name=u'тип файла')
    file = models.FileField(upload_to= 'uploads/archive', blank=True, max_length=256, verbose_name=u'файл', help_text=u'')
    file_content = models.TextField(verbose_name='содержимое файла', blank=True, help_text=u'для pnf-файлов заполняется автоматически')
    slug = models.SlugField(max_length=128, verbose_name=u'slug', blank=True, help_text=u'Заполнять не нужно')
    
    class Meta:
        verbose_name = u'файл'
        verbose_name_plural = u'файлы'
        ordering = ['-date']
    
    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=pytils.translit.slugify(self.name)
        if self.file.name.endswith('.pdf'):
            file_name = settings.PROJECT_ROOT + '/media/' + self.file.name
            self.file_content = get_page_content(file_name)
            
        super(ArchiveFile, self).save(*args, **kwargs)
        
    @staticmethod
    def get_by_slug(slug):
        try:
            return ArchiveFile.objects.get(slug=slug)
        except:
            return None
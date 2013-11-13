# -*- coding: utf-8 -*-
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from ckeditor.fields import RichTextField
import pytils
from taggit.managers import TaggableManager
from taggit.models import Tag, TaggedItem
import datetime
from django.contrib.auth.models import User


class Category(MPTTModel):
    name = models.CharField(max_length=50, unique=True, verbose_name=u'название')
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', verbose_name=u'родитель')
    show = models.BooleanField(default=True, verbose_name=u'показывать на сайте')
    order = models.IntegerField(default=0, verbose_name=u'порядок')
    slug = models.SlugField(max_length=50, verbose_name=u'slug', blank=True, help_text=u'Заполнять не нужно')
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
        super(Category, self).save(*args, **kwargs)
        
    @staticmethod
    def get_by_slug(slug):
        try:
            return Category.objects.get(slug=slug)
        except:
            return None


class ArticleTag(Tag):
    count = models.IntegerField(default=0, blank=True, verbose_name = u'Сколько раз встречается')
    
    class Meta:
        proxy = True
        
    def save(self, *args, **kwargs):
        self.count = self.count + 1
        self.slug = self.name.lower().replace(' ', '-')
        super(ArticleTag, self).save(*args, **kwargs)
        
    def nbsp(self):
        return self.name.replace(' ', '&nbsp;')

    def slugify(self, tag, i=None):
        slug = tag.lower().replace(' ', '-')
        if i is not None:
            slug += '-%d' % i
        return pytils.translit.slugify(slug)

    def __unicode__(self):
        return self.slug
    
    class Meta:
        verbose_name = u'тег'
        verbose_name_plural = u'теги'
    
    

class ArticleTaggedItem(TaggedItem):
    class Meta:
        proxy = True

    @classmethod
    def tag_model(cls):
        return ArticleTag
    

class Article(models.Model):
    category = models.ManyToManyField(Category, verbose_name=u'категория')
    name = models.CharField(max_length=512, verbose_name=u'название')
    date = models.DateField(verbose_name=u'дата')
    desc = RichTextField(max_length=2048, verbose_name=u'вступительный контент')
    text = RichTextField(verbose_name=u'продолжение контента')
    tags = TaggableManager(blank=True, through=ArticleTaggedItem)
    slug = models.SlugField(max_length=300, verbose_name=u'slug', unique=True, blank=True, help_text=u'Заполнять не нужно')
   
    class Meta:
        verbose_name = u'статья'
        verbose_name_plural = u'статьи'
        ordering = ['date']
    
    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=pytils.translit.slugify(self.name)
        super(Article, self).save(*args, **kwargs)
        
    @staticmethod
    def get_by_slug(slug):
        try:
            return Article.objects.get(slug=slug)
        except:
            return None
    
    @staticmethod
    def get_recent(count=4):
        return list(Article.objects.all()[:count])
    
    @staticmethod
    def get_by_tag(tag):
        if not tag:
            return []
        else:
            return list(Article.objects.filter(tags__in=[tag]))

class Comment(models.Model):
    user = models.ForeignKey(User, blank=True, verbose_name=u'автор')
    article = models.ForeignKey(Article, verbose_name=u'статья', related_name='comment')
    name = models.CharField(max_length=128, verbose_name=u'имя')
    date = models.DateTimeField(auto_now=True, verbose_name=u'дата')
    text = models.TextField(verbose_name=u'контент')
    show = models.BooleanField(default=True, blank=True, verbose_name=u'показывать?')
    class Meta:
        verbose_name = u'комментарий'
        verbose_name_plural = u'комментарии'
        ordering = ['date']
    
    def __unicode__(self):
        return self.name

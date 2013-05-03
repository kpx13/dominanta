# -*- coding: utf-8 -*-
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from ckeditor.fields import RichTextField
import pytils
from taggit.managers import TaggableManager
from taggit.models import Tag, TaggedItem


class Category(MPTTModel):
    name = models.CharField(max_length=50, unique=True, verbose_name=u'название')
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', verbose_name=u'родитель')
    show = models.BooleanField(default=True, verbose_name=u'показывать на сайте')
    order = models.IntegerField(default=0, verbose_name=u'порядок')
    slug = models.SlugField(verbose_name=u'slug', blank=True, help_text=u'Заполнять не нужно')
    
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
    name = models.CharField(max_length=128, verbose_name=u'название')
    date = models.DateField(verbose_name=u'дата')
    text = RichTextField(verbose_name=u'контент')
    desc = RichTextField(max_length=512, verbose_name=u'вступительный контент')
    tags = TaggableManager(blank=True, through=ArticleTaggedItem)
    slug = models.SlugField(verbose_name=u'slug', unique=True, blank=True, help_text=u'Заполнять не нужно')
   
    class Meta:
        verbose_name = u'статья'
        verbose_name_plural = u'статьи'
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
            return Article.objects.get(slug=slug)
        except:
            return None
    
    @staticmethod
    def get_recent(count=4):
        return list(Article.objects.all()[:count])
    
    @staticmethod
    def get_by_tag(tag=None):
        if not tag:
            return []
        else:
            return list(Article.objects.filter(tags__slug__in=[tag]))
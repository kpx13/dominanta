# -*- coding: utf-8 -*-

import datetime
from django.core.context_processors import csrf
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from livesettings import config_value

from pages.models import Page
from blog.models import Article, Category, ArticleTag

def get_common_context(request):
    c = {}
    c['request_url'] = request.path
    c.update(csrf(request))
    c['tags'] = ArticleTag.objects.all()
    return c

def home_page(request):
    c = get_common_context(request)
    c['request_url'] = 'home'
    c['settings'] = { }
    
    return render_to_response('home.html', c, context_instance=RequestContext(request))

def other_page(request, page_name):
    c = get_common_context(request)
    try:
        c.update(Page.get_by_slug(page_name))
        return render_to_response('page.html', c, context_instance=RequestContext(request))
    except:
        raise Http404()

def articles_page(request, category=None):
    c = get_common_context(request)
    if category:
        c['category'] = Category.get_by_slug(category)
        categories = c['category'].get_descendants(include_self=True)
        c['sub_categories'] = c['category'].get_children()

        c['breadcrumb'] = []
        curr_cat = c['category']
        while curr_cat:
            c['breadcrumb'].append(curr_cat)
            curr_cat = curr_cat.parent
        c['breadcrumb'].reverse()
        c['breadcrumb'] = c['breadcrumb'][:-1]
        
        c['articles'] = Article.objects.filter(category__in=categories)
        return render_to_response('articles.html', c, context_instance=RequestContext(request))
    else:
        c['articles'] = Article.objects.all()
        return render_to_response('articles.html', c, context_instance=RequestContext(request))
    
def article_page(request, category, name):
    c = get_common_context(request)
    
    c['category'] = Category.get_by_slug(category)
    descendants = c['category'].get_descendants(include_self=True)
    
    c['article'] = Article.objects.get(slug=name, category__in=descendants)
    categoies = c['article'].category.all()
    curr_cat = None
    for cat in categoies:
        if cat in descendants:
            curr_cat = cat
    
    c['breadcrumb'] = []
    while curr_cat:
        print curr_cat
        c['breadcrumb'].append(curr_cat)
        curr_cat = curr_cat.parent
    c['breadcrumb'].reverse()
    return render_to_response('article.html', c, context_instance=RequestContext(request))

def tags_page(request, tag=None):
    c = get_common_context(request)
    c['articles'] = Article.get_by_tag(tag)
    c['tag'] = ArticleTag.objects.filter(slug__in=[tag])[0]
    c['category'] = Category.get_by_slug('mikst')
    return render_to_response('articles.html', c, context_instance=RequestContext(request))

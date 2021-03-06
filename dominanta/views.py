# -*- coding: utf-8 -*-

import datetime
from django.core.context_processors import csrf
from django.contrib.auth.forms import AuthenticationForm
from registration.forms import RegistrationForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from livesettings import config_value

from blog.forms import ArticleForm
from pages.models import Page
from blog.models import Article, Category, ArticleTag, Comment
from archive.models import Specialty, FileType, ArchiveFile

PAGINATION_COUNT = 15

def get_common_context(request):
    c = {}
    c['request_url'] = request.path
    c.update(csrf(request))
    c['tags'] = ArticleTag.objects.all()
    c['top_menu'] = Category.objects.filter(show=True).order_by('order')
    return c

def context():
    c = {}
    c['authentication_form'] = AuthenticationForm()
    c['registration_form'] = RegistrationForm()
    return c

def login_page(request):
    c = get_common_context(request)
    c['request_url'] = request.path
    return render_to_response('registry.html', c, context_instance=RequestContext(request))

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

def article_page(request, id):
    c = get_common_context(request)
    c['article'] = Article.objects.get(id=id)
    
    if request.method == 'POST':
        if request.POST['text']:
            Comment(article=c['article'],
                    user=request.user,
                    name=request.user.first_name + ' ' + request.user.last_name,
                    text=request.POST['text']).save()
        return HttpResponseRedirect(request.path)
    categories = c['article'].category.all().filter(show=True)

    c['articles'] = Article.objects.filter(category__in=categories)
    
    c['breadcrumb'] = []
    curr_cat = categories[0]
    while curr_cat:
        c['breadcrumb'].append(curr_cat)
        curr_cat = curr_cat.parent
    c['breadcrumb'].reverse()
    return render_to_response('article.html', c, context_instance=RequestContext(request))

def article_edit_page(request, id):
    if not request.user.is_superuser:
        return HttpResponseRedirect('/article/%s/' % id)
    c = get_common_context(request)
    c['article'] = Article.objects.get(id=id)
    
    if request.method == 'POST':
        if (request.POST['action'] == 'save') or (request.POST['action'] == 'save_back'):
            af = ArticleForm(request.POST, instance=c['article'])
            if af.is_valid(): 
                af.save()
                if request.POST['action'] == 'save_back':
                    return HttpResponseRedirect('/article/%s/' % id)
                else:
                    return HttpResponseRedirect('/article/%s/edit/' % id)
            else:
                pass
        return HttpResponseRedirect(request.path)
    categories = c['article'].category.all().filter(show=True)

    c['articles'] = Article.objects.filter(category__in=categories)
    
    c['article_form'] = ArticleForm(instance=c['article'])
    return render_to_response('article_edit.html', c, context_instance=RequestContext(request))

def article_del_page(request, id):
    if not request.user.is_superuser:
        return HttpResponseRedirect('/article/%s/' % id)
    c = get_common_context(request)
    Article.objects.get(id=id).delete()
    return HttpResponseRedirect('/')

def comment_del(request, id):
    if not request.user.is_superuser:
        return HttpResponseRedirect('/')
    c = Comment.objects.get(id=id)
    article_id = c.article.id 
    c.delete()
    return HttpResponseRedirect('/article/%s/' % article_id)

def comment_ban(request, id):
    if not request.user.is_superuser:
        return HttpResponseRedirect('/')
    c = Comment.objects.get(id=id)
    article_id = c.article.id
    u = c.user
    u.is_active = False
    u.save()
    c.delete()
    return HttpResponseRedirect('/article/%s/' % article_id)

def articles_page(request, id):
    c = get_common_context(request)

    c['category'] = Category.objects.get(id=id)
    categories = c['category'].get_descendants(include_self=True).filter(show=True)
    c['sub_categories'] = c['category'].get_children().filter(show=True)

    c['breadcrumb'] = []
    curr_cat = c['category']
    while curr_cat:
        c['breadcrumb'].append(curr_cat)
        curr_cat = curr_cat.parent
    c['breadcrumb'].reverse()
    c['breadcrumb'] = c['breadcrumb'][:-1]
    
    items = Article.objects.filter(category=c['category'])
    c['all_articles'] = items
    
    paginator = Paginator(items, PAGINATION_COUNT)
    page = int(request.GET.get('page', '1'))
    c['get_request'] = c['request_url'][:-1]
    try:
        c['articles'] = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        c['articles'] = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        c['articles'] = paginator.page(page)
    c['page'] = page
    c['page_range'] = paginator.page_range
    if len(c['page_range']) > 1:
        c['need_pagination'] = True
    return render_to_response('articles.html', c, context_instance=RequestContext(request))

def tags_page(request, id):
    c = get_common_context(request)
    c['tag'] = ArticleTag.objects.get(id=id)
    items = Article.get_by_tag(c['tag'])
    
    paginator = Paginator(items, 2)
    page = int(request.GET.get('page', '1'))
    c['get_request'] = c['request_url'][:-1]
    try:
        c['articles'] = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        c['articles'] = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        c['articles'] = paginator.page(page)
    c['page'] = page
    c['page_range'] = paginator.page_range
    if len(c['page_range']) > 1:
        c['need_pagination'] = True
        
    return render_to_response('articles.html', c, context_instance=RequestContext(request))

def search_page(request):
    c = get_common_context(request)
    if request.method == 'GET':
        return render_to_response('articles.html', c, context_instance=RequestContext(request))
    else:       
        from fullsearch import search_articles, search_archive
        query = request.POST.get('query', '').strip()
        if query:
            items_articles = search_articles(query)
            c['search_query'] = query
        else:
            items_articles = Article.objects.all()
            c['search_query'] = u'По всем категориям'
        in_archive = request.POST.get('in_archive', False)
        if in_archive:
            items_archive = search_archive(query)
            c['archive'] = items_archive
            c['archive_active'] = False
    
        
        """
        paginator = Paginator(items, PAGINATION_COUNT)
        page = int(request.POST.get('page', '1'))
        c['get_request'] = c['request_url'][:-1]
        try:
            c['articles'] = paginator.page(page)
        except PageNotAnInteger:
            page = 1
            c['articles'] = paginator.page(page)
        except EmptyPage:
            page = paginator.num_pages
            c['articles'] = paginator.page(page)
        c['page'] = page
        c['page_range'] = paginator.page_range
        if len(c['page_range']) > 1:
            c['need_pagination'] = True
        """
        c['articles'] = items_articles
        c['articles_active'] = False
        c['show_tab'] = False
        if len(items_articles) > 0:
            c['articles_active'] = True
        else:
            c['archive_active'] = True
        if in_archive:
            c['show_tab'] = True
        
        return render_to_response('articles_search.html', c, context_instance=RequestContext(request))

def archive_search_page(request):
    c = get_common_context(request)
    if request.method == 'GET':
        return render_to_response('articles.html', c, context_instance=RequestContext(request))
    else:       
        from fullsearch import search_archive
        
        query = request.POST.get('query', '').strip()
        categories = [int(x) for x in request.POST.getlist('category', '')]
        if query:
            items_archive = search_archive(query, categories)
            c['search_query'] = query
        else:
            items_archive = ArchiveFile.objects.filter(category__in=categories)
            c['search_query'] = 'по выбранным категориям'
         
        c['archive'] = items_archive
        c['archive_active'] = False
        
        c['articles_active'] = False
        c['show_tab'] = True
        
        return render_to_response('archive_search.html', c, context_instance=RequestContext(request))

def archive_page(request):
    c = get_common_context(request)
    c['filetypes'] = FileType.objects.filter(show=True).order_by('order')
    c['medspec'] = Specialty.objects.get(slug='medspetsialnosti').get_children().filter(show=True).order_by('order')
    c['dokl'] = Specialty.objects.get(slug='doklinika').get_children().filter(show=True).order_by('order')
    return render_to_response('archive_home.html', c, context_instance=RequestContext(request))

def archive_filetype_page(request, id):
    c = get_common_context(request)
    c['filetype'] = FileType.objects.get(id=id)
    c['files'] =  ArchiveFile.objects.filter(filetype=id)
    return render_to_response('archive_filetype.html', c, context_instance=RequestContext(request))
 
def archive_category_page(request, id):
    c = get_common_context(request)
    c['category'] = Specialty.objects.get(id=id)
    c['files'] =  ArchiveFile.objects.filter(category=id)
    return render_to_response('archive_category.html', c, context_instance=RequestContext(request))
 
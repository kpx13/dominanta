# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from filebrowser.sites import site
admin.autodiscover()

import settings
import views

urlpatterns = patterns('',
    
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    url(r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/static/favicon.ico'}),
    
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^admin/filebrowser/', include(site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/jsi18n/', 'django.views.i18n.javascript_catalog'),
    url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^settings/', include('livesettings.urls')),
    url(r'^ulogin/', include('django_ulogin.urls')),
    
    url(r'^logout/',  'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    url(r'^accounts/', include('registration.urls'), {'extra_context': views.context()}),

    url(r'^$' , views.home_page),
    url(r'^article/(?P<id>[\w-]*)/$' , views.article_page),
    url(r'^articles/category/(?P<id>[\w-]+)/$' , views.articles_page),
    url(r'^articles/tag/(?P<id>[\w-]+)/$' , views.tags_page),
    url(r'^search/$' , views.search_page),
    url(r'^archive/$' , views.archive_page),
    url(r'^archive/filetype/(?P<id>[\w-]+)/$' , views.archive_filetype_page),
    url(r'^archive/category/(?P<id>[\w-]+)/$' , views.archive_category_page),

    url(r'^(?P<page_name>[\w-]+)/$' , views.other_page),
    
)

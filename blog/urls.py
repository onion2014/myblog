#!/usr/bin/env python
# -*- coding:utf-8 -*-


from django.conf.urls import url
from . import views
from django.conf import settings
from django.views import static
from blog.uploads import upload_image

# 视图函数命名空间,通过 app_name='blog' 告诉 Django 这个 urls.py 模块是属于 blog 应用的
app_name = 'blog'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^full_blog$', views.full_blog, name='full_blog'),
    url(r'^about$', views.about, name='about'),
    url(r'^contact$', views.contact, name='contact'),
    # url(r'^single$', views.single, name='single'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.archives, name='archives'),
    url(r'^category/(?P<pk>[0-9]+)/$', views.category, name='category'),
    url(r'^search/$', views.search, name='search'),
    url(r'^tag/(?P<pk>[0-9]+)/$', views.TagView.as_view(), name='tag'),
    # url(r'^tag/(?P<pk>[0-9]+)/$', views.tag_tag, name='tag_tag'),
    url(r"^uploads/(?P<path>.*)$", static.serve, {"document_root": settings.MEDIA_ROOT},),
    url(r'^admin/upload/(?P<dir_name>[^/]+)$', upload_image, name='upload_image'),
]
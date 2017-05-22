#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.contrib import admin
from .models import Post, Category, Tag


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_time', 'modified_time', 'category', 'author']

# Register your models here.
# 把新增的 PostAdmin 也注册进来
admin.site.register(Post,PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)


#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.contrib import admin
from .models import Post, Category, Tag

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_time', 'modified_time', 'category', 'author']

    class Media:
        # 在管理后台的HTML文件中加入js文件, 每一个路径都会追加STATIC_URL/
        js = (
            '/static/js/kindeditor/kindeditor-all-min.js',
            '/static/js/kindeditor/lang/zh-CN.js',
            '/static/js/kindeditor/config.js',
        )


# Register your models here.
# 把新增的 PostAdmin 也注册进来
admin.site.register(Post,PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)


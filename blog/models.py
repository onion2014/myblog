#!/usr/bin/env python
# -*- coding:utf-8 -*-
import markdown

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.six import python_2_unicode_compatible   #兼容python2
from django.utils.html import strip_tags


# python_2_unicode_compatible 装饰器用于兼容 Python2


@python_2_unicode_compatible
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Post(models.Model):
    # 给数据库增加字段
    title = models.CharField(max_length=70)
    body = models.TextField()
    # 这两个列分别表示文章的创建时间和最后一次修改时间，存储时间的字段用 DateTimeField 类型。
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()

    # 文章摘要，可以没有文章摘要，但默认情况下 CharField 要求我们必须存入数据，否则就会报错。
    # 指定 CharField 的 blank=True 参数值后就可以允许空值了。
    excerpt = models.CharField(max_length=200,blank=True)

    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag, blank=True)
    author = models.ForeignKey(User)
    # 新增 views 字段记录阅读量
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    # 自定义 get_absolute_url 方法
    # 记得从 django.urls 中导入 reverse 函数
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    # 增加views的方法
    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])
    # 创建排序类
    class Meta:
        ordering = ['-created_time']

    def save(self, *args, **kwargs):
        # 如果没有填写摘要
        if not self.excerpt:
            # 首先实例化一个 Markdown 类，用于渲染 body 的文本
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            # 先将 Markdown 文本渲染成 HTML 文本
            # strip_tags 去掉 HTML 文本的全部 HTML 标签
            # 从文本摘取前 54 个字符赋给 excerpt
            self.excerpt = strip_tags(md.convert(self.body))[:54]

            # 调用父类的 save 方法将数据保存到数据库中
            super(Post, self).save(*args, **kwargs)
        super(Post, self).save(*args, **kwargs)

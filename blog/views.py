# -*- coding:utf-8 -*-
# from django.http import HttpResponse


import markdown

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.utils.text import slugify
from django.views.generic import ListView
from markdown.extensions.toc import TocExtension
from comments.forms import CommentForm
from .models import Post, Category, Tag


def index(request):
    # 直接返回响应
    # return HttpResponse("欢迎访问我的博客首页！")

    # 获取全部文章，按创建时间倒序排序
    post_list = Post.objects.all().order_by('-created_time')
    paginator = Paginator(post_list, 5)
    page = request.GET.get('page')

    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    # 调用render函数，根据传入的参数来构造HttpResponse
    return render(request, 'blog/index.html', context={'post_list': post_list})

# class IndexView(ListView):
#     model = Post
#     template_name = 'blog/index.html'
#     context_object_name = 'post_list'


def full_blog(request):
    post_list = Post.objects.all().order_by('-created_time')
    paginator = Paginator(post_list, 5)
    page = request.GET.get('page')

    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'blog/full-blog.html', context={'post_list': post_list})


def about(request):
    return render(request, 'blog/about.html')


def contact(request):
    return render(request, 'blog/contact.html')


# def single(request):
#     return render(request, 'blog/single.html')


def archives(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month,
                                    ).order_by('-created_time')
    # 调用render函数，根据传入的参数来构造HttpResponse
    paginator = Paginator(post_list, 5)
    page = request.GET.get('page')

    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'blog/index.html', context={'post_list': post_list})


def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    # model 中创建了meta类，进行排序，order_by('-created_time')可以删掉
    post_list = Post.objects.filter(category=cate)
    paginator = Paginator(post_list, 5)
    page = request.GET.get('page')

    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'blog/index.html', context={'post_list': post_list})


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # 阅读量 +1
    post.increase_views()
    # post.body = markdown.Markdown(post.body,
    #                               extensions=[
    #                                 'markdown.extensions.extra',
    #                                 'markdown.extensions.codehilite',
    #                                 'markdown.extensions.toc',
    #                             ])
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        TocExtension(slugify=slugify),
    ])
    post.body = md.convert(post.body)

    # 记得在顶部导入 CommentForm
    form = CommentForm()
    comment_list = post.comment_set.all()
    post_list = Post.objects.all().order_by('-created_time')
    paginator = Paginator(post_list, 5)
    page = request.GET.get('page')

    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)

    # 将文章、表单、以及文章下的评论列表作为模板变量传给 detail.html 模板，以便渲染相应数据。
    context = {'post': post,
               'toc': md.toc,
               'form': form,
               'comment_list': comment_list,
               'post_list': post_list,
               }
    return render(request, 'blog/detail.html', context=context)


def search(request):
    keyword = request.GET.get('searchWords')
    error_msg = ''

    if not keyword:
        error_msg = '请输入关键词'
        return render(request, 'blog/index.html', {'error_msg': error_msg})

    post_list = Post.objects.filter(title__icontains=keyword)
    paginator = Paginator(post_list, 5)
    page = request.GET.get('page')

    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)

    # 将搜索到的内容显示在index.html中
    return render(request, 'blog/index.html', {'error_msg': error_msg,
                                               'post_list': post_list})

# def tag_tag(request, pk):
#     tag_1 = get_object_or_404(Tag, pk=pk)
#     post_list = Post.objects.filter(tags=tag_1)
#     return render(request, 'blog/index.html', context={'post_list': post_list})

# class TagView(ListView):
#     model = Post
#     template_name = 'blog/index.html'
#     context_object_name = 'post_list'
#
#     def get_queryset(self):
#         tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
#         return super(TagView, self).get_queryset().filter(tags=tag)

class TagView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)
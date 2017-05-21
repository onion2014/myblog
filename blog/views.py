# -*- coding:utf-8 -*-
# from django.http import HttpResponse
import markdown

from django.shortcuts import render, get_object_or_404
from comments.forms import CommentForm
from .models import Post, Category
from django.db.models.aggregates import Count

def index(repuest):
    # 直接返回响应
    # return HttpResponse("欢迎访问我的博客首页！")

    post_list = Post.objects.all().order_by('-created_time')  # 获取全部文章，按创建时间倒序排序

    # 调用render函数，根据传入的参数来构造HttpResponse
    return render(repuest, 'blog/index.html', context={'post_list': post_list})

def archives(repuest, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month,
                                    ).order_by('-created_time')
    # 调用render函数，根据传入的参数来构造HttpResponse
    return render(repuest, 'blog/index.html', context={'post_list': post_list})

def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    # model 中创建了meta类，进行排序，order_by('-created_time')可以删掉
    post_list = Post.objects.filter(category=cate)
    # category_list = Category.objects.annotate(num_posts=Count('post'))
    return render(request, 'blog/index.html', context={'post_list': post_list})

def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                    'markdown.extensions.extra',
                                    'markdown.extensions.codehilite',
                                    'markdown.extensions.toc',
                                ])

    # 记得在顶部导入 CommentForm
    form = CommentForm()
    comment_list = post.comment_set.all()

    # 将文章、表单、以及文章下的评论列表作为模板变量传给 detail.html 模板，以便渲染相应数据。
    context = {'post': post,
               'form': form,
               'comment_list': comment_list
               }
    return render(request, 'blog/detail.html', context=context)

def search(request):
    q = request.GET.get('q')
    error_msg = ''

    if not q:
        error_msg = '请输入关键词'
        return render(request, 'blog/index.html', {'error_msg': error_msg})

    post_list = Post.objects.filter(title__icontains=q)
    return render(request, 'blog/results.html', {'error_msg': error_msg,
                                                 'post_list': post_list})


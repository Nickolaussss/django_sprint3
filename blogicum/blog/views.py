from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from blog.models import Post, Category

import datetime


def index(request):
    template = 'blog/index.html'
    post_list = Post.objects.select_related(
        'location'
    ).filter(
        pub_date__lt=datetime.datetime.now(),
        is_published=True,
        category__is_published=True
    ).order_by('-created_at')[:5]
    context = {
        'post_list': post_list
    }
    return render(request, template, context)


def post_detail(request, id):
    template = 'blog/detail.html'
    post = get_object_or_404(
        Post.objects.select_related('location').filter(
            Q(is_published=True),
            Q(category__is_published=True),
            pub_date__lt=datetime.datetime.now(),
        ),
        pk=id
    )
    context = {
        'post': post
    }
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category.objects.values('title', 'description').filter(is_published=True),
        slug=category_slug
    )
    post_list = Post.objects.select_related(
        'location'
    ).filter(
        category__slug=category_slug,
        is_published=True,
        pub_date__lt=datetime.datetime.now()
    )
    context = {
        'category': category,
        'post_list': post_list
    }
    return render(request, template, context)

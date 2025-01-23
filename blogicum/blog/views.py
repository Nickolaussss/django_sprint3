from django.shortcuts import render, get_object_or_404

from blog.models import Post, Category

import datetime

num_objects = 5


def index(request):
    template = 'blog/index.html'
    post_list = display(
        note_relations(Post.objects)
    ).order_by('created_at')[:num_objects]
    context = {
        'post_list': post_list
    }
    return render(request, template, context)


def post_detail(request, id):
    template = 'blog/detail.html'
    post = get_object_or_404(
        display(note_relations(Post.objects)),
        pk=id
    )
    context = {
        'post': post
    }
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category.objects.values(
            'title', 'description'
        ).filter(is_published=True),
        slug=category_slug
    )
    post_list = display(note_relations(Post.objects)).filter(
        category__slug=category_slug
    )
    context = {
        'category': category,
        'post_list': post_list
    }
    return render(request, template, context)


def note_relations(notes):
    return notes.select_related('location')


def display(notes):
    return notes.filter(
        category__is_published=True,
        is_published=True,
        pub_date__lt=datetime.datetime.now()

    )

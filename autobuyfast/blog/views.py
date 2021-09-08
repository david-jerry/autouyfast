try:
    from urllib import quote_plus  # python 2
except:
    pass

try:
    from urllib.parse import quote_plus  # python 3
except:
    pass

import datetime

import django.contrib.sites.models
from category.models import Category, Tag
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import transaction
from django.db.models import Count, F, Q, Sum
from django.http import HttpResponseForbidden, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, FormMixin, UpdateView
# from angalabiri.blog.forms import CommentForm
from next_prev import next_in_order, prev_in_order

from .forms import EmailPostForm
from .models import Post  # , Comment

User = get_user_model()

# Create your views here.
class PostList(ListView):
    model = Post
    template_name = "blog/list.html"
    ordering = ["title", "-pub_date"]
    context_object_name = "posts"
    allow_empty = True
    paginate_by = 5
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self): # new
        # cat = get_object_or_404(Category, slug="news")
        # object_list = Post.objects.all_posts().filter(categories__slug__in=[cat])
        object_list = Post.objects.all_posts().filter(categories__slug="news")
        return object_list


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        request = self.request
        # site = Site.objects.get_or_create(id=settings.SITE_ID, domain="autobuyfast.com", name="autobuyfast.com")
        # site = Site.objects.get_or_create(id=2, domain="autobuyfast.com", name="autobuyfast")
        cat = get_object_or_404(Category, slug="news")
        tags = Tag.objects.all().filter(categories__slug="news")
        context["tags"] = tags
        return context

def reviews_posts(request):
    object_list = Post.objects.all_posts().filter(categories__slug="reviews")
    tags = Tag.objects.all().filter(categories__slug="reviews")

    paginator = Paginator(object_list, 5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    data = {
        'page': page,
        'posts': posts,
        'tags': tags,
    }        
    return render(request, 'blog/review_list.html', data)


# class ReviewList(ListView):
#     model = Post
#     template_name = "blog/review_list.html"
#     ordering = ["title", "-pub_date"]
#     queryset = Post.objects.all_posts().filter(tags__title="reviews")
#     context_object_name = "posts"
#     allow_empty = True
#     paginate_by = 5
#     slug_field = "slug"
#     slug_url_kwarg = "slug"

#     def get_context_data(self, *args, **kwargs):
#         context = super().get_context_data(*args, **kwargs)
#         request = self.request
#         tags = Tag.objects.all()
#         categories = Category.objects.all()
#         recent_posts = Post.objects.recent_posts().filter(tags__title="reviews")[:5]
#         context["tags"] = tags
#         context["categories"] = categories
#         context["recent_posts"] = recent_posts
#         return context


class SearchPostList(ListView):
    model = Post
    template_name = "blog/search_list.html"
    ordering = ["title", "-pub_date"]
    context_object_name = "posts"
    allow_empty = True
    paginate_by = 5
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self): # new
        query = self.request.GET.get('q')
        return Post.objects.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query)
        ).distinct()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        request = self.request
        tags = Tag.objects.all()
        context["tags"] = tags
        return context


# "all_news_category": Post.objects.all_posts().filter(categories__slug="news"),

def tag_posts(request, tag_slug=None):
    object_list = Post.objects.all_posts()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag], status="published")
        print("tag object id = ", object_list)

    tags = Tag.objects.all()

    paginator = Paginator(object_list, 5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    data = {
        'page': page,
        'posts': posts,
        'tags': tags,
        'tag': tag
    }        
    return render(request, 'blog/tags.html', data)



# def cat_posts(request, cat_slug=None):
#     object_list = Post.objects.all()
#     cat = None

#     if cat_slug:
#         cat = get_object_or_404(Category, slug=cat_slug)
#         object_list = object_list.filter(categories__in=[cat], status="published")
#         print("tag object id = ", object_list)

#     tags = Tag.objects.all()
#     categories = Category.objects.all()
#     recent_posts = Post.objects.recent_posts()[:5]

#     paginator = Paginator(object_list, 5)
#     page = request.GET.get('page')
#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         # If page is not an integer deliver the first page
#         posts = paginator.page(1)
#     except EmptyPage:
#         # If page is out of range deliver last page of results
#         posts = paginator.page(paginator.num_pages)
#     data = {
#         'page': page,
#         'posts': posts,
#         'tags': tags,
#         'categories': categories,
#         'recent_posts': recent_posts,
#         'cat': cat
#     }        
#     return render(request, 'blog/categories.html', data)


def post_share(request, slug):
    post = get_object_or_404(Post, slug=slug, status="published")
    if not request.method == "POST":
        HttpResponseForbidden

    tags = Tag.objects.all()
    categories = Category.objects.all()
    recent_posts = Post.objects.recent_posts()[:5]

    form = EmailPostForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        post_url = request.build_absolute_url(post.get_absolute_url())
        subject = f"{cd['name']} recommends you read {post.title}"
        message = f"Read {post.title} at {post_url} \n\n {cd['name']}\'s comments: {cd['comments']}"
        send_mail(
            subject,
            message,
            "no-reply@autobuyfast.com",
            [cd['to']],
            fail_silently=False
        )
        messages.success(request, f"You have successfully shared {post.title}")
        return HttpResponseRedirect(reverse_lazy('blogs:list'))
    else:
        form = EmailPostForm()

    data = {
        'tags': tags,
        'categories': categories,
        'recent_posts': recent_posts,
        'post': post, 
        'form': form
    }
    
    return render(request, 'blog/share.html', data)




def PostDetail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    tags = Tag.objects.all()
    post_tags_ids = post.tags.values_list('id', flat=True)
    related_posts = Post.objects.all_posts().filter(tags__in=post_tags_ids).exclude(id=post.id)
    related_posts = related_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-pub_date')[:5]

    qs = Post.objects.all_posts()
    newest = qs.first()
    second_newest = next_in_order(newest, qs=qs)
    oldest = prev_in_order(newest, qs=qs, loop=True)



    data = {
        "post": post,
        'posts': qs,
        'related_posts': related_posts,
        'newest': newest,
        'next_post': second_newest,
        'prev_post': oldest,
        "tags": tags
    }
    return render(request, "blog/detail.html", data)



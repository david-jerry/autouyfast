from django.urls import path

from .views import (
    PostDetail,
    PostList,
    ReviewList,
    SearchPostList,
    cat_posts,
    post_share,
    tag_posts,
)

app_name = "blogs"
urlpatterns = [
    path('', PostList.as_view(), name='list'),
    path('reviews/', ReviewList.as_view(), name='rlist'),
    path('search/', SearchPostList.as_view(), name="search"),
    path('<slug>/', PostDetail, name='detail'),
    path('<slug>/share/', post_share, name='share'),
    path('tag/<slug:tag_slug>/', tag_posts, name='posts_by_tag'),
    path('category/<slug:cat_slug>/', cat_posts, name='posts_by_cat'),
]

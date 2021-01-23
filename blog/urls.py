from django.urls import path

from .views import (
    HomePageView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
)

urlpatterns = [
    path('', HomePageView.as_view(), name='blog_home'),
    path('user/<str:username>/', UserPostListView.as_view(), name='user_posts'),
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    path('new_post/', PostCreateView.as_view(), name='post_create'),
    path('post/<slug:slug>/update', PostUpdateView.as_view(), name='post_update'),
    path('post/<slug:slug>/delete', PostDeleteView.as_view(), name='post_delete'),
]

from django.urls import path, include
from .views import UserDetail, AllUsers, TopReviewers, UserUpdate, UserReviews

urlpatterns = [
    path('user/all_users/', AllUsers.as_view(), name='all_users'),
    path('user/top_reviewers/', TopReviewers.as_view(), name='top_reviewers'),
    path('user/<int:pk>/', UserDetail.as_view(), name='profile_detail'),
    path('user/<int:pk>/update/', UserUpdate.as_view(), name='profile_update'),
    path('user/<int:pk>/reviews/', UserReviews.as_view(), name='profile_reviews'),
    path('', include('allauth.urls')),
]

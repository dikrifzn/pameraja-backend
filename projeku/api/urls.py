from django.urls import path
from .views import UserAPI, SocialMediaAPI, UserProfileAPI

urlpatterns = [
    path('users/', UserAPI.as_view(), name='user-list'),
    path('users/<int:id>/', UserProfileAPI.as_view(), name='user-profile'),
    path('socialmedias/', SocialMediaAPI.as_view(), name='socialmedia-list'),
]

from django.urls import path
from .views import UserAPI, SocialMediaAPI, UserProfileAPI, ProjectAPI, CommentAPI

urlpatterns = [
    path('users/', UserAPI.as_view(), name='user-list'),
    path('users/<int:id>', UserProfileAPI.as_view(), name='user-profile'),
    path('social-media/<int:id>', SocialMediaAPI.as_view(), name='socialmedia-list'),
    path('project/', ProjectAPI.as_view(), name='project-all'),
    path('project/<int:id>', ProjectAPI.as_view(), name='project-list'),
    path('comment/<int:id>', CommentAPI.as_view(), name='comment-project'),
]

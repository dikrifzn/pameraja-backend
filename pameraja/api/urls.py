from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterView, LogoutView,
    UserProfileAPI,
    SocialMediaAPI, ProjectAPI,
    CommentAPI, LikeAPI
)

urlpatterns = [
    # Auth
    path('auth/register/', RegisterView.as_view(), name='auth-register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='auth-login'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='auth-token-refresh'),
    path('auth/logout/', LogoutView.as_view(), name='auth-logout'),

    # User
    path('users/', UserProfileAPI.as_view(), name='user-detail'), # GET, PUT, DELETE

    # Social Media (per user)
    path('users/social-media/', SocialMediaAPI.as_view(), name='user-social-media'),  # GET, POST, PUT, DELETE
    path('users/social-media/<int:id>/', SocialMediaAPI.as_view(), name='user-social-media-detail'),  # PUT, DELETE

    # Projects
    path('projects/', ProjectAPI.as_view(), name='project-list'), # GET (all), POST (by id_user in path/data)
    path('projects/<int:id>/', ProjectAPI.as_view(), name='project-detail'), # GET (by id), PUT, DELETE

    # Comments on project
    path('projects/<int:id>/comments/', CommentAPI.as_view(), name='comment-list-create'),  # GET (list), POST (create)
    path('comments/<int:id>/', CommentAPI.as_view(), name='comment-update-delete'),  # PUT, DELETE (by comment id)

    # Likes on project
    path('projects/<int:id>/likes/', LikeAPI.as_view(), name='project-likes'),
]
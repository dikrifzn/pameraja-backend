from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserAPI, SocialMediaAPI, UserProfileAPI, ProjectAPI, CommentAPI, LikeAPI, RegisterView, LogoutView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('users/', UserAPI.as_view(), name='user-list'),
    path('users/<int:id>', UserProfileAPI.as_view(), name='user-profile'),
    path('social-media/<int:id>', SocialMediaAPI.as_view(), name='socialmedia-list'),
    path('project/', ProjectAPI.as_view(), name='project-all'),
    path('project/<int:id>', ProjectAPI.as_view(), name='project-list'),
    path('comment/<int:id>', CommentAPI.as_view(), name='comment-project'),
    path('like/<int:id>', LikeAPI.as_view(), name='like-project')
]

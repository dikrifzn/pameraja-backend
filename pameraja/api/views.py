from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from .models import User, SocialMedia, Project, Comment, Like
from .serializers import UserSerializer, SocialMediaSerializer, ProjectSerializer, CommentSerializer, LikeSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from utils.response import success_response, error_response

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")

        if User.objects.filter(username=username).exists():
            return error_response("Username already exists", {"username": ["Already taken"]})
        user = User.objects.create_user(username=username, password=password, email=email)
        return success_response("User created successfully", {"id": user.id, "username": user.username}, 201)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return success_response("Logged out successfully", status_code=205)
        except Exception as e:
            return error_response("Logout failed", {"detail": str(e)}, 400)

class UserAPI(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return success_response("User data retrieved successfully", serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response("User created successfully", serializer.data, 201)
        return error_response("Failed to create user", serializer.errors)

class UserProfileAPI(APIView):
    def get(self, request, id):
        try:
            user = User.objects.get(id=id)
            serializer = UserSerializer(user)
            return success_response("User profile retrieved successfully", serializer.data)
        except User.DoesNotExist:
            return error_response("User not found", status_code=404)

    def put(self, request, id):
        try:
            user = User.objects.get(id=id)
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return success_response("User profile updated successfully", serializer.data)
            return error_response("Failed to update user profile", serializer.errors)
        except User.DoesNotExist:
            return error_response("User not found", status_code=404)

    def delete(self, request, id):
        try:
            user = User.objects.get(id=id)
            user.delete()
            return success_response("User deleted successfully", status_code=204)
        except User.DoesNotExist:
            return error_response("User not found", status_code=404)

class SocialMediaAPI(APIView):
    def get(self, request, id):
        if not User.objects.filter(id=id).exists():
            return error_response("User not found", status_code=404)
        socialmedias = SocialMedia.objects.filter(id_user=id)
        serializer = SocialMediaSerializer(socialmedias, many=True)
        return success_response("Social Media retrieved successfully", serializer.data)

    def post(self, request, id):
        if not User.objects.filter(id=id).exists():
            return error_response("User not found", status_code=404)
        serializer = SocialMediaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response("Social media account added successfully", serializer.data, 201)
        return error_response("Failed to add social media", serializer.errors)

    def put(self, request, id):
        id_user = request.data.get("id_user")
        try:
            user = User.objects.get(id=id_user)
            socialmedia = SocialMedia.objects.get(id=id, id_user=user)
            serializer = SocialMediaSerializer(socialmedia, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return success_response("Social Media updated successfully", serializer.data)
            return error_response("Failed to update Social Media", serializer.errors)
        except (User.DoesNotExist, SocialMedia.DoesNotExist):
            return error_response("User or Social Media not found", status_code=404)

    def delete(self, request, id):
        social_media_id = request.data.get("social_media_id")
        try:
            social_media = SocialMedia.objects.get(id=social_media_id, id_user_id=id)
            social_media.delete()
            return success_response("Social Media deleted successfully")
        except SocialMedia.DoesNotExist:
            return error_response("Social Media not found", status_code=404)

class ProjectAPI(APIView):
    def get(self, request, id=None):
        query = request.GET.get('search')
        id_user = request.GET.get('id_user')

        if id is not None:
            try:
                project = Project.objects.get(id=id)
                serializer = ProjectSerializer(project)
                return success_response("Project retrieved", serializer.data)
            except Project.DoesNotExist:
                return error_response("Project not found", status_code=404)

        projects = Project.objects.all().order_by('-created_at')
        if id_user:
            projects = projects.filter(id_user=id_user)
        if query:
            projects = projects.filter(Q(title__icontains=query) | Q(description__icontains=query))

        paginator = PageNumberPagination()
        paginated = paginator.paginate_queryset(projects, request, view=self)
        serializer = ProjectSerializer(paginated, many=True)
        return paginator.get_paginated_response({
            "status": True,
            "message": "Project list retrieved successfully",
            "data": serializer.data
        })

    def post(self, request, id):
        if not User.objects.filter(id=id).exists():
            return error_response("User not found", status_code=404)
        request_data = request.data.copy()
        request_data['id_user'] = id
        serializer = ProjectSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return success_response("Project added successfully", serializer.data, 201)
        return error_response("Failed to add project", serializer.errors)

    def put(self, request, id):
        id_user = request.data.get("id_user")
        try:
            user = User.objects.get(id=id_user)
            project = Project.objects.get(id=id, id_user=user)
        except (User.DoesNotExist, Project.DoesNotExist):
            return error_response("User or Project not found", status_code=404)
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response("Project updated successfully", serializer.data)
        return error_response("Failed to update project", serializer.errors)

    def delete(self, request, id):
        project_id = request.data.get("project_id")
        try:
            project = Project.objects.get(id=project_id, id_user_id=id)
            project.delete()
            return success_response("Project deleted successfully")
        except Project.DoesNotExist:
            return error_response("Project not found", status_code=404)

class CommentAPI(APIView):
    def get(self, request, id):
        if not Project.objects.filter(id=id).exists():
            return error_response("Project not found", status_code=404)
        comments = Comment.objects.filter(id_project=id).order_by('-created_at')
        serializer = CommentSerializer(comments, many=True)
        return success_response("Comments retrieved successfully", serializer.data)

    def post(self, request, id):
        data = request.data.copy()
        data['id_project'] = id
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return success_response("Comment added successfully", serializer.data, 201)
        return error_response("Failed to add comment", serializer.errors)

    def put(self, request, id):
        try:
            comment = Comment.objects.get(id=id)
        except Comment.DoesNotExist:
            return error_response("Comment not found", status_code=404)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_response("Comment updated successfully", serializer.data)
        return error_response("Failed to update comment", serializer.errors)

    def delete(self, request, id):
        try:
            comment = Comment.objects.get(id=id)
            comment.delete()
            return success_response("Comment deleted successfully", status_code=204)
        except Comment.DoesNotExist:
            return error_response("Comment not found", status_code=404)

class LikeAPI(APIView):
    def get(self, request, id):
        if not Project.objects.filter(id=id).exists():
            return error_response("Project not found", status_code=404)
        likes = Like.objects.filter(id_project=id)
        user_serializer = UserSerializer([like.id_user for like in likes], many=True)
        return success_response("Likes retrieved successfully", {
            "likes_count": likes.count(),
            "liked_by": user_serializer.data
        })

    def post(self, request, id):
        id_user = request.data.get("id_user")
        if not User.objects.filter(id=id_user).exists() or not Project.objects.filter(id=id).exists():
            return error_response("User or Project not found", status_code=404)

        like, created = Like.objects.get_or_create(id_user_id=id_user, id_project_id=id)
        if not created:
            like.delete()
            return success_response("Like removed successfully")
        return success_response("Like added successfully", status_code=201)
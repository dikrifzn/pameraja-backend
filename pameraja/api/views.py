from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from .models import SocialMedia, Project, Comment, Like
from .serializers import UserSerializer, SocialMediaSerializer, ProjectSerializer, CommentSerializer, LikeSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import MultiPartParser, FormParser
from utils.response import success_response, error_response

User = get_user_model()


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

class UserProfileAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return success_response("User profile retrieved successfully", serializer.data)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response("User profile updated successfully", serializer.data)
        return error_response("Failed to update user profile", serializer.errors)

    def delete(self, request):
        request.user.delete()
        return success_response("User deleted successfully", status_code=204)


class SocialMediaAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        socialmedias = SocialMedia.objects.filter(id_user=request.user)
        serializer = SocialMediaSerializer(socialmedias, many=True)
        return success_response("Social Media retrieved successfully", serializer.data)

    def post(self, request):
        data = request.data.copy()
        data['id_user'] = request.user.id
        serializer = SocialMediaSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return success_response("Social media account added successfully", serializer.data, 201)
        return error_response("Failed to add social media", serializer.errors)

    def put(self, request, id):
        try:
            socialmedia = SocialMedia.objects.get(id=id, id_user=request.user)
            serializer = SocialMediaSerializer(socialmedia, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return success_response("Social Media updated successfully", serializer.data)
            return error_response("Failed to update Social Media", serializer.errors)
        except SocialMedia.DoesNotExist:
            return error_response("Social Media not found", status_code=404)

    def delete(self, request, id):
        try:
            social_media = SocialMedia.objects.get(id=id, id_user=request.user)
            social_media.delete()
            return success_response("Social Media deleted successfully")
        except SocialMedia.DoesNotExist:
            return error_response("Social Media not found", status_code=404)


class ProjectAPI(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, id=None):
        query = request.GET.get('search')

        if id is not None:
            try:
                project = Project.objects.get(id=id, id_user=request.user)
                serializer = ProjectSerializer(project)
                return success_response("Project retrieved", serializer.data)
            except Project.DoesNotExist:
                return error_response("Project not found", status_code=404)

        projects = Project.objects.filter(id_user=request.user).order_by('-created_at')
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

    def post(self, request):
        request_data = request.data.copy()
        request_data['id_user'] = request.user.id

        serializer = ProjectSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return success_response("Project added successfully", serializer.data, 201)
        return error_response("Failed to add project", serializer.errors)

    def put(self, request, id):
        try:
            project = Project.objects.get(id=id, id_user=request.user)
        except Project.DoesNotExist:
            return error_response("Project not found", status_code=404)

        serializer = ProjectSerializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_response("Project updated successfully", serializer.data)
        return error_response("Failed to update project", serializer.errors)

    def delete(self, request, id):
        try:
            project = Project.objects.get(id=id, id_user=request.user)
            project.delete()
            return success_response("Project deleted successfully")
        except Project.DoesNotExist:
            return error_response("Project not found", status_code=404)


class CommentAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        if not Project.objects.filter(id=id).exists():
            return error_response("Project not found", status_code=404)
        comments = Comment.objects.filter(id_project=id).order_by('-created_at')
        serializer = CommentSerializer(comments, many=True)
        return success_response("Comments retrieved successfully", serializer.data)

    def post(self, request, id):
        data = request.data.copy()
        data['id_project'] = id
        data['id_user'] = request.user.id
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return success_response("Comment added successfully", serializer.data, 201)
        return error_response("Failed to add comment", serializer.errors)

    def put(self, request, id):
        try:
            comment = Comment.objects.get(id=id, id_user=request.user)
        except Comment.DoesNotExist:
            return error_response("Comment not found", status_code=404)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_response("Comment updated successfully", serializer.data)
        return error_response("Failed to update comment", serializer.errors)

    def delete(self, request, id):
        try:
            comment = Comment.objects.get(id=id, id_user=request.user)
            comment.delete()
            return success_response("Comment deleted successfully", status_code=204)
        except Comment.DoesNotExist:
            return error_response("Comment not found", status_code=404)


class LikeAPI(APIView):
    permission_classes = [IsAuthenticated]

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
        if not Project.objects.filter(id=id).exists():
            return error_response("Project not found", status_code=404)

        like, created = Like.objects.get_or_create(id_user=request.user, id_project_id=id)
        if not created:
            like.delete()
            return success_response("Like removed successfully")
        return success_response("Like added successfully", status_code=201)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from .models import User, SocialMedia, Project, Comment, Like
from .serializers import UserSerializer, SocialMediaSerializer, ProjectSerializer, CommentSerializer, LikeSerializer

# Create your views here.
class UserAPI(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response({
            "message": "Data retrieved successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "User created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "message": "Failed to create user",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
class UserProfileAPI(APIView):
    # Get user profile by ID
    def get(self, request, id):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({
                "message": "User not found"
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user)
        return Response({
            "message": "User profile retrieved successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    # Update user profile by ID
    def put(self, request, id):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({
                "message": "User not found"
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "User profile updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "message": "Failed to update user profile",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    # Delete user profile by ID
    def delete(self, request, id):
        try:
            user = User.objects.get(id=id)
            user.delete()
            return Response({
                "message": "User deleted successfully"
            }, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({
                "message": "User not found"
            }, status=status.HTTP_404_NOT_FOUND)
    
class SocialMediaAPI(APIView):
    # Get Social Media by ID User
    def get(self, request, id):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({
                "message": "User not found"
            }, status=status.HTTP_404_NOT_FOUND)
        
        try:
            socialmedias = SocialMedia.objects.filter(id_user=id)
            serializer = SocialMediaSerializer(socialmedias, many=True)
            return Response({
                "message": "Social Media User retrieved successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except SocialMedia.DoesNotExist:
            return Response({
                "message": "Social Media not found"
            }, status=status.HTTP_404_NOT_FOUND)

    # Add Social Media by ID User
    def post(self, request, id):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({
                "message": "User not found"
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = SocialMediaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Social media account added successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Update Social Media user profile by ID
    def put(self, request, id):
        try:
            id_user_id = request.data.get("id_user")
            user = User.objects.get(id=id_user_id)
        except User.DoesNotExist:
            return Response({
                "message": "User not found"
            }, status=status.HTTP_404_NOT_FOUND)
        socialmedia = SocialMedia.objects.get(id=id, id_user=id_user_id)
        serializer = SocialMediaSerializer(socialmedia, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Social Media User updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "message": "Failed to update user Social Media User",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Delete Social Media by ID User
    def delete(self, request, id):
        try:
            social_media_id = request.data.get("social_media_id")
            social_media = SocialMedia.objects.get(id=social_media_id, id_user_id=id)
            social_media.delete()
            return Response({"message": "Social Media berhasil dihapus"}, status=200)
        except SocialMedia.DoesNotExist:
            return Response({"error": "Data tidak ditemukan"}, status=404)

class ProjectAPI(APIView):
    def get(self, request, id=None):
        query = request.GET.get('search', None)
        if id is not None:
            try:
                project = Project.objects.get(id=id)
                serializer = ProjectSerializer(project)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Project.DoesNotExist:
                return Response({"message": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

        id_user = request.GET.get('id_user', None)
        if id_user:
            projects = Project.objects.filter(id_user=id_user).order_by('-created_at')
        else:
            projects = Project.objects.all().order_by('-created_at')

        if query:
            projects = projects.filter(Q(title__icontains=query) | Q(description__icontains=query))

        paginator = PageNumberPagination()
        paginated_projects = paginator.paginate_queryset(projects, request, view=self)

        serializer = ProjectSerializer(paginated_projects, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    def post(self, request, id):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({
                "message": "User not found"
            }, status=status.HTTP_404_NOT_FOUND)

        # Tambahkan id_user ke data yang dikirim sebelum diserialisasi
        request_data = request.data.copy()
        request_data['id_user'] = user.id  

        serializer = ProjectSerializer(data=request_data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Project added successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "message": "Failed to add project",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        try:
            id_user = request.data.get("id_user")
            user = User.objects.get(id=id_user)
            project = Project.objects.filter(id=id)
        except User.DoesNotExist:
            return Response({
                "message": "User not found"
            }, status=status.HTTP_404_NOT_FOUND)
        project = Project.objects.get(id=id, id_user=user)
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Project User updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "message": "Failed to update Project User",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, id):
        try:
            user = User.objects.get(id=id)
            project_id = request.data.get("project_id")
            project = Project.objects.get(id=project_id, id_user=user)
            project.delete()
            return Response({"message": "Project berhasil dihapus"}, status=200)
        except Project.DoesNotExist:
            return Response({"error": "Data tidak ditemukan"}, status=404)

class CommentAPI(APIView):
    def get(self, request, id):
        try:
            id_user = request.data.get("id_user")
            id_project = id
            user = User.objects.get(id=id_user)
            project = Project.objects.get(id=id_project)
        except Project.DoesNotExist:
            return Response({
                "message": "Project not found"
            }, status=status.HTTP_404_NOT_FOUND)
        try:
            comments = Comment.objects.filter(id_project=id_project).order_by('-created_at')
            serializer = CommentSerializer(comments, many=True)
            return Response({
                "message": "Comments Project retrieved successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Comment.DoesNotExist:
            return Response({
                "message": "Comment not found"
            }, status=status.HTTP_404_NOT_FOUND)
    def post(self, request, id):
        data = request.data.copy()
        data['id_project'] = id
        
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Comment added successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, id):
        try:
            comment = Comment.objects.get(id=id)
        except Comment.DoesNotExist:
            return Response({"message": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Comment updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        try:
            comment = Comment.objects.get(id=id)
        except Comment.DoesNotExist:
            return Response({"message": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)
        
        comment.delete()
        return Response({"message": "Comment deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
class LikeAPI(APIView):
    def get(self, request, id):
        if not Project.objects.filter(id=id).exists():
            return Response({"message": "Project not found"}, status=status.HTTP_404_NOT_FOUND)
        
        likes = Like.objects.filter(id_project=id)
        likes_count = likes.count()
        users = [like.id_user for like in likes]
        user_serializer = UserSerializer(users, many=True)
        
        return Response({
            "message": "Likes retrieved successfully",
            "likes_count": likes_count,
            "liked_by": user_serializer.data
        }, status=status.HTTP_200_OK)
    
    def post(self, request, id):
        id_user = request.data.get("id_user")
        
        if not User.objects.filter(id=id_user).exists() or not Project.objects.filter(id=id).exists():
            return Response({"message": "User or Project not found"}, status=status.HTTP_404_NOT_FOUND)
        
        like, created = Like.objects.get_or_create(id_user_id=id_user, id_project_id=id)
        
        if not created:
            like.delete()
            return Response({"message": "Like removed successfully"}, status=status.HTTP_200_OK)
        
        return Response({"message": "Like added successfully"}, status=status.HTTP_201_CREATED)
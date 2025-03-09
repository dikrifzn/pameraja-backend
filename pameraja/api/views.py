from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from .models import User, SocialMedia, Project, Comment
from .serializers import UserSerializer, SocialMediaSerializer, ProjectSerializer, CommentSerializer

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
        if id is not None:
            try:
                user = User.objects.get(id=id)
                projects = Project.objects.filter(id_user=user).order_by('-created_at')
            except User.DoesNotExist:
                return Response({
                    "message": "User not found"
                }, status=status.HTTP_404_NOT_FOUND)
        else:
            projects = Project.objects.all().order_by('-created_at')

        paginator = PageNumberPagination()
        paginated_projects = paginator.paginate_queryset(projects, request)

        serializer = ProjectSerializer(paginated_projects, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    def post(self, request, id):
        try:
            user = User.objects.get(id=id)
            projects = Project.objects.filter(id_user=user).order_by('-created_at')
        except User.DoesNotExist:
            return Response({
                "message": "User not found"
            }, status=status.HTTP_404_NOT_FOUND)
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Project added successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request, id):
        try:
            user = User.objects.get(id=id)
            project = Project.objects.filter(id_user=user)
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
        pass
    def put(self, request, id):
        pass
    def delete(self, request, id):
        pass
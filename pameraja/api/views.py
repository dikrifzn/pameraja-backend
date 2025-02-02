from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, SocialMedia
from .serializers import UserSerializer, SocialMediaSerializer

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
            socialmedias = SocialMedia.objects.get(id_user=id)
            serializer = SocialMediaSerializer(socialmedias)
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

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
    def get(self, request):
        socialmedias = SocialMedia.objects.all()
        serializer = SocialMediaSerializer(socialmedias, many=True)
        return Response({
            "message": "Data retrieved successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
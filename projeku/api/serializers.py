from rest_framework import serializers
from .models import User, SocialMedia, Project, Comment, Like

class UserSerializer (serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    class Meta:
        model = User
        fields = '__all__'

    def update(self, instance, validated_data):
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.position = validated_data.get('position', instance.position)
        instance.address = validated_data.get('address', instance.address)
        instance.save()
        return instance

class SocialMediaSerializer (serializers.ModelSerializer):
    class Meta:
        model = SocialMedia
        fields = '__all__'

class ProjectSerializer (serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class CommentSerializer (serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class LikeSerializer (serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'
from django.db import models
import uuid
import os
from datetime import datetime
from django.contrib.auth.models import AbstractUser
# from your_app.utils import upload_user_image

def upload_user_image(instance, filename):
    ext = filename.split('.')[-1]
    user_id = instance.id
    date_str = datetime.now().strftime('%Y%m%d')
    random_str = uuid.uuid4().hex[:16]
    filename = f"{user_id}_{date_str}_{random_str}.{ext}"
    return os.path.join('users_images', filename)

def upload_project_image(instance, filename):
    ext = filename.split('.')[-1]
    user_id = instance.id_user.id if instance.id_user else 'anon'
    date_str = datetime.now().strftime('%Y%m%d')
    random_str = uuid.uuid4().hex[:16]
    filename = f"{user_id}_{date_str}_{random_str}.{ext}"
    return os.path.join('projects_images', filename)

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    position = models.CharField(max_length=225)
    address = models.TextField()
    image_url = models.ImageField(upload_to=upload_user_image, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

class SocialMedia(models.Model):
    id_user = models.ForeignKey("User", verbose_name=("id_user"), on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        user = self.id_user.username if self.id_user else "Unknown"
        return f"{user}'s {self.name}"
    
class Project(models.Model):
    id_user = models.ForeignKey("User", verbose_name=("id_user"), on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=225)
    description = models.TextField()
    category = models.CharField(max_length=225)
    file_url = models.CharField(null=True, blank=True)
    image_url = models.ImageField(upload_to=upload_project_image, null=True, blank=True)
    views = models.IntegerField(null=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        user = self.id_user.username if self.id_user else "Unknown"
        return f"{self.title} made by {user}"

class Comment(models.Model):
    id_user = models.ForeignKey("User", verbose_name=("id_user"), on_delete=models.CASCADE, null=True)
    id_project = models.ForeignKey("Project", verbose_name=("id_project"), on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        user = self.id_user.username if self.id_user else "Unknown"
        return f"{user} commented {self.id_project.title}"

class Like(models.Model):
    id_user = models.ForeignKey("User", verbose_name=("id_user"), on_delete=models.CASCADE, null=True)
    id_project = models.ForeignKey("Project", verbose_name=("id_project"), on_delete=models.CASCADE)

    def __str__(self):
        user = self.id_user.username if self.id_user else "Unknown"
        return f"{user} liked {self.id_project.title}"
    
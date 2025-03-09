from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    position = models.CharField(max_length=225)
    password = models.CharField(max_length=255)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class SocialMedia(models.Model):
    id_user = models.ForeignKey("User", verbose_name=("id_user"), on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id_user.name}'s {self.name}"
    
class Project(models.Model):
    id_user = models.ForeignKey("User", verbose_name=("id_user"), on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=225)
    description = models.TextField()
    category = models.CharField(max_length=225)
    file_url = models.CharField(max_length=225, null=True)
    image_url = models.CharField(max_length=225, null=True)
    views = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} made by {self.id_user.name}"

class Comment(models.Model):
    id_user = models.ForeignKey("User", verbose_name=("id_user"), on_delete=models.CASCADE, null=True)
    id_project = models.ForeignKey("Project", verbose_name=("id_project"), on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id_user.name} commented {self.id_project.title}"

class Like(models.Model):
    id_user = models.ForeignKey("User", verbose_name=("id_user"), on_delete=models.CASCADE, null=True)
    id_project = models.ForeignKey("Project", verbose_name=("id_project"), on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id_user.name} liked {self.id_project.title}"
    
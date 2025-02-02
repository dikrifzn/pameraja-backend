from django.contrib import admin
from .models import User, SocialMedia, Project, Comment, Like
# Register your models here.
admin.site.register(User)
admin.site.register(SocialMedia)
admin.site.register(Project)
admin.site.register(Comment)
admin.site.register(Like)

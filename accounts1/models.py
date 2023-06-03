from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    email = models.CharField(max_length=30, default='', null=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Profile1(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    forget_password_token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class SearchModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    keyword = models.CharField(max_length=50, null=False, unique=False)
    category = models.CharField(max_length=50, null=False, unique=False)

    def __str__(self):
        return self.user.username


class Playlist(models.Model):
    keyword = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    pid = models.CharField(max_length=255, default='')
    view_count = models.IntegerField()
    se = models.IntegerField(default=0)
    vc = models.IntegerField(default=0)
    time = models.IntegerField(default=0)
    hours = models.IntegerField(default=0)
    minutes = models.IntegerField(default=0)
    def __str__(self):
        return self.title
from django.db import models
from django.contrib.auth.models import User


class MyUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_image/',
                                      default='profile_image/Screenshot_from_2024-05-13_12-39-29.png')
    follower_count = models.PositiveIntegerField(default=0)
    following_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}"


class Post(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    is_published = models.BooleanField(default=True)
    post_image = models.ImageField(upload_to='post/', blank=True, null=True)
    view_count = models.IntegerField(default=0)
    like_count = models.PositiveIntegerField(default=0)
    comment_count = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f"{self.author.user.username}"


class CommentPost(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    message = models.CharField(max_length=200)
    is_visible = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


class LikePost(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


class FollowMyUser(models.Model):
    follower = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='follower_user')
    following = models.ForeignKey(MyUser, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

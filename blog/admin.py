from django.contrib import admin

from .models import Post, MyUser, CommentPost, LikePost, FollowMyUser


class PostInline(admin.TabularInline):
    model = CommentPost
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [PostInline]
    list_display = ('id', 'author', 'comment_count', 'post_image', 'is_published', 'view_count', 'created_at')
    list_display_links = ('id', 'author')


@admin.register(CommentPost)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'is_visible', 'created_at')
    list_display_links = ('id', 'author')


@admin.register(LikePost)
class LikePostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'created_at')
    list_display_links = ('id', 'author')


@admin.register(FollowMyUser)
class FollowMyUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'follower', 'following', 'created_at')
    list_display_links = ('id', 'follower')


@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'follower_count', 'created_at')
    list_display_links = ('id', 'user')

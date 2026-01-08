from django.contrib import admin
from .models import Genre, Post, Comment, PostLike, CommentLike, Follow, UserProfile


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'genre', 'is_published', 'created_at', 'likes_count']
    list_filter = ['genre', 'is_published', 'created_at', 'author']
    search_fields = ['title', 'content', 'author__username']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']

    def likes_count(self, obj):
        return obj.likes_count
    likes_count.short_description = 'Likes'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'parent', 'created_at', 'likes_count']
    list_filter = ['created_at', 'post']
    search_fields = ['content', 'author__username', 'post__title']
    raw_id_fields = ['author', 'post', 'parent']
    date_hierarchy = 'created_at'

    def likes_count(self, obj):
        return obj.likes_count
    likes_count.short_description = 'Likes'


@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created_at']
    list_filter = ['created_at']
    raw_id_fields = ['user', 'post']


@admin.register(CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'comment', 'created_at']
    list_filter = ['created_at']
    raw_id_fields = ['user', 'comment']


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['follower', 'following', 'created_at']
    list_filter = ['created_at']
    raw_id_fields = ['follower', 'following']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'dark_mode', 'created_at']
    list_filter = ['dark_mode', 'created_at']
    search_fields = ['user__username', 'user__email', 'bio']
    raw_id_fields = ['user']
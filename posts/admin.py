from django.contrib import admin

from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_short_description', 'user', 'created_at', 'updated_at']
    list_filter = ['user', 'created_at', 'updated_at']
    search_fields = ['description', 'body']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_short_body', 'user', 'post', 'created_at']
    list_filter = ['user', 'post', 'created_at']
    search_fields = ['body']
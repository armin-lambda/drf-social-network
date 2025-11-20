from rest_framework import serializers
from rest_framework.reverse import reverse

from accounts.serializers import UserInlineSerializer
from .models import Post, Comment


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'id',
            'body',
            'created_at',
        ]


class CommentSerializer(serializers.ModelSerializer):
    user = UserInlineSerializer()

    class Meta:
        model = Comment
        fields = [
            'id',
            'user',
            'body',
            'created_at',
        ]


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'id',
            'description',
            'body',
            'created_at',
            'updated_at',
        ]


class PostListSerializer(serializers.ModelSerializer):
    user = UserInlineSerializer()
    comments_count = serializers.SerializerMethodField()
    detail_page_url = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            'user',
            'description',
            'created_at',
            'updated_at',
            'comments_count',
            'detail_page_url',
        ]
    
    def get_comments_count(self, obj):
        return obj.comments.count() 

    def get_detail_page_url(self, obj):
        request = self.context.get('request')
        return reverse('posts:post_detail', kwargs={'pk': obj.pk}, request=request)


class PostDetailSerializer(serializers.ModelSerializer):
    user = UserInlineSerializer()
    comments = CommentSerializer(many=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'user',
            'body',
            'created_at',
            'updated_at',
            'comments',
        ]
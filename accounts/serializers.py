from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from rest_framework.reverse import reverse

from .models import Relation


User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'password',
            'confirm_password',
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise ValidationError('Passwords do not match.')
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        return User.objects.create_user(**validated_data)


class UserListSerializer(serializers.ModelSerializer):
    profile_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'image',
            'profile_url',
        ]

    def get_profile_url(self, obj):
        request = self.context.get('request')
        return reverse('accounts:profile', kwargs={'username': obj.username}, request=request)


class UserProfileSerializer(serializers.ModelSerializer):
    posts_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    post_list_url = serializers.SerializerMethodField()
    follower_list_url = serializers.SerializerMethodField()
    following_list_url = serializers.SerializerMethodField()
    follow_url = serializers.SerializerMethodField()
    unfollow_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'website_url',
            'github_url',
            'linkedin_url',
            'bio',
            'image',   
            'posts_count',
            'followers_count',
            'following_count',
            'post_list_url',
            'follower_list_url',
            'following_list_url',
            'follow_url',
            'unfollow_url',
        ]
    
    def get_posts_count(self, obj):
        return obj.get_posts_count()
    
    def get_followers_count(self, obj):
        return obj.get_followers_count()
    
    def get_following_count(self, obj):
        return obj.get_following_count()

    def get_post_list_url(self, obj):
        request = self.context.get('request')
        return reverse('accounts:post_list', kwargs={'username': obj.username}, request=request)
    
    def get_follower_list_url(self, obj):
        request = self.context.get('request')
        return reverse('accounts:follower_list', kwargs={'username': obj.username}, request=request)
    
    def get_following_list_url(self, obj):
        request = self.context.get('request')
        return reverse('accounts:following_list', kwargs={'username': obj.username}, request=request)
    
    def get_follow_url(self, obj):
        request = self.context.get('request')
        if obj != request.user:
            if not Relation.objects.filter(from_user=request.user, to_user=obj).exists():
                return reverse('accounts:follow', kwargs={'username': obj.username}, request=request)
        return None
    
    def get_unfollow_url(self, obj):
        request = self.context.get('request')
        if obj != request.user:
            if Relation.objects.filter(from_user=request.user, to_user=obj).exists():
                return reverse('accounts:unfollow', kwargs={'username': obj.username}, request=request)
        return None


class UserInlineSerializer(serializers.ModelSerializer):
    profile_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'profile_url',
        ]

    def get_profile_url(self, obj):
        request = self.context.get('request')
        return reverse('accounts:profile', kwargs={'username': obj.username}, request=request)
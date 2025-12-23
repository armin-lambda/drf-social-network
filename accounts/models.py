from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

from utils.paths import get_user_image_upload_path
from utils.validators import (
    UsernameValidator,
    NameValidator,
    URLValidator,
)


User = settings.AUTH_USER_MODEL


class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=30,
        unique=True,
        validators=[UsernameValidator()],
        help_text='Required. 30 characters or fewer. Lowercase letters, numbers and underline.',
        error_messages={
            'unique': 'This username already exists.',
        },
    )
    email = models.EmailField(
        unique=True,
        verbose_name='email address',
        help_text='Required. Must be a valid and unique email address.',
        error_messages={
            'unique': 'This email address already exists.',
        },
    )
    first_name = models.CharField(
        max_length=30,
        help_text='Required. 30 characters or fewer. Letters only.',
        validators=[NameValidator('First Name')],
    )
    last_name = models.CharField(
        max_length=30,
        help_text='Required. 30 characters or fewer. Letters only.',
        validators=[NameValidator('Last Name')],
    )

    phone_number = models.CharField(
        max_length=15,
        unique=True,
        help_text='Required. 15 characters or fewer.',
        error_messages={
            'unique': 'This phone number already exists.',
        },
    )
    website_url = models.URLField(
        max_length=100,
        blank=True,
        null=True,
        help_text='100 characters or fewer. Must start with https://',
        validators=[URLValidator()],
    )
    github_url = models.URLField(
        max_length=100,
        blank=True,
        null=True,
        help_text='100 characters or fewer. Must start with https://github.com/',
        validators=[URLValidator('github')],
    )
    linkedin_url = models.URLField(
        max_length=100,
        blank=True,
        null=True,
        help_text='100 characters or fewer. Must start with https://linkedin.com/',
        validators=[URLValidator('linkedin')],
    )
    bio = models.TextField(
        max_length=500,
        blank=True,
        null=True,
        help_text='500 characters or fewer.',
    )
    image = models.ImageField(
        blank=True,
        null=True,
        upload_to=get_user_image_upload_path,
        help_text='Only png/jpg/jpeg types are allowed.',
        validators=[
            FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg']),
        ],
    )

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'phone_number']

    class Meta:
        ordering = ['username']
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def get_followers(self):
        return CustomUser.objects.filter(following__to_user=self)
    
    def get_following(self):
        return CustomUser.objects.filter(followers__from_user=self)

    def get_followers_count(self):
        return self.followers.count()
    
    def get_following_count(self):
        return self.following.count()
    
    def get_posts(self):
        return self.posts.all()
    
    def get_posts_count(self):
        return self.posts.count()


class Relation(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['from_user', 'to_user']
    
    def __str__(self):
        return f"{self.from_user} followed {self.to_user}"
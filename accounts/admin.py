from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm


User = get_user_model()


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    list_display = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'is_staff']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'groups']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'bio']

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            'Personal Info', {
                'fields': (
                    'phone_number',
                    'website_url',
                    'github_url',
                    'linkedin_url',
                    'bio',
                    'image',
                ),
            },
        ),
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            'Personal Info', {
                'fields': (
                    'phone_number',
                    'website_url',
                    'github_url',
                    'linkedin_url',
                    'bio',
                    'image',
                ),
            },
        ),
    )
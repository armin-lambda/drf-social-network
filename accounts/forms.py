from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AdminUserCreationForm, UserChangeForm


User = get_user_model()


class CustomUserCreationForm(AdminUserCreationForm):
    class Meta:
        model = User
        fields = AdminUserCreationForm.Meta.fields + (
            'phone_number',
            'website_url',
            'github_url',
            'linkedin_url',
            'bio',
            'image',
        )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = UserChangeForm.Meta.fields


from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


INVALID_NAMES = [
    'signup', 'signin', 'signout', 'password', 'confirm_password', 'auth', 'accounts',
    'register', 'login', 'logout', 'users',
    'delete', 'edit', 'change', 'remove', 'follow', 'unfollow', 'restore', 'confirm', 'verify',
]


def apply_regex(value, regex, message=None):
    RegexValidator(
        regex=regex,
        message=message or f"{value} is invalid.",
    )(value)

def apply_basics(value, field_name):
    if value.isdigit():
        raise ValidationError(f"{field_name} cannot be only numbers.")
    if all(char in '._' for char in value):
        raise ValidationError(f"{field_name} cannot consist only of dots and underlines.")

def apply_word_list(value, field_name, word_list):
    for word in word_list:
        if word in value:
            raise ValidationError(f"{value} is not allowed as a {field_name}.")


@deconstructible
class UsernameValidator:
    def __init__(self, invalid_names=None):
        self.invalid_names = invalid_names or INVALID_NAMES
    
    def __call__(self, value):
        apply_regex(
            value=value,
            regex=r'^[a-z0-9_]+$',
            message='Username must contain only lowercase letters, numbers and underline.',
        )
        apply_basics(value, 'Username')
        apply_word_list(value, 'Username', INVALID_NAMES)


@deconstructible
class NameValidator:
    def __init__(self, field_name=None, invalid_names=None):
        self.field_name = field_name or 'Name'
        self.invalid_names = invalid_names or INVALID_NAMES

    def __call__(self, value):
        apply_regex(
            value=value,
            regex=r'^[a-zA-Z]+$',
            message=f"{self.field_name} must contain only letters.",
        )
        apply_basics(value, self.field_name)
        apply_word_list(value, self.field_name, INVALID_NAMES)


@deconstructible
class URLValidator:
    def __init__(self, website_name=None):
        self.website_name = website_name

    def __call__(self, value):
        if not value.startswith('https://'):
            raise ValidationError('URL must start with https://')
        if self.website_name:
           if self.website_name == 'github' and not value.startswith('https://github.com/'):
              raise ValidationError('GitHub URL must start with https://github.com/')
           if self.website_name == 'linkedin' and not value.startswith('https://linkedin.com/'):
               raise ValidationError('LinkedIn URL must start with https://linkedin.com/')
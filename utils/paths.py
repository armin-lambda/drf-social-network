import os

from django.conf import settings
from django.utils.text import slugify


def get_user_image_upload_path(instance, filename):
    username = slugify(instance.username)
    file_name = f"{username}{os.path.splitext(filename)[1]}"
    file_path = f"accounts/{username}/{file_name}"
    full_path = os.path.join(settings.MEDIA_ROOT, file_path)

    if os.path.isfile(full_path):
        os.remove(full_path)
    return file_path
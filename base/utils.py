from django.conf import settings
from django.urls import reverse


def get_password_reset_link(key):
    return settings.HOST + reverse('auth:reset_password', args=(key,))

from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _


class Customer(AbstractUser):

    username = models.CharField(_('username'), max_length=150, unique=True)
    email = models.EmailField(_('email address'), blank=False, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    password = models.CharField(max_length=6)


class CustomerGroup(Group):

    group_name = models.CharField(max_length=128)
    members = models.ManyToManyField(Customer)

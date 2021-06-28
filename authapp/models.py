from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    CUSTOMER = 1
    ADMIN = 2

    ROLES = (
        (CUSTOMER, 'customer'),
        (ADMIN, 'admin'),
    )

    role = models.PositiveSmallIntegerField(choices=ROLES)

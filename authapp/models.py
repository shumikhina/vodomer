import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class Customer(AbstractUser):
    pass


class CustomerGroup(Group):

    group_name = models.CharField(max_length=128)
    members = models.ManyToManyField(Customer)


class CustomerResetPasswordAttempt(models.Model):

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    key = models.UUIDField()
    created_at = models.DateTimeField(auto_now=True)

    @classmethod
    def create(cls, customer: Customer):
        return cls.objects.create(
            customer=customer,
            key=uuid.uuid4()
        )


from django.db import transaction, IntegrityError
from rest_framework.exceptions import ValidationError

from core.models import Client
from authapp.models import Customer, CustomerResetPasswordAttempt, CustomerGroup


class CreateInactiveCustomerService:

    INVALID_PASSWORD_PLACEHOLDER = 'invalid_password'

    def __init__(self, username: str):
        self.username = username

    @staticmethod
    def _create_client_for_customer(customer: Customer, group: CustomerGroup) -> Client:
        return Client.objects.create(customer=customer, group=group)

    @staticmethod
    def _create_reset_password_attempt(customer: Customer) -> CustomerResetPasswordAttempt:
        return CustomerResetPasswordAttempt.create(customer)

    def get_reset_password_attempt(self):
        return CustomerResetPasswordAttempt.objects.filter(
            customer__username=self.username
        ).first()

    @transaction.atomic()
    def create(self, group, **kwargs) -> Customer:
        customer_kwargs = {
            'username': self.username,
            'password': self.INVALID_PASSWORD_PLACEHOLDER,
            'is_active': False
        }
        customer_kwargs.update(kwargs)
        try:
            customer = Customer.objects.create(**customer_kwargs)
        except IntegrityError:
            raise ValidationError('Username already exists')
        self._create_client_for_customer(customer, group)
        self._create_reset_password_attempt(customer)
        return customer

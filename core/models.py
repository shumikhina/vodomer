import uuid

from django.db import models

from authapp.models import Customer, CustomerGroup


class Client(models.Model):

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    token = models.CharField(max_length=36, default=uuid.uuid4)
    group = models.ForeignKey(CustomerGroup, on_delete=models.PROTECT)


class ProviderTypeChoices(models.TextChoices):

    HOT_WATER = 'HW', 'Hot water'
    COLD_WATER = 'CW', 'Cold water'
    WARMING_WATER = 'WW', 'Warming water'
    ELECTRICITY = 'EL', 'Electricity'
    GAS = 'GS', 'Gas'


class Provider(models.Model):

    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    provider_type = models.CharField(
        max_length=2,
        choices=ProviderTypeChoices.choices,
        default=ProviderTypeChoices.COLD_WATER)


class ProviderValue(models.Model):

    provider = models.ForeignKey(Provider, on_delete=models.PROTECT)
    value = models.FloatField()
    created_at = models.DateTimeField()
    received_at = models.DateTimeField(auto_now_add=True)

from django.db import models


class Client(models.Model):

    client_id = models.IntegerField()


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
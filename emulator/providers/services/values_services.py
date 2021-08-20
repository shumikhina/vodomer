import abc
import json
import random

import requests
from django.utils import timezone

from providers.models import Provider, ProviderValue


class UpdateValuesService:

    def __init__(self, factor=None):
        self._factor = factor or random.randint(1, 50)

    def build_new_value(self, provider: Provider):
        last_provider_value = ProviderValue.objects.filter(provider=provider).order_by('-sent_at').first()
        if last_provider_value is not None:
            value = last_provider_value.value + self._factor
        else:
            value = random.randint(1, 1000)
        ProviderValue.objects.create(
            provider=provider,
            value=value
        )


class BaseSendValuesService:

    @abc.abstractmethod
    def _serialize_object(self, value: ProviderValue):
        pass

    @abc.abstractmethod
    def _send_data(self, data: dict):
        pass

    def send_value(self, value: ProviderValue):
        data = self._serialize_object(value)
        self._send_data(data)
        value.sent_at = timezone.now()
        value.save()


class HttpSendValuesService(BaseSendValuesService):

    def __init__(self, host):
        self._host = host

    def _serialize_object(self, value: ProviderValue):
        return {
            'client_id': value.provider.client.id,
            'provider_type': value.provider.provider_type,
            'value': value.value,
            'created_at': str(value.created_at),
        }

    def _send_data(self, data: dict):
        requests.post(self._host, json=data, headers={'Content-Type': 'application/json'})

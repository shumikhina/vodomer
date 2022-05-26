from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core import models
from core.models import Client


class ProviderDataSerializer(serializers.Serializer):

    token = serializers.CharField()
    provider_type = serializers.CharField(write_only=True)
    value = serializers.FloatField(write_only=True)
    created_at = serializers.DateTimeField(write_only=True)

    @staticmethod
    def _raise_invalid_token_error():
        raise ValidationError('Invalid token')

    def validate(self, attrs):
        token = attrs.get('token')
        if token is None:
            self._raise_invalid_token_error()
        attrs['client'] = Client.objects.filter(token=token).first()
        if attrs['client'] is None:
            self._raise_invalid_token_error()
        return attrs

    def create(self, validated_data):
        provider, _ = models.Provider.objects.get_or_create(
            client=validated_data['client'],
            provider_type=validated_data['provider_type']
        )
        return models.ProviderValue.objects.create(
            provider=provider,
            value=validated_data['value'],
            created_at=validated_data['created_at']
        )


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = ('pk', 'token')

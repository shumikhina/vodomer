from rest_framework import serializers

from core import models


class ProviderDataSerializer(serializers.Serializer):

    client_id = serializers.IntegerField(write_only=True)
    provider_type = serializers.CharField(write_only=True)
    value = serializers.FloatField(write_only=True)
    created_at = serializers.DateTimeField(write_only=True)

    def create(self, validated_data):
        client, _ = models.Client.objects.get_or_create(client_id=validated_data['client_id'])
        provider, _ = models.Provider.objects.get_or_create(
            client=client,
            provider_type=validated_data['provider_type']
        )
        return models.ProviderValue.objects.create(
            provider=provider,
            value=validated_data['value'],
            created_at=validated_data['created_at']
        )

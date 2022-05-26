from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from authapp.models import CustomerResetPasswordAttempt, CustomerGroup
from authapp.services.create_customer import CreateInactiveCustomerService
from base.utils import get_password_reset_link


class CreateCustomerSerializer(serializers.Serializer):

    username = serializers.CharField(write_only=True)
    group = serializers.PrimaryKeyRelatedField(queryset=CustomerGroup.objects.all())
    reset_link = serializers.CharField(read_only=True)

    def create(self, validated_data):
        service = CreateInactiveCustomerService(validated_data['username'])
        service.create(validated_data['group'])
        attempt = service.get_reset_password_attempt()
        validated_data['reset_link'] = get_password_reset_link(attempt.key)
        return validated_data


class ResetPasswordSerializer(serializers.Serializer):

    password = serializers.CharField(write_only=True)

    @staticmethod
    def _get_attempt(key):
        return CustomerResetPasswordAttempt.objects.filter(key=key).first()

    def validate(self, attrs):
        key = self.context['view'].kwargs.get('key')
        attempt = self._get_attempt(key)
        if attempt is None:
            raise ValidationError('Invalid key')
        attrs['attempt'] = attempt
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        attempt = validated_data['attempt']
        user = attempt.customer
        user.set_password(validated_data['password'])
        user.is_active = True
        user.save()
        attempt.delete()
        return validated_data

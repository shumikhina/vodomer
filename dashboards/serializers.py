from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from authapp.models import CustomerGroup
from core.models import Client, ProviderTypeChoices
from dashboards.services.aggregators import DateGroupDimensionEnum, ChartTypeEnum, LinearDashboardQueryAggregator
from dashboards.services.factories import LinearDashboardFilterFactory
from dashboards.services.linear_dashboard import LinearDashboard


class DashboardInputSerializer(serializers.Serializer):

    date = serializers.DateField(required=False, allow_null=True)
    date_to = serializers.DateField(required=False, allow_null=True)
    date_from = serializers.DateField(required=False, allow_null=True)
    client = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all(), required=False, allow_null=True)
    groups = serializers.ListSerializer(
        child=serializers.PrimaryKeyRelatedField(queryset=CustomerGroup.objects.all()),
        required=False,
        allow_null=True
    )
    provider_type = serializers.CharField()
    date_dimension = serializers.CharField()
    chart_type = serializers.CharField()

    @staticmethod
    def _validate_provider_type(attrs):
        if attrs['provider_type'] not in ProviderTypeChoices.values:
            raise ValidationError('You have to pass a valid provider type')

    def _validate_groups(self, attrs):
        if (groups := attrs.get('groups', None)) is None:
            return
        if not self.context['request'].user.is_staff:
            raise ValidationError('Only staff has access to groups data')
        if not all([c_group in groups for c_group in self.context['request'].user.customergroup_set.all()]):
            raise ValidationError('You may have access only to assigned groups')

    def _validate_client(self, attrs):
        if (client := attrs.get('client', None)) is None:
            return
        user = self.context['request'].user
        self_client = client in user.client_set.all()
        staff_client = client.group in user.customergroup_set.all() and user.is_staff
        if not (self_client or staff_client):
            raise ValidationError('You have no access to this client')

    def _validate_date_dimension(self, attrs):
        if attrs['date_dimension'] not in DateGroupDimensionEnum.values():
            raise ValidationError('You have to pass a valid date dimension')

    def _validate_chart_type(self, attrs):
        if attrs['chart_type'] not in ChartTypeEnum.values():
            raise ValidationError('You have to pass a valid chart type')

    def validate(self, attrs):
        self._validate_provider_type(attrs)
        self._validate_groups(attrs)
        self._validate_client(attrs)
        self._validate_date_dimension(attrs)
        self._validate_chart_type(attrs)
        return attrs

    def create(self, validated_data):
        filters_factory = LinearDashboardFilterFactory(
            date=validated_data.get('date', None),
            date_to=validated_data.get('date_to', None),
            date_from=validated_data.get('date_from', None),
            client=validated_data.get('client', None),
            groups=validated_data.get('groups', None),
            provider_type=validated_data.get('provider_type', None)
        )
        filters_factory.validate_kwargs()
        aggregator = LinearDashboardQueryAggregator(validated_data['date_dimension'], validated_data['chart_type'])
        return LinearDashboard().get_chart(filters_factory.get_filters(), aggregator)


class DashboardOutputSerializer(serializers.Serializer):

    total_value = serializers.FloatField()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        date = instance.get(DateGroupDimensionEnum.HOUR.value) \
               or instance.get(DateGroupDimensionEnum.DAY.value) \
               or instance.get(DateGroupDimensionEnum.MONTH.value)
        data['date'] = date
        return data


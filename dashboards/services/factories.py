from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.models import ProviderTypeChoices
from dashboards.services.aggregators import LinearDashboardQueryAggregator
from dashboards.services.filters.date_filter import OneDayQueryFilter, RangeDateFilter
from dashboards.services.filters.provider_filter import ClientQueryFilter, GroupQueryFilter, ProviderTypeQueryFilter


class BaseFactory:

    def __init__(
            self,
            date=None,
            date_to=None,
            date_from=None,
            client=None,
            groups=None,
            provider_type=None
    ):
        self.date = date
        self.date_to = date_to
        self.date_from = date_from
        self.client = client
        self.groups = groups
        self.provider_type = provider_type
        self.is_validated = False

    def validate_kwargs(self):
        self._cal_validation_methods()
        self.is_validated = True

    def _cal_validation_methods(self):
        self._validate_dates()
        self._validate_providers()
        self._validate_provider_type()

    def _raise_validation_error(self):
        raise ValidationError('Invalid kwargs configuration')

    def _validate_dates(self):
        if self.date is None and (self.date_to is None or self.date_from is None):
            self._raise_validation_error()

    def _validate_providers(self):
        if self.client is None and not self.groups:
            self._raise_validation_error()

    def _validate_provider_type(self):
        if self.provider_type is None or self.provider_type.upper() not in [i for i, _ in ProviderTypeChoices.choices]:
            self._raise_validation_error()



class LinearDashboardFilterFactory(BaseFactory):

    def get_filters(self):
        assert self.is_validated, "You have to call .validate_kwargs() method before getting filters"
        filters = [ProviderTypeQueryFilter(self.provider_type)]
        if self.date:
            filters.append(OneDayQueryFilter(self.date))
        else:
            filters.append(RangeDateFilter(self.date_from, self.date_to))
        if self.client:
            filters.append(ClientQueryFilter(self.client))
        else:
            filters.append(GroupQueryFilter(self.groups))
        return filters

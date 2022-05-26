from core.models import ProviderValue


class LinearDashboard:

    value_model = ProviderValue

    def _get_values_queryset(self):
        return self.value_model.objects.all()

    def get_chart(self, filters, aggregator):
        query = self._get_values_queryset()
        for filter_service in filters:
            query = filter_service.get_filtered_query(query)
        return aggregator.get_aggregated_data(query)

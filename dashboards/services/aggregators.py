from enum import Enum

from django.db.models import Max, Sum, Subquery, OuterRef, Q, Count
from django.db.models.functions import TruncHour, TruncDay, TruncMonth


class DateGroupDimensionEnum(Enum):

    HOUR = 'hour'
    DAY = 'day'
    MONTH = 'month'


class ChartTypeEnum(Enum):

    DELTA = 'delta'
    ABSOLUTE = 'absolute'


class LinearDashboardQueryAggregator:

    def __init__(self, date_group_dimension: DateGroupDimensionEnum, chart_type: ChartTypeEnum):
        self.date_group_dimension = date_group_dimension
        self.chart_type = chart_type

    def get_aggregated_data(self, query):
        query = query.annotate(
            hour=TruncHour('created_at'),
            day=TruncDay('created_at'),
            month=TruncMonth('created_at'),
        )
        annotate_query = query.annotate(
            max_value=Subquery(
                query.values(
                    'provider_id', self.date_group_dimension
                ).annotate(
                    max_value=Max('value') / Count('value')
                ).values(
                    'max_value'
                ).filter(
                    **{'provider_id': OuterRef('provider_id'), self.date_group_dimension: OuterRef(self.date_group_dimension)}
                )[:1]
            )
        ).values(
            self.date_group_dimension
        ).annotate(
            total_value=Sum('max_value')
        )
        if self.chart_type == ChartTypeEnum.ABSOLUTE.value:
            return annotate_query
        else:
            return self._get_delta_values_for_chart(annotate_query)

    def _get_delta_values_for_chart(self, query):
        if not query:
            return query
        values = [
            {
                "total_value": 0,
                self.date_group_dimension: query[0][self.date_group_dimension]
            }
        ]
        for index, item in enumerate(query[1:]):
            values.append(
                {
                    "total_value": item['total_value'] - query[index]['total_value'],
                    self.date_group_dimension: item[self.date_group_dimension]
                }
            )
        return values

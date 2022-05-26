from dashboards.services.filters.base_filter import BaseQueryFilter


class OneDayQueryFilter(BaseQueryFilter):

    def __init__(self, date):
        self.date = date

    def get_filtered_query(self, query):
        return query.filter(created_at=self.date)


class RangeDateFilter(BaseQueryFilter):

    def __init__(self, date_from, date_to):
        self.date_from = date_from
        self.date_to = date_to

    def get_filtered_query(self, query):
        return query.filter(
            created_at__gt=self.date_from,
            created_at__lte=self.date_to
        )

from dashboards.services.filters.base_filter import BaseQueryFilter


class ClientQueryFilter(BaseQueryFilter):

    def __init__(self, client):
        self.client = client

    def get_filtered_query(self, query):
        return query.filter(provider__client=self.client)


class GroupQueryFilter(BaseQueryFilter):

    def __init__(self, groups):
        self.groups = groups

    def get_filtered_query(self, query):
        return query.filter(provider__client__group__in=self.groups)


class ProviderTypeQueryFilter(BaseQueryFilter):

    def __init__(self, subtype):
        self.subtype = subtype

    def get_filtered_query(self, query):
        return query.filter(provider__provider_type=self.subtype)

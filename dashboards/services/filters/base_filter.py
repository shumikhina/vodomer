import abc


class BaseQueryFilter:

    @abc.abstractmethod
    def get_filtered_query(self, query):
        pass

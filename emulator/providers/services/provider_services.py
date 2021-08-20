from providers.models import Provider, Client


class ProviderService:

    @staticmethod
    def create_provider(client_description='Client description'):
        return Provider.objects.create(
            client=Client.objects.create(description=client_description)
        )

from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from core.models import Client
from core.permissions import AllowedByGroup
from core.serializers import ProviderDataSerializer, ClientSerializer


class ReceiveDataFromProvidersView(CreateAPIView):

    permission_classes = (AllowAny, )
    serializer_class = ProviderDataSerializer


class GetTokenForClientAPIView(RetrieveAPIView):

    permission_classes = (IsAuthenticated, AllowedByGroup)
    serializer_class = ClientSerializer
    queryset = Client.objects.all()

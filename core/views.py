from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from core.serializers import ProviderDataSerializer


class ReceiveDataFromProvidersView(CreateAPIView):

    permission_classes = (AllowAny, )
    serializer_class = ProviderDataSerializer

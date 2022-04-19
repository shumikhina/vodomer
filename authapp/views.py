from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from authapp.serializers import CreateCustomerSerializer, ResetPasswordSerializer
from base.permissions import IsStaff


class CreateCustomerAPIView(CreateAPIView):

    permission_classes = (IsAuthenticated, IsStaff,)
    serializer_class = CreateCustomerSerializer


class ResetPassword(CreateAPIView):

    permission_classes = (AllowAny,)
    serializer_class = ResetPasswordSerializer

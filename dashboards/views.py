from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from dashboards.serializers import DashboardInputSerializer, DashboardOutputSerializer


class DashboardAPIView(CreateAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = DashboardInputSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instances = serializer.save()
        output_serializer = DashboardOutputSerializer(instances, many=True)
        headers = self.get_success_headers(output_serializer.data)
        return Response(output_serializer.data, status=status.HTTP_200_OK, headers=headers)


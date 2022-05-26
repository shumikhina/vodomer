from django.urls import path

from dashboards.views import DashboardAPIView

urlpatterns = [
    path('', DashboardAPIView.as_view()),
]

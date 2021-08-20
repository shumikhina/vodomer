from django.urls import path

from core import views

urlpatterns = [
    path('recieve/', views.ReceiveDataFromProvidersView.as_view()),
]

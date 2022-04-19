from django.urls import path
from rest_framework.authtoken import views as rest_views

from authapp.views import CreateCustomerAPIView, ResetPassword

app_name = 'auth'

urlpatterns = [
    path('log_in/', rest_views.obtain_auth_token),
    path('create_customer/', CreateCustomerAPIView.as_view(), name='create_customer'),
    path('reset_password/<uuid:key>/', ResetPassword.as_view(), name='reset_password'),
]

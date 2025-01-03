from django.urls import path
from . import views

urlpatterns = [
    path('', views.Organization_settings.as_view(), name='organization_settings'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.organization_settings, name='organization_settings'),
]
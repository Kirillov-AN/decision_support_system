from django.urls import path
from . import views

urlpatterns = [

     path('', views.Model_execution.as_view(), name='model_execution')
]
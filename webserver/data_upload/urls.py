from django.urls import path
from . import views

urlpatterns = [

     path('', views.Upload_data.as_view(), name='upload_data')
]
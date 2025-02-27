"""
URL configuration for webserver project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Main.as_view(), name='main'),  # Главная страница
    path('data-upload/', include('data_upload.urls')),  # Ссылка на urls.py в data_upload
    path('organization-settings/', include('organization_settings.urls')),  # Ссылка на urls.py в organization_settings
    path('model-execution/', include('model_execution.urls')),  # Ссылка на urls.py в organization_settings

 #   path('model-execution/', include('model_execution.urls')),  # Ссылка на urls.py в model_execution

    
]

# webserver/views.py (или в любом другом приложении)
from django.shortcuts import render
from . import views


def main(request):
    return render(request, 'main.html')  # Главная страница
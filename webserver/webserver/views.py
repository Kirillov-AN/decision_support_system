# webserver/views.py (или в любом другом приложении)
from django.views.generic import TemplateView



class Main(TemplateView):
    template_name = "main.html"

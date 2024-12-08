from django.shortcuts import render
from .models import Parameter


def organization_settings(request):
    parameters = Parameter.objects.all()

    if request.method == "POST":

        for param in parameters:
            value  = int(request.POST.get(f'param_{param.id}'))
            param.value = value
            param.save()
    return render(request, 'organization_settings.html', {'parameters': parameters} )



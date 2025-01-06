from django.shortcuts import render
from .models import Parameter


from django.views.generic import TemplateView
from django.shortcuts import redirect
from .models import Parameter , Model, Limit
from .models import Model
class Organization_settings(TemplateView):
    template_name = 'organization_settings.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Передаём все параметры в контекст
        context['parameters'] = Parameter.objects.all()
        context['models'] = Model.objects.all()
        context['limits'] = Limit.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        parameters = Parameter.objects.all()
        for param in parameters:
            # Получаем значение параметра из POST-запроса
            param_weight = request.POST.get(f'param_{param.id}')
            if param_weight:  # Проверяем, есть ли значение
                try:
                    param.weight = int(param_weight)
                    param.save()
                except ValueError:
                    pass  # Игнорируем ошибки преобразования
        limits = Limit.objects.all()
        for limit in limits:
            limit_size = request.POST.get(f'limit_{limit.id}')
            if limit_size:
                try:
                    limit.value = int(limit_size)
                    limit.save()
                except ValueError:
                    pass  # Игнорируем ошибки преобразования


        return redirect('organization_settings')  

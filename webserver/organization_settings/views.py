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
        context['models'] = Model.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        models = Model.objects.all()
        for model in models:
            print(self.model.parameters.get("base"))
            params = model.parameters
            for section in params:
                param_list = model.parameters[section]
                for i in param_list:
            # Получаем значение параметра из POST-запроса
                  param_weight = request.POST.get(f'param_{i["id"]}')
                  if param_weight:  # Проверяем, есть ли значение
                    try:
                        i["weight"] = int(param_weight)
                        model.save()
                    except ValueError:
                        pass  # Игнорируем ошибки преобразования
            limits = model.limits
            for limit in limits:
                   limit_size = request.POST.get(f'limit_{limit["id"]}')
                   if limit_size:
                    try:
                        limit["value"] = int(limit_size)
                        model.save()
                    except ValueError:
                        pass  # Игнорируем ошибки преобразования


        return redirect('organization_settings')  

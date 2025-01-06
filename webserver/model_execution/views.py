from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import TemplateView
import json
import pandas as pd
import numpy as np
import os

from organization_settings.models import Model, Parameter, Variant, Parameter_Variant
from .optimization_utils import optimal_alternative


class Model_execution(TemplateView):
    template_name = 'model_execution.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Передаём все параметры в контекст
        models = Model.objects.all()
        parameters = { model: Parameter.objects.filter(model=model)  for model in models }
        context['models'] = models
        context['[parameters]'] = parameters
        context['modelParamsJson'] = json.dumps({  model.id: [param.name for param in Parameter.objects.filter(model=model)]  for model in models })
        return context




    def post(self, request):


           model_id = request.POST.get('model_id')
           selected_model = get_object_or_404(Model, id=model_id)
       
           # Получаем параметры, относящиеся к выбранной модели
           variants = Variant.objects.filter(model=selected_model)
           vectors = [
            [
                param_variant.int_value if param_variant.int_value is not None else
                param_variant.str_value if param_variant.str_value is not None else
                param_variant.bool_value
                for param_variant in Parameter_Variant.objects.filter(variant=v).order_by('parameter__id')
            ]
            for v in variants
           ]
           # Получаем все Parameter_Variant, относящиеся к этим параметрам
           print(vectors)


           return HttpResponse(status=200)


       
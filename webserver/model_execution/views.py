from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import TemplateView
import json
import pandas as pd
import numpy as np
import os
import numpy as np
from pulp import LpMaximize, LpProblem, LpVariable, lpSum

from . import opt_cups
from organization_settings.models import Model, Parameter, Variant, Parameter_Variant
from .optimization_utils import optimal_alternative


class Model_execution(TemplateView):

    dict_models_id = {}
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
           vectors = convert_json_to_model_structure(model_id)
           weight = get_list_of_weights(model_id)
           limits_data = get_dict_of_limits(model_id)
           if model_id == "1":
               print(limits_data)
               model = opt_cups.CupOptimization(cups_data=vectors,weight_factors=weight,limits=limits_data)
               result = model.run_optimization()
               print(result)
           elif model_id == 2:
                pass
           return HttpResponse(status=200)
def convert_json_to_model_structure(model_id):
    variants = Variant.objects.filter(model=model_id)
    vectors = []
    for v in variants:
        supplier_name = v.name  
        row = [
            supplier_name,
            v.vector["Цена за один стаканчик"],
            v.vector["Размер партии стаканчиков"],
            v.vector["Наличие логотипа бренда"],
            v.vector["Удобство пользования"],
            v.vector["Затраты на логистику"],
            v.vector["Репутация поставщика"],
            v.vector["Срок доставки"]
        ]
        vectors.append(row)
    return vectors
        
def get_list_of_weights(model_id):
    params_dict = get_object_or_404(Model, id=model_id).parameters
    
    base_weights = [item["weight"] for item in params_dict["base"]]
    advanced_weights = [item["weight"] for item in params_dict["advanced"]]

    list_of_weights = base_weights + advanced_weights
    return list_of_weights

def get_dict_of_limits(model_id):
    limits = get_object_or_404(Model, id=model_id).limits
    dict_of_limits = {}
    for i in limits:
       dict_of_limits[i["id"]] = i["value"]
    return dict_of_limits



       
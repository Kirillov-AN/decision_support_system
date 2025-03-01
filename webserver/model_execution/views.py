from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import TemplateView
import json
import pandas as pd
import os
from pulp import LpMaximize, LpProblem, LpVariable, lpSum
from .infra_adapters.infra_adapters import CupsDataSQLRepository
from .use_cases.use_cases import CupOptimizationPreparation , CupOptimizationTOPSIS

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

           self.model_controller(model_id)
           return HttpResponse(status=200)

    def model_controller(self, model_id):
        print(model_id)
        repository = CupsDataSQLRepository(model_id)
        if model_id == "1":
            
        
            use_case = CupOptimizationPreparation(repository)
            processed_data = use_case.processed_data
            normalized_indices,indices_array,rank = use_case.calculate_indices(processed_data)
            print(normalized_indices)
            ratings_list = use_case.calculate_ratings(normalized_indices)
            weights = use_case.weights
            print(normalized_indices)
            print(rank,len(indices_array))
            print(rank / len(indices_array))
    
            if rank / len(indices_array) <= 0.3:
                print("Применяется MILP оптимизация")
                milp = CupOptimizationMILP()
                selected_index, optimal_rating = milp.milp_optimization(normalized_indices, ratings_list)
            
                if selected_index is not None:
                    print(f"Выбрана альтернатива: {processed_data[selected_index]}")
                    print(f"Оптимальный рейтинг: {optimal_rating}")
                else:
                    print("Оптимальное решение не найдено")
            else: 
                print("Применяется TOPSIS методика анализа")
                topsis = CupOptimizationTOPSIS()
            
                ideal_combination = topsis.get_best_combination(processed_data)
                ideal_indices, _ , _ = use_case.calculate_indices([ideal_combination])
                ideal_indices = ideal_indices[0]
                ideal_rating = use_case.calculate_ratings([ideal_indices])[0]
            
                sorted_results = sorted(zip(ratings_list, processed_data), key=lambda pair: abs(pair[0] - ideal_rating))
            
                print("Матрица индексов:")
                for idx in normalized_indices:
                    print(idx)
            
                print("\nИдеальный вариант (по индексам):")
                print(ideal_indices)
                print(f"Рейтинг идеального варианта: {ideal_rating}")

                print("\nИсходные данные, отсортированные по разнице с идеальным рейтингом:")
                for rating, entry in sorted_results:
                    print(f"Рейтинг: {rating}, Данные: {entry}")




# def convert_json_to_model_structure(model_id):
#     variants = Variant.objects.filter(model=model_id)
#     vectors = []
#     for v in variants:
#         supplier_name = v.name  
#         row = [
#             supplier_name,
#             v.vector["Цена за один стаканчик"],
#             v.vector["Размер партии стаканчиков"],
#             v.vector["Наличие логотипа бренда"],
#             v.vector["Удобство пользования"],
#             v.vector["Затраты на логистику"],
#             v.vector["Репутация поставщика"],
#             v.vector["Срок доставки"]
#         ]
#         vectors.append(row)
#     return vectors
        
# def get_list_of_weights(model_id):
#     params_dict = get_object_or_404(Model, id=model_id).parameters
    
#     base_weights = [item["weight"] for item in params_dict["base"]]
#     advanced_weights = [item["weight"] for item in params_dict["advanced"]]

#     list_of_weights = base_weights + advanced_weights
#     return list_of_weights

# def get_dict_of_limits(model_id):
#     limits = get_object_or_404(Model, id=model_id).limits
#     dict_of_limits = {}
#     for i in limits:
#        dict_of_limits[i["id"]] = i["value"]
#     return dict_of_limits



       
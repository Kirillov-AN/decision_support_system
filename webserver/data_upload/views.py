from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.views.generic import TemplateView
import json
import pandas as pd
import numpy as np
import os

from organization_settings.models import Model, Parameter , Variant, Parameter_Variant

class Upload_data(TemplateView):
    template_name = 'data_upload.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Передаём все параметры в контекст
        models = Model.objects.all()
        parameters = { model: Parameter.objects.filter(model=model)  for model in models }
        context['models'] = models
        context['[parameters]'] = parameters
        context['modelParamsJson'] = json.dumps({  model.id: [param.name for param in Parameter.objects.filter(model=model)]  for model in models })
        return context


    def check_cell_type(self,value):
        if isinstance(value, bool):
            return "bool"
        elif isinstance(value, float):
            return "float"
        elif isinstance(value, str):
            return "str"
        else:
            return "Unknown"

    def post(self, request):
        model_id = request.POST.get('model_id')
        selected_model = get_object_or_404(Model, id=model_id)
        uploaded_file = request.FILES.get('file')
        parameters = Parameter.objects.filter(model=selected_model)
        if not uploaded_file:
            return HttpResponse("No file uploaded", status=400)
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith(('.xls','.xlsx')):
                df = pd.read_excel(uploaded_file)
            else:
                return HttpResponse("Unsupported file format", status=400)
            #print(df.head())
            for index, row in df.iterrows():
                for column_name in df.columns:
                    print(column_name)
                    if column_name == "Название варианта":
                        variant_name = row["Название варианта"]
                        variant = Variant.objects.create(name=variant_name,model=selected_model)
                    else:
                        value = row[column_name]
                        filtered_parameter = Parameter.objects.get(  # Учитываем только связанные параметры
                        name=column_name  # Фильтруем по имени варианта
                        )
                        parameter_type = filtered_parameter.type
                        int_value = None
                        str_value = None
                        bool_value = None
                        if parameter_type == 1:
                            int_value = value
                        elif parameter_type == 2:
                            str_value = value
                        else: 
                            bool_value = value


                        parameter_variant_value = Parameter_Variant.objects.create(variant=variant,parameter=filtered_parameter,int_value=int_value,str_value=str_value,bool_value=bool_value)
                    #type = check_cell_type()
                    #Parameter_Variant.objects.create()



            return HttpResponse("File processed successfully!")
        except Exception as e:
            print(f"Error processing file: {e}")
            return HttpResponse(f"Error processing file: {str(e)}", status=500)



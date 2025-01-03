from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
import json
import pandas as pd
import numpy as np
import os

from organization_settings.models import Model, Parameter

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
                
                print(index)
                print(row)
            parameter_names = df.columns.tolist()
            return HttpResponse("File processed successfully!")
        except Exception as e:
            print(f"Error processing file: {e}")
            return HttpResponse(f"Error processing file: {str(e)}", status=500)



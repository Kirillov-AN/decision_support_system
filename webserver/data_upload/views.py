from django.shortcuts import render
from django.http import HttpResponse
  
 
def upload_data(request):
    return render(request, "data_upload.html")
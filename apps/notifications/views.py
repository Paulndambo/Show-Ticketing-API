from django.shortcuts import render

# Create your views here.
# myapp/views.py
from django.http import JsonResponse



def add_view(request):
    
    return JsonResponse({"task_id": 2, "status": "Success"})

from django.shortcuts import render

# Create your views here.
# myapp/views.py
from django.http import JsonResponse
from apps.notifications.tasks import add

def add_view(request):
    result = add.delay(4, 4)
    return JsonResponse({'task_id': result.id, 'status': result.status})

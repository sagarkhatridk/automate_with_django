from django.shortcuts import render
from django.http import HttpResponse
from dataentry.tasks import celery_test_task

def home(request):
    return render(request, 'home.html')

def celery_test(request):
    result = celery_test_task.delay()
    return HttpResponse(f"<h3>Function executed successfully. Task ID: {result.id}</h3>")

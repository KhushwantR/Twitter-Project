from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

def register(request):
    return render(request, 'register.html')

def layout(request):
    return render(request, 'layout.html')

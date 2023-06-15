from django.shortcuts import render
from store import  forms

# Create your views here.

def home (request):
    return render(request, 'home.html')


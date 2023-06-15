from django.shortcuts import render
from store import forms

# Create your views here.

def home (request):
    form = forms.RegisterForm()
    return render(request, 'home.html',{'form':form})

def product_page (request):
    return render(request,'product_page.html')


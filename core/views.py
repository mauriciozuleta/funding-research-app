def signup_intro(request):
    return render(request, 'signup_intro.html')
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

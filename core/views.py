def dashboard(request):
    return render(request, 'dashboard.html')
def signup_intro(request):
    return render(request, 'signup_intro.html')

from django.shortcuts import render, redirect
from django.contrib import messages

def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        # Basic validation
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'register.html', {'first_name': first_name, 'last_name': last_name, 'email': email})
        if not first_name or not last_name or not email or not password:
            messages.error(request, 'All fields are required.')
            return render(request, 'register.html', {'first_name': first_name, 'last_name': last_name, 'email': email})
        # Here you would add user creation logic
        messages.success(request, 'User created successfully!')
        return redirect('home')
    # On GET, clear all fields
    return render(request, 'register.html', {'first_name': '', 'last_name': '', 'email': ''})

def openai_paypal(request):
    return render(request, 'openai_paypal.html')

from django.contrib.auth import logout

# ...existing code...

def logout_view(request):
    logout(request)
    return redirect('home')
from django.contrib.auth import authenticate, login
from .forms import AccountForm, UserProfileForm
from .models import UserProfile
from django.contrib.auth.models import User

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            # Check if user has a completed UserProfile
            try:
                profile = user.profile
                # Check if all required fields are filled (customize as needed)
                required_fields = ['country', 'career_stage', 'ai_consent']
                incomplete = any(not getattr(profile, f) for f in required_fields)
            except UserProfile.DoesNotExist:
                incomplete = True
            if incomplete:
                # Prepopulate form with user data
                profile_form = UserProfileForm()
                return render(request, 'register.html', {
                    'user_id': user.id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'account_created': True,
                    'profile_form': profile_form,
                })
            else:
                return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid email or password.'})
    return render(request, 'login.html')
def dashboard(request):
    return render(request, 'dashboard.html')
def signup_intro(request):
    return render(request, 'signup_intro.html')

from django.shortcuts import render, redirect
from django.contrib import messages

def home(request):
    return render(request, 'home.html')


from .forms import AccountForm, UserProfileForm
from .models import UserProfile
from django.contrib.auth.models import User
def register(request):
    if request.method == 'POST':
        account_form = AccountForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if account_form.is_valid() and profile_form.is_valid():
            # Create user
            user = account_form.save(commit=False)
            user.username = account_form.cleaned_data['email']
            user.set_password(account_form.cleaned_data['password'])
            user.save()
            # Create profile
            UserProfile.objects.create(
                user=user,
                country=profile_form.cleaned_data['country'],
                state=profile_form.cleaned_data.get('state', ''),
                career_stage=profile_form.cleaned_data['career_stage'],
                institution_name=profile_form.cleaned_data['institution_name'],
                discipline=profile_form.cleaned_data.get('discipline', ''),
                ai_consent=profile_form.cleaned_data['ai_consent']
            )
            # Log in user
            from django.contrib.auth import authenticate, login
            user = authenticate(request, username=user.username, password=account_form.cleaned_data['password'])
            if user is not None:
                login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'register.html', {
                'form': account_form,
                'profile_form': profile_form,
                'first_name': request.POST.get('first_name', ''),
                'last_name': request.POST.get('last_name', ''),
                'email': request.POST.get('email', ''),
                'form_errors': account_form.errors,
                'profile_errors': profile_form.errors,
            })
    else:
        account_form = AccountForm()
        profile_form = UserProfileForm()
        return render(request, 'register.html', {
            'form': account_form,
            'profile_form': profile_form,
            'first_name': '',
            'last_name': '',
            'email': '',
        })

def openai_paypal(request):
    return render(request, 'openai_paypal.html')

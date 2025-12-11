
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_intro, name='signup_intro'),
    path('signup/register/', views.register, name='register'),
    path('openai-paypal/', views.openai_paypal, name='openai_paypal'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]

"""basic URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from .views import AboutView, ContactView, FaqView, DashboardView, login

urlpatterns = [
    path('', login, name='index'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('faq/', FaqView.as_view(), name='faq'),
    path('register/', include('register.urls')),
    path('change/', include('forgot_pass.urls')),
    path('dashboard/', DashboardView.as_view(), name='login')

]
"""basic URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from .views import MainView, AboutView, ContactView, FaqView

urlpatterns = [
    path('', MainView.as_view(), name='index'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('faq/', FaqView.as_view(), name='faq'),
    path('register/', include('register.urls'))

]
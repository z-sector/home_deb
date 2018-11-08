"""basic URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from basic.views import AboutView, ContactView, FaqView, MainView

urlpatterns = [
    path('', MainView.as_view(), name='index'),
    path('user/', include('apps.user_management.accounts.urls')),
    path('about/', AboutView.as_view(), name='about'),
    path('contacts/', ContactView.as_view(), name='contacts'),
    path('faq/', FaqView.as_view(), name='faq'),
    path('registration/', include('apps.user_management.register.urls')),
    path('change/', include('apps.user_management.forgot_pass.urls')),
    path('dashboard/', include('apps.dashboard.urls'))

]
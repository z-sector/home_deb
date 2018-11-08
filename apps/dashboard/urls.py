from django.contrib import admin
from django.urls import path, include
from apps.dashboard.views import LoginDashboardtView

urlpatterns = [
    path('', LoginDashboardtView.as_view(), name='login_dashboard'),
]

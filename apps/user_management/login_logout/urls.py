from django.contrib import admin
from django.urls import path, include
from apps.user_management.login_logout.views import LoginActiveView, LogoutView

urlpatterns = [
    path('login/activate/', LoginActiveView.as_view(), name='login_activate'),
    path('logout/', LogoutView.as_view(), name='logout')
]

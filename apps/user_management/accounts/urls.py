from django.contrib import admin
from django.urls import path, include
from .views import LoginActiveView, LogoutView, DeleteAcountView

urlpatterns = [
    path('login/activate/', LoginActiveView.as_view(), name='login_activate'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('delete/', DeleteAcountView.as_view(), name='delete_account'),
]

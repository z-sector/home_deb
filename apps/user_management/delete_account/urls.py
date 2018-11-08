from django.contrib import admin
from django.urls import path, include
from .views import DeleteAcountView

urlpatterns = [
    path('delete/', DeleteAcountView.as_view(), name='delete_account'),
]

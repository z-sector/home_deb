from django.contrib import admin
from django.urls import path, include
from .views import ChangeView

urlpatterns = [
    path('', ChangeView.as_view(), name='change'),

]

from django.contrib import admin
from django.urls import path, include
from .views import MainView, ConsumersView, OrganizationsView, Regulators

urlpatterns = [
    path('', MainView.as_view(), name='index'),
    path('consumers/', ConsumersView.as_view(), name='consumers'),
    path('organizations/', OrganizationsView.as_view(), name='organizations'),
    path('regulators/', Regulators.as_view(), name='regulators'),
]

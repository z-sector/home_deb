from django.contrib import admin
from django.urls import path, include
from .views import (
    MainView, ConsumersView, OrganizationsView, RegulatorsView, RegistrationView
)


urlpatterns = [
    path('', MainView.as_view(), name='register'),
    path('consumers/', ConsumersView.as_view(), name='consumers'),
    path('organizations/', OrganizationsView.as_view(), name='organizations'),
    path('regulators/', RegulatorsView.as_view(), name='regulators'),
    path('consumers/registration/', RegistrationView.as_view(), name='registration')
]

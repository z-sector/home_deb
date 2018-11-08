from django.contrib import admin
from django.urls import path, include, re_path

from apps.user_management.register.views import (
    MainView, ConsumerRegistrationBaseView, OrganizationsView, RegulatorsView,
    ConsumerRegistrationActivateView, ConsumerRegistrationMainView, ConsumerRegistrationQuestionsView,
    ConsumerRegistrationTermsView, ConsumerRegistrationEffectView
)

urlpatterns = [
    path('', MainView.as_view(), name='registration'),
    path('consumer/base/', ConsumerRegistrationBaseView.as_view(), name='consumer_registration_base'),
    path('organization/', OrganizationsView.as_view(), name='organization'),
    path('regulator/', RegulatorsView.as_view(), name='regulator')
]

urlpatterns += [
    path('consumer/activate/', ConsumerRegistrationActivateView.as_view(),
         name='consumer_registration_activate'),
    path('consumer/main/', ConsumerRegistrationMainView.as_view(),
         name='consumer_registration_main'),
    path('consumer/questions/', ConsumerRegistrationQuestionsView.as_view(),
         name='consumer_registration_questions'),
    path('consumer/terms/', ConsumerRegistrationTermsView.as_view(),
         name='consumer_registration_terms'),
    path('consumer/effect/', ConsumerRegistrationEffectView.as_view(),
         name='consumer_registration_effect'),
]

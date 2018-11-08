from django.contrib import admin
from django.urls import path, include
from .views import (
    RecoverView, CheckSecretQuestionsView, NewPasswordView, FinishRestorationView)

urlpatterns = [
    path('', RecoverView.as_view(), name='recover'),
    path('question/', CheckSecretQuestionsView.as_view(), name='secret_question'),
    path('question/restoration/', NewPasswordView.as_view(), name='new_Password'),
    path('question/restoration/done/', FinishRestorationView.as_view(), name='done'),
]

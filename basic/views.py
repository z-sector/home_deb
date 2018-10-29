from django.views.generic.base import View
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import auth
import redis
from django.core.mail import send_mail
from threading import Thread
from django.conf import settings


# Create your views here.


# class MainView(View):
#     template_name = 'index.html'
#
#     def get(self, request, *args, **kwargs):
#         return render(request, self.template_name)


class AboutView(View):
    template_name = 'about.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class ContactView(View):
    template_name = 'contact.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class FaqView(View):
    template_name = 'faq.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class DashboardView(View):
    template_name = 'dashboard.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            return render(request, "dashboard.html", {'username': username})
        else:
            return render(request, "error_login.html", {'error': True})

    return render(request, "index.html")

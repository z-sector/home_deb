from django.views.generic.base import View
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import auth
import redis
from django.core.mail import send_mail
from threading import Thread
from django.conf import settings
import jwt


# Create your views here.


class MainView(View):
    template_name = 'index.html'

    def get(self, request):
        cookie = request.COOKIES.get('session')
        if cookie:
            redis_db = redis.Redis(settings.REDIS_HOST, port=settings.REDIS_PORT,
                                         password=settings.REDIS_PASSWORD)
            data = redis_db.get(f'session:{cookie}')
            print(data)
            if data:
                return redirect('login_dashboard')
        return render(request, self.template_name)


class AboutView(View):
    template_name = 'about.html'

    def get(self, request):
        return render(request, self.template_name)


class ContactView(View):
    template_name = 'contacts.html'

    def get(self, request):
        return render(request, self.template_name)


class FaqView(View):
    template_name = 'faq.html'

    def get(self, request):
        return render(request, self.template_name)






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
            redis_db = redis.StrictRedis(settings.REDIS_HOST, port=settings.REDIS_PORT,
                                         password=settings.REDIS_PASSWORD)
            data = redis_db.get(f'session:{cookie}')
            if data:
                data = jwt.decode(data, settings.SECRET_KEY, algorithm=settings.JWS_ALGORITHM)
                if data.get('user_type') == '1':
                    response = render(
                        request,
                        template_name='dashboard_consumer.html',
                        context={'username': data.get('email')}
                    )
                    return response
        return render(request, self.template_name)


class AboutView(View):
    template_name = 'about.html'

    def get(self, request):
        return render(request, self.template_name)


class ContactView(View):
    template_name = 'contact.html'

    def get(self, request):
        return render(request, self.template_name)


class FaqView(View):
    template_name = 'faq.html'

    def get(self, request):
        return render(request, self.template_name)






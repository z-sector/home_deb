from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.contrib import auth

from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.contrib import auth

import secrets
import jwt
from datetime import datetime, timedelta
import redis
from threading import Thread

from apps.user_management.accounts.models import User


# Create your views here.

class LoginActiveView(View):
    template_name = 'login_active.html'

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user:
            user_id = secrets.token_urlsafe(settings.SECRET_BYTE)
            redis_db = redis.StrictRedis(settings.REDIS_HOST, port=settings.REDIS_PORT,
                                         password=settings.REDIS_PASSWORD)

            user_type = str(user.user_type)

            payload = {
                'email': username,
                'user_type': user_type
            }
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWS_ALGORITHM).decode('utf-8')
            redis_db.set(f'user:{user_id}', token)
            redis_db.expire(f'user:{user_id}', settings.REDIS_EXPIRE)
            message = f'Activation code:\n{user_id}'
            thread = Thread(target=send_mail,
                            args=('Hello', message, '', [username]))
            thread.daemon = True
            thread.start()
            return render(request, self.template_name, {'username': username})
        return render(request, template_name="index.html", context={'error': True})

    def get(self, request):
        return render(request, self.template_name)


class LogoutView(View):

    def post(self, request):
        data = {key: ''.join(value) for key, value in request.POST.items()}
        token = data.pop('csrfmiddlewaretoken')

        cookie = request.COOKIES.get('session')
        response_redirect = redirect('/')
        response_redirect.delete_cookie('cookie')

        redis_db = redis.StrictRedis(settings.REDIS_HOST, port=settings.REDIS_PORT,
                                     password=settings.REDIS_PASSWORD)
        redis_db.delete(f'session:{cookie}')

        return response_redirect

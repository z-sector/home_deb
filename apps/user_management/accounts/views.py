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
from apps.user_management.utils import send_by_email_message, create_token_activate
from apps.user_management.backends import authentic


# Create your views here.

class LoginActiveView(View):
    template_name = 'login_token.html'

    def post(self, request):
        if request.COOKIES.get('activate'):
            return render(request, self.template_name,
                          context={'error': 'A verification code has already been sent by email to you'})
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authentic(username=username, password=password)
        if user:
            user_id, user_code = create_token_activate(username=username, user_type=str(user.user_type))
            send_by_email_message(message=f'{user_code}', recipient=user.email)
            response = render(request, self.template_name)
            response.set_cookie(
                'activate',
                user_id,
                expires=(datetime.now() + timedelta(seconds=settings.REDIS_EXPIRE)),
                path='/'
            )
            return response
        return render(request, template_name="index.html", context={'error': 'Incorrect email or password'})


class LogoutView(View):

    def post(self, request):
        data = {key: ''.join(value) for key, value in request.POST.items()}
        token = data.pop('csrfmiddlewaretoken')

        cookie = request.COOKIES.get('session')
        response_redirect = redirect('/')
        response_redirect.delete_cookie('cookie')

        redis_db = redis.Redis(settings.REDIS_HOST, port=settings.REDIS_PORT,
                               password=settings.REDIS_PASSWORD)
        redis_db.delete(f'session:{cookie}')

        return response_redirect


class DeleteAcountView(View):
    template_name = 'delete_account.html'

    def post(self, request):
        cookie = request.COOKIES.get('session')
        if cookie is None:
            return render(request, template_name='dashboard.html')
        redis_db = redis.StrictRedis(settings.REDIS_HOST, port=settings.REDIS_PORT, password=settings.REDIS_PASSWORD)
        data = redis_db.get(f'session:{cookie}')
        if data is None:
            return render(request, template_name='dashboard.html')
        data = jwt.decode(data, settings.SECRET_KEY, algorithm=settings.JWS_ALGORITHM)
        User.objects.filter(email=data.get('email')).delete()
        return render(request, self.template_name)

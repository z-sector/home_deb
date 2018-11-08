from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.contrib import auth
from django.utils import timezone

import secrets
import jwt
from datetime import datetime, timedelta
import redis
from threading import Thread

from apps.user_management.accounts.models import User


class LoginDashboardtView(View):

    def post(self, request):
        user_id = request.POST.get('code')
        redis_db = redis.StrictRedis(settings.REDIS_HOST, port=settings.REDIS_PORT, password=settings.REDIS_PASSWORD)
        token = redis_db.get(f'user:{user_id}')

        if not token:
            messages.add_message(request, messages.INFO,
                                 'Invalid activation code entered, try again. Or Registration time out')
            return redirect('/user/login/activate/')

        data = jwt.decode(token, settings.SECRET_KEY, algorithm=settings.JWS_ALGORITHM)

        session_id = secrets.token_urlsafe(settings.SESSION_BYTE)
        redis_db.set(f'session:{session_id}', token)
        redis_db.expire(f'session:{session_id}', settings.SESSION_EXPIRE)

        user = User.objects.get(email=data.get('email'))
        user.last_login = timezone.now()
        user.save()
        if data.get('user_type') == '1':
            response = render(
                request,
                template_name='dashboard_consumer.html',
                context={'username': data.get('email')}
            )
            response.set_cookie(
                'session',
                session_id,
                path='/'
            )
            return response

    def get(self, request):
        cookie = request.COOKIES.get('session')
        if cookie is None:
            return render(request, template_name='dashboard_consumer.html')
        redis_db = redis.StrictRedis(settings.REDIS_HOST, port=settings.REDIS_PORT, password=settings.REDIS_PASSWORD)
        data = redis_db.get(f'session:{cookie}')
        if data is None:
            return render(request, template_name='dashboard_consumer.html')
        data = jwt.decode(data, settings.SECRET_KEY, algorithm=settings.JWS_ALGORITHM)
        if data.get('user_type') == '1':
            response = render(
                request,
                template_name='dashboard_consumer.html',
                context={'username': data.get('email')}
            )
            return response
        return render(request, template_name='dashboard_consumer.html')

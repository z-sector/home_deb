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
from apps.user_management.utils import create_token_session


class LoginDashboardtView(View):

    def post(self, request):
        cookie = request.COOKIES.get('activate')
        if not cookie:
            return render(request, 'index.html', context={'error': 'Registration time out'})

        user_id = request.POST.get('verification_code')
        redis_db = redis.Redis(settings.REDIS_HOST, port=settings.REDIS_PORT, password=settings.REDIS_PASSWORD)
        token = redis_db.get(f'user:{user_id}')

        if not token:
            return render(request, 'login_token.html', context={'error': 'Invalid activation code entered, try again!'})

        data = jwt.decode(token, settings.SECRET_KEY, algorithm=settings.JWS_ALGORITHM)

        user = User.objects.get(email=data.get('email'))
        user.last_login = timezone.now()
        user.save()

        # for field_name in user._meta.local_fields:
        #     print(field_name.name)
        #     value = getattr(user, field_name.name, None)
        #     print(value.__str__())

        data = {key: value for key, value in user}
        session_id = create_token_session(**data)


        # session_id = secrets.token_urlsafe(settings.SESSION_BYTE)
        # redis_db.set(f'session:{session_id}', token)
        # redis_db.expire(f'session:{session_id}', settings.SESSION_EXPIRE)

        response = render(
            request,
            template_name='dashboard.html',
            context=data
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
            return render(request, template_name='index.html')
        redis_db = redis.Redis(settings.REDIS_HOST, port=settings.REDIS_PORT, password=settings.REDIS_PASSWORD)
        data = redis_db.get(f'session:{cookie}')
        if data is None:
            return render(request, template_name='index.html')
        data = jwt.decode(data, settings.SECRET_KEY, algorithm=settings.JWS_ALGORITHM)
        response = render(
            request,
            template_name='dashboard.html',
            context=data
        )
        return response

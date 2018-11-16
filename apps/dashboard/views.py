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
from apps.user_management.backends import login


class LoginDashboardtView(View):

    def post(self, request):
        cookie = request.COOKIES.get('activate')
        if not cookie:
            return render(request, 'index.html', context={'error': 'Registration time out'})

        verification_code = request.POST.get('verification_code')
        redis_db = redis.Redis(settings.REDIS_HOST, port=settings.REDIS_PORT, password=settings.REDIS_PASSWORD)

        token = redis_db.get(f'user:{cookie}')
        if not token:
            return render(request, 'index.html', context={'error': 'Registration time out'})

        data = jwt.decode(token, settings.SECRET_KEY, algorithm=settings.JWS_ALGORITHM)
        user_code = data.get('user_code')

        if verification_code != user_code:
            return render(request, 'login_token.html', context={'error': 'Invalid activation code entered, try again!'})

        data = login(data.get('username'))

        session_id = create_token_session(**data)

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

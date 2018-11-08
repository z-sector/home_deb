from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings

import secrets
import jwt
from datetime import datetime, timedelta
import redis
from threading import Thread

from apps.user_management.accounts.models import User

class DeleteAcountView(View):
    def post(self, request):
        cookie = request.COOKIES.get('session')
        if cookie is None:
            return render(request, template_name='dashboard_consumer.html')
        redis_db = redis.StrictRedis(settings.REDIS_HOST, port=settings.REDIS_PORT, password=settings.REDIS_PASSWORD)
        data = redis_db.get(f'session:{cookie}')
        if data is None:
            return render(request, template_name='dashboard_consumer.html')
        data = jwt.decode(data, settings.SECRET_KEY, algorithm=settings.JWS_ALGORITHM)
        print(data)
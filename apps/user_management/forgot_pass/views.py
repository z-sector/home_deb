from django.views.generic.base import View
from django.shortcuts import render, redirect
from apps.user_management.accounts.models import User
from django.conf import settings
from django.contrib import messages

import redis
import jwt
import secrets

from datetime import datetime, timedelta


class RecoverView(View):
    template_name = 'change.html'

    def get(self, request):
        return render(request, self.template_name)


class CheckSecretQuestionsView(View):
    template_name = 'change_secret_question.html'

    def get(self, request):
        token = request.COOKIES.get('restore')
        if token is None:
            return redirect('./')

        token = token.encode('utf-8')
        try:
            user_id = jwt.decode(token, settings.SECRET_KEY, algorithm=settings.JWS_ALGORITHM)['id']
        except Exception:
            return redirect('./')

        redis_db = redis.StrictRedis(settings.REDIS_HOST, port=settings.REDIS_PORT,
                                     password=settings.REDIS_PASSWORD)
        user_id_key = redis_db.hkeys(f'user:{user_id}')
        if not user_id_key:
            error = 'Registration time out'
            messages.add_message(request, messages.INFO, error)
            return redirect(request, './../')

        response = render(request, self.template_name,
                          {'email': redis_db.hget(f'user:{user_id}', 'email').decode('utf-8')})
        return response

    def post(self, request):
        email = request.POST.get("email", "")
        user = User()
        try:
            user = User.objects.get(email=email)
        except user.DoesNotExist:
            messages.add_message(request, messages.INFO, 'Error, no such user')
            return redirect('./../')
        data = {'email': user.email, 'answer_1': user.answer_1, 'answer_2': user.answer_2, 'answer_3': user.answer_3}


        user_id = secrets.token_urlsafe(settings.SECRET_BYTE)
        redis_db = redis.StrictRedis(settings.REDIS_HOST, port=settings.REDIS_PORT, password=settings.REDIS_PASSWORD)
        all([redis_db.hset(f'user:{user_id}', key,
                           jwt.encode(dict(answer=value), settings.SECRET_KEY, algorithm=settings.JWS_ALGORITHM).decode(
                               'utf-8'))
             if key in ('answer_1', 'answer_2', 'answer_3') else redis_db.hset(f'user:{user_id}', key, value)
             for key, value in data.items()])
        redis_db.expire(f'user:{user_id}', settings.REDIS_EXPIRE)

        payload = {
            'id': user_id
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWS_ALGORITHM).decode('utf-8')
        response = render(request, self.template_name, {
            'email': email, 'question_1': user.question_1, 'question_2': user.question_2, 'question_3': user.question_3,
        })
        response.set_cookie(
            'restore',
            token,
            expires=(datetime.now() + timedelta(seconds=settings.REDIS_EXPIRE)),
            path='/'
        )
        return response


class NewPasswordView(View):
    template_name = 'change_new_password.html'

    def post(self, request):
        token = request.COOKIES.get('restore')

        if token is None:
            return redirect('./../../')

        token = token.encode('utf-8')
        try:
            user_id = jwt.decode(token, settings.SECRET_KEY, algorithm=settings.JWS_ALGORITHM)['id']
        except Exception:
            return redirect('./../../')

        redis_db = redis.StrictRedis(settings.REDIS_HOST, port=settings.REDIS_PORT,
                                     password=settings.REDIS_PASSWORD)
        user_id_key = redis_db.hkeys(f'user:{user_id}')
        if not user_id_key:
            error = 'Registration time out'
            messages.add_message(request, messages.INFO, error)
            return redirect(request, './../../')

        answer_1 = request.POST.get('answer_1', "")
        answer_2 = request.POST.get('answer_2', "")
        answer_3 = request.POST.get('answer_3', "")

        if (answer_1 != jwt.decode(redis_db.hget(f'user:{user_id}', 'answer_1'), settings.SECRET_KEY,
                                   algorithm=settings.JWS_ALGORITHM)['answer']
                or
                answer_2 != jwt.decode(redis_db.hget(f'user:{user_id}', 'answer_2'), settings.SECRET_KEY,
                                       algorithm=settings.JWS_ALGORITHM)['answer']
                or
                answer_3 != jwt.decode(redis_db.hget(f'user:{user_id}', 'answer_3'), settings.SECRET_KEY,
                                       algorithm=settings.JWS_ALGORITHM)['answer']):
            messages.add_message(request, messages.INFO, 'Wrong secret answer')
            return redirect('./../')

        return render(request, self.template_name)


class FinishRestorationView(View):
    template_name = 'change_done.html'

    def post(self, request):
        token = request.COOKIES.get('restore')

        if token is None:
            messages.add_message(request, messages.INFO, 'Wrong token')
            return redirect('index')

        token = token.encode('utf-8')

        try:
            user_id = jwt.decode(token, settings.SECRET_KEY, algorithm=settings.JWS_ALGORITHM)['id']
        except Exception:
            messages.add_message(request, messages.INFO, 'Wrong token')
            return redirect('index')

        redis_db = redis.StrictRedis(settings.REDIS_HOST, port=settings.REDIS_PORT,
                                     password=settings.REDIS_PASSWORD)
        user_id_key = redis_db.hkeys(f'user:{user_id}')

        if not user_id_key:
            error = 'Registration time out'
            self.template_name = 'error.html'
            messages.add_message(request, messages.INFO, error)
            return render(request, 'index.html', {'reg_errors': error})
        email = redis_db.hget(f'user:{user_id}', 'email').decode('utf-8')
        redis_db.delete(user_id)
        response = render(request, self.template_name)

        response.delete_cookie('restore')
        new_password = request.POST.get("password", "")
        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()
        return response

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


# Create your views here.

class ErrorMessage:

    @staticmethod
    def email_validate(data):
        error = ''
        user = User(**data)
        try:
            user.validate_unique()
        except ValidationError:
            email = data["email"]
            error = f'User {email} exists, try again'
        return error

    @staticmethod
    def redis_session_timeout(redis_db, user_id):
        error = ''
        user_id_key = redis_db.hkeys(f'user:{user_id}')
        if not user_id_key:
            error = 'Registration time out'
        return error

    @staticmethod
    def valid_token(request):
        token = request.COOKIES.get('activate')

        if token is None:
            return None

        token = token.encode('utf-8')

        try:
            user_id = jwt.decode(token, settings.SECRET_KEY, algorithm=settings.JWS_ALGORITHM)['id']
        except Exception:
            return None

        return user_id


class MainView(View):
    template_name = 'registration_type.html'

    def get(self, request):
        return render(request, self.template_name)


class ConsumerRegistrationBaseView(View):
    template_name = 'registration_consumer.html'

    def get(self, request):
        return render(request, self.template_name)


class OrganizationsView(View):
    template_name = 'base_organizations.html'

    def get(self, request):
        return render(request, self.template_name)


class RegulatorsView(View):
    template_name = 'base_regulators.html'

    def get(self, request):
        return render(request, self.template_name)


class ConsumerRegistrationActivateView(View, ErrorMessage):
    template_name = 'registration_activate.html'

    def post(self, request):
        data = {key: ''.join(value) for key, value in request.POST.items()}
        data.pop('csrfmiddlewaretoken')

        # r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        #
        # import re
        #
        # if not re.match(r"... regex here ...", email):
        # ^(?=.*[0-9])(?=.*[!@# $%^&*()\-_+={}[\]\'\",.?<>/\\|])(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z!@#$%^&*()\-_+={}[\]\'\",.?<>/\\|]{8,}$


        error = self.email_validate({'email': data.get('email')})
        if error:
            messages.add_message(request, messages.INFO, error)
            return redirect('../base/')

        user_id = secrets.token_urlsafe(settings.SECRET_BYTE)

        redis_db = redis.StrictRedis(settings.REDIS_HOST, port=settings.REDIS_PORT, password=settings.REDIS_PASSWORD)
        all([redis_db.hset(f'user:{user_id}', key, value) for key, value in data.items()])
        redis_db.expire(f'user:{user_id}', settings.REDIS_EXPIRE)

        message = f'Activation code:\n{user_id}'
        thread = Thread(target=send_mail,
                        args=('Hello', message, '', [data['email']]))
        thread.daemon = True
        thread.start()

        return render(request, self.template_name, {'username': data.get('email')})

    def get(self, request):
        return render(request, self.template_name)


class ConsumerRegistrationMainView(View, ErrorMessage):
    template_name = 'consumer_registration_main.html'

    def post(self, request):
        user_id = request.POST.get('code')
        redis_db = redis.StrictRedis(settings.REDIS_HOST, port=settings.REDIS_PORT, password=settings.REDIS_PASSWORD)
        user_id_key = redis_db.hkeys(f'user:{user_id}')

        if not user_id_key:
            messages.add_message(request, messages.INFO,
                                 'Invalid activation code entered, try again. Or Registration time out')
            return redirect('../activate/')

        payload = {
            'id': user_id,
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWS_ALGORITHM).decode('utf-8')
        response = render(request, self.template_name)
        response.set_cookie(
            'activate',
            token,
            expires=(datetime.now() + timedelta(seconds=settings.REDIS_EXPIRE)),
            path='/register/consumer/'
        )

        return response

    def get(self, request):
        user_id = self.valid_token(request)
        if user_id is None:
            return redirect('register')

        redis_db = redis.StrictRedis(settings.REDIS_HOST, port=settings.REDIS_PORT,
                                     password=settings.REDIS_PASSWORD)

        error = self.redis_session_timeout(redis_db, user_id)
        if error:
            messages.add_message(request, messages.INFO, error)
            return redirect('register')

        return render(request, self.template_name)


class ConsumerRegistrationQuestionsView(View, ErrorMessage):
    template_name = 'consumer_registration_questions.html'

    def post(self, request):
        data = {key: ''.join(value) for key, value in request.POST.items()}
        token = data.pop('csrfmiddlewaretoken')

        user_id = self.valid_token(request)
        if user_id is None:
            return redirect('register')

        if data.get('password') != data.get('password_confirm') or data.get('password') is None:
            error = 'Invalid password confirmed'
            messages.add_message(request, messages.INFO, error)
            return redirect('../main/')

        data.pop('password_confirm')
        data['password'] = jwt.encode({'passw': data.get('password')}, settings.SECRET_KEY)

        redis_db = redis.StrictRedis(settings.REDIS_HOST, port=settings.REDIS_PORT, password=settings.REDIS_PASSWORD)

        error = self.redis_session_timeout(redis_db, user_id)
        if error:
            messages.add_message(request, messages.INFO, error)
            return redirect('register')

        db_email = redis_db.hget(f'user:{user_id}', 'email').decode('utf-8')
        if db_email != data.get('email'):
            error = 'Invalid email'
            messages.add_message(request, messages.INFO, error)
            return redirect('../main/')

        all([redis_db.hset(f'user:{user_id}', key, value) for key, value in data.items()])

        return render(request, self.template_name)


class ConsumerRegistrationTermsView(View, ErrorMessage):
    template_name = 'consumer_registration_terms.html'

    def post(self, request):
        data = {key: ''.join(value) for key, value in request.POST.items()}
        token = data.pop('csrfmiddlewaretoken')

        user_id = self.valid_token(request)
        if user_id is None:
            return redirect('register')

        redis_db = redis.StrictRedis(settings.REDIS_HOST, port=settings.REDIS_PORT,
                                     password=settings.REDIS_PASSWORD)

        error = self.redis_session_timeout(redis_db, user_id)
        if error:
            messages.add_message(request, messages.INFO, error)
            return redirect('register')

        # Record answers in the form of hash answers
        all([redis_db.hset(f'user:{user_id}', key,
                           jwt.encode(dict(answer=value), settings.SECRET_KEY, algorithm=settings.JWS_ALGORITHM).decode(
                               'utf-8'))
             if key in ('answer_1', 'answer_2', 'answer_3') else redis_db.hset(f'user:{user_id}', key, value)
             for key, value in data.items()]
            )

        return render(request, self.template_name)


class ConsumerRegistrationEffectView(View, ErrorMessage):
    template_name = 'end.html'

    def post(self, request):
        data = {key: ''.join(value) for key, value in request.POST.items()}
        token = data.pop('csrfmiddlewaretoken')
        data = {key: True for key, value in data.items() if value == 'on'}

        user_id = self.valid_token(request)
        if user_id is None:
            return redirect('register')

        redis_db = redis.StrictRedis(settings.REDIS_HOST, port=settings.REDIS_PORT,
                                     password=settings.REDIS_PASSWORD)

        error = self.redis_session_timeout(redis_db, user_id)
        if error:
            messages.add_message(request, messages.INFO, error)
            return redirect('register')

        data_db = redis_db.hgetall(f'user:{user_id}')
        data_db = {key.decode('utf-8'): value.decode('utf-8') for key, value in data_db.items()}
        redis_db.delete(f'user:{user_id}')

        data_db['password'] = jwt.decode(data_db['password'], settings.SECRET_KEY,
                                         algorithm=settings.JWS_ALGORITHM)['passw']

        keys = ('answer_1', 'answer_2', 'answer_3')

        data_db = {key: (jwt.decode(value, settings.SECRET_KEY, algorithm=settings.JWS_ALGORITHM)['answer']
                         if key in keys else value) for key, value in data_db.items()}

        data.update(data_db)

        print(data)

        password = data.pop('password')

        user = User(**data)
        user.set_password(password)

        user.save()

        response = render(request, self.template_name)
        response.delete_cookie('activate')

        return render(request, self.template_name)

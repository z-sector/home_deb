from django.core.mail import send_mail
from django.conf import settings
from django.template import loader

from threading import Thread
import redis
import jwt
import secrets


def send_by_email_message(message, recipient):
    html_message = loader.render_to_string('email.html', context={'verification_code': message})
    thread = Thread(target=send_mail,
                    args=('Debitrum', message, '', [recipient]), kwargs={'html_message': html_message})
    thread.daemon = True
    thread.start()


def create_token_activate(**kwargs):
    user_code = secrets.token_urlsafe(settings.SECRET_BYTE)
    kwargs.update(user_code=user_code)
    redis_db = redis.Redis(settings.REDIS_HOST, port=settings.REDIS_PORT,
                           password=settings.REDIS_PASSWORD)
    token = jwt.encode(kwargs, settings.SECRET_KEY, algorithm=settings.JWS_ALGORITHM).decode('utf-8')
    user_id = secrets.token_urlsafe(settings.SESSION_BYTE)
    redis_db.set(f'user:{user_id}', token)
    redis_db.expire(f'user:{user_id}', settings.REDIS_EXPIRE)
    return user_id, user_code


def create_token_session(**kwargs):
    redis_db = redis.Redis(settings.REDIS_HOST, port=settings.REDIS_PORT,
                           password=settings.REDIS_PASSWORD)
    session_id = secrets.token_urlsafe(settings.SESSION_BYTE)
    token = jwt.encode(kwargs, settings.SECRET_KEY, algorithm=settings.JWS_ALGORITHM).decode('utf-8')
    redis_db.set(f'session:{session_id}', token)
    redis_db.expire(f'session:{session_id}', settings.SESSION_EXPIRE)
    return session_id

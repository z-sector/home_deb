from django.utils import timezone

from apps.user_management.accounts.models import User


def authentic(username=None, password=None):
    if username is None or password is None:
        return False

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return False

    if user.check_password(password):
        return user
    else:
        return False


def login(username):
    user = User.objects.get(username=username)

    user.last_login = timezone.now()
    user.save()

    data = {key: value for key, value in user}

    return data

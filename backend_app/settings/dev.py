from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'xit(-1e(53z+_mr=un&=!clrn-bps7+&2__41a4!1cefnc^zs@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '127.0.0.1',
    '192.168.1.63'
]


STATICFILES_DIRS = [
    os.path.join(os.path.dirname(BASE_DIR), "static"),
]

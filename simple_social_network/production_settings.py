from .base_settings import *

DEBUG = False

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'simple_social_network_data',
        'USER': 'postgres',
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# static files cnfgurations
STATIC_URL = "/static"
STATIC_ROOT = os.path.join(BASE_DIR, "static/")

# HTTPS settings
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True


# HSTS settings
SECURE_HSTS_SECONDS = 31536000 # 1 year
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True


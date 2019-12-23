"""
Django settings for qteam_quest project.
"""

import os

from dotenv import load_dotenv

from qteam_quest.utils import get_env_value

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ROOT_URL = get_env_value('ROOT_URL')

SECRET_KEY = get_env_value('SECRET_KEY')

DEBUG = get_env_value('DEBUG')

ALLOWED_HOSTS = [
    host.lower() for host in get_env_value('ALLOWED_HOSTS').split(',')
]

# Application definition settings
INSTALLED_APPS = [
    # Django`s apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # Installed apps
    'rest_framework',
    'rest_framework.authtoken',

    # Created apps
    'users',
    'apps.dashboard',
    'apps.quests',
    'apps.games',
    'apps.teams',
    'apps.coupons',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'qteam_quest.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'qteam_quest.wsgi.application'

# Database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': get_env_value('POSTGRES_DB_NAME'),
        'USER': get_env_value('POSTGRES_DB_USER'),
        'PASSWORD': get_env_value('POSTGRES_DB_PASSWORD'),
        'HOST': get_env_value('POSTGRES_DB_HOST'),
        'PORT': int(get_env_value('POSTGRES_DB_PORT')),
    }
}

# Password validation settings
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization settings
LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    '../static/',
]

# Media files
MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Authentication settings
AUTH_USER_MODEL = 'users.User'

ACCOUNT_USER_MODEL_USERNAME_FIELD = 'phone'

ACCOUNT_AUTHENTICATION_METHOD = 'phone'

ACCOUNT_EMAIL_REQUIRED = False

ACCOUNT_UNIQUE_EMAIL = True

ACCOUNT_USERNAME_REQUIRED = True

ACCOUNT_USER_EMAIL_FIELD = 'email'

ACCOUNT_LOGOUT_ON_GET = True

# REST settings
REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'users.serializers.UserSerializer',
}

REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': 'users.serializers.UserRegisterSerializer',
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}

# Different settings
APPEND_SLASH = True

SITE_ID = 1

CSRF_COOKIE_SECURE = False

CORS_ORIGIN_ALLOW_ALL = True

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Celery settings
BROKER_URL = 'redis://localhost:6379'

CELERY_RESULT_BACKEND = 'redis://localhost:6379'

CELERY_ACCEPT_CONTENT = ['application/json', ]

CELERY_TASK_SERIALIZER = 'json'

CELERY_RESULT_SERIALIZER = 'json'

CELERY_TIMEZONE = 'Europe/Moscow'

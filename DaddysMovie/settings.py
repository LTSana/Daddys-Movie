'''
Django settings for DaddysMovie project.

Generated by 'django-admin startproject' using Django 3.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
'''

import os
import dotenv

from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load all the enviroment values if running on local machine
dotenv_file = os.path.join(BASE_DIR, '.env')
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
if os.getenv('SECRET_KEY'):
    SECRET_KEY = os.getenv('SECRET_KEY')
else:
    SECRET_KEY = """_5DC0o,D~buG1@N`=6?{xI:%y#5syy=m!Tfno?o*~2}@61|F&Aj}3IG?+[u@Nxy&=uI^W>c{QUko'\|lpxa$_dBYSC4%WN09'gj("""

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG') if os.getenv('DEBUG') else False

ALLOWED_HOSTS = [
    '192.168.100.2', 
    '127.0.0.1', 
    'localhost',
    'daddysmovie.herokuapp.com',
    ]

ADMINS = [('LT.Sana', 'snm.developer@gmail.com')]

MANAGERS = [('LT.Sana', 'snm.developer@gmail.com')]

# Application definition

# Set this to True to avoid transmitting the CSRF cookie over HTTP accidentally.
CSRF_COOKIE_SECURE = True
CSRF_FAILURE_VIEW = 'pages.views.csrf_failure'

# Set this to True to avoid transmitting the session cookie over HTTP accidentally.
SESSION_COOKIE_SECURE = True

# Enabling persistent database connections can result in a nice speed-up when connecting to 
# the database accounts for a significant part of the request processing time.
CONN_MAX_AGE = 500 # Integer is seconds (60 - seconds, 1 - second and so on)

# To always redirect the user to HTTPS
SECURE_SSL_REDIRECT = True

# *** WARNING ***
# DO NOT CHANGE THIS VALUE FROM 60s
# IF SET TO LONGER IT WILL BREAK YOUR SITE IF HTTPS CONNECTION IS LOST
SECURE_HSTS_SECONDS = 600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Redirect the user to the login page if they try
# accessing a page that requires a logged in user
LOGIN_URL = '/login'
LOGOUT_URL = '/logout'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    # - Core is for API calls to the server from HTTP Responses
    'core',
    # - Message is for the Websocket messaging and movie status
    'message',
    # - Pages is to render the html templates
    'pages',
    # - Movie is for the movie API including Websocket
    'movie',
    # - For media storage
    'cloudinary_storage',
    'cloudinary',
    # - Channels for websockets
    'channels',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# This is a whitelist of URL's allowed to connect to django
CORS_ORIGIN_WHITELIST = [
    'http://localhost:3000',
    'http://localhost:8000',
    'http://192.168.100.2:8000',
]

ROOT_URLCONF = 'DaddysMovie.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'DaddysMovie.wsgi.application'
ASGI_APPLICATION = 'DaddysMovie.asgi.application'

# Channels
CHANNEL_LAYERS = {
    'default': {
        #'BACKEND': 'channels_redis.core.RedisChannelLayer', # USE IN PRODUCTION
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASE_SETTINGS = {
    'default': {
        'ENGINE': os.getenv('DATABASE_ENGINE') if os.getenv('DATABASE_ENGINE') else 'django.db.backends.sqlite3',
        'NAME': os.getenv('DATABASE_NAME') if os.getenv('DATABASE_NAME') else BASE_DIR / 'db.sqlite3',
        'USER': os.getenv('DATABASE_USER') if os.getenv('DATABASE_USER') else None,
        'PASSWORD': os.getenv('DATABASE_PASSWORD') if os.getenv('DATABASE_PASSWORD') else None,
        'HOST': os.getenv('DATABASE_HOST') if os.getenv('DATABASE_HOST') else None,
        'PORT': os.getenv('DATABASE_PORT') if os.getenv('DATABASE_PORT') else None,
    }
}
DATABASES = DATABASE_SETTINGS


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

PROJECT_ROOT = 'staticfiles'
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

# This is the static files folder name which you created in django project root folder.
# This is different from above STATIC_URL. 
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

# Add configuration for static files storage using whitenoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Cloudinary Settings for File Upload Storage
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"
CLOUDINARY_STORAGE = { # Cloudinary Credentials
    "CLOUD_NAME": os.getenv("CLOUDINARY_NAME"),
    "API_KEY": os.getenv("CLOUDINARY_API_KEY"),
    "API_SECRET": os.getenv("CLOUDINARY_API_SECRET"),
}

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# reCAPTCHA v3 keys
RECAPTCHA_SITE_KEY = os.getenv("RECAPTCHA_SITE_KEY")
RECAPTCHA_SECRET_KEY = os.getenv("RECAPTCHA_SECRET_KEY")

# Used for React to allow POST submittions from forms
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        #'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
}

# Settings for JWT simple
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(hours=6),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,

    'ALGORITHM': 'HS512',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]
"""
Django settings for Main project.

Generated by 'django-admin startproject' using Django 4.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""


import os
from pathlib import Path


# Access the environment variable
COMPLAYING_FEDERATIONS_LINK = os.environ.get('COMPLAYING_FEDERATIONS_LINK', default='https://kznsannualreport.pythonanywhere.com')
# Read .env file
#environ.Env.read_env()
# Access the environment variable
#COMPLAYING_FEDERATIONS_LINK = env('COMPLAYING_FEDERATIONS_LINK')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'cjdncjcnjdcnjdjdcnjcnjdcndjcnjddjango-insecure-n0ujlyxp!8v$#106vocy-zo#4*+f9gduc9zc@p=c!cza77!igl'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'MyApp',
    'LoginManager',
    'ProcessApplication',
    'rest_framework',
    'manage_personnel',
      'corsheaders',
      
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
    
]
CORS_ORIGIN_WHITELIST = [
    'http://127.0.0.1:5500','http://127.0.0.1:8000'
    #'http://localhost:5173',  # Add your Vue.js application's origin here
    # Add more origins if necessary
]

ROOT_URLCONF = 'Main.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [r"C:\Users\INTERN\OneDrive\Colors\Main\MyApp\template"],
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

WSGI_APPLICATION = 'Main.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True
LOGIN_REDIRECT_URL ='login'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
MEDIA_URL = 'media/'
MEDIA_ROOT= os.path.join(BASE_DIR,'media')
STATIC_ROOT = os.path.join(BASE_DIR,'static')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_USE_TLS = False
# EMAIL_USE_SSL = True
# EMAIL_HOST = 'mail.kznsc.com'
# EMAIL_PORT = 465
# EMAIL_HOST_USER = 'admin@kznsc.com'
# EMAIL_FROM = 'admin@kznsc.com'
# EMAIL_HOST_PASSWORD = ''
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


#email config
# #EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'livesoundsmusic@gmail.com'
EMAIL_FROM = 'livesoundsmusic@gmail.com'
EMAIL_HOST_PASSWORD = 'fesezjwkjjjuyzen'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
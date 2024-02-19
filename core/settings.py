"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import environ
from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
env.read_env(str(BASE_DIR / ".env"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-d=szegh%23&@*-_e4bq+j$*iiiet@^gy5qrtqr3kmah5mloj+f'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['162.43.50.92']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

ADDTIONAL_INSTALLED_APPS = [
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'whitenoise.runserver_nostatic',
    'django_cleanup',
    'admin_reorder',
    'django_filters',
    'account',
    'unregisterCat',
    'registerCat',
    'other',
]

INSTALLED_APPS += ADDTIONAL_INSTALLED_APPS

# Custom User
AUTH_USER_MODEL = 'account.Member'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'admin_reorder.middleware.ModelAdminReorder',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
MEDIA_URL = 'media/'

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOW_CREDENTIALS = True
# CORS_ALLOW_HEADERS = ['X-CSRFTOKEN', 'content-type']

CORS_ALLOWED_ORIGINS = [
   'http://162.43.50.92'
]

CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "DELETE",
    "OPTIONS",
]

# For email
MAIL_API_KEY = env('MAIL_API_KEY')
BACKEND_EMAIL = env('BACKEND_EMAIL')

FRONT_URL = 'http://162.43.50.92'

# For reorder apps and models in admin page
ADMIN_REORDER = (
    {'app': 'account', 'models': ('account.Member', 'account.Avatar')},
    {'app': 'registerCat', 'models': ('registerCat.ShopType', 'registerCat.Shop', 'registerCat.ShopImage', 'registerCat.Cat', 'registerCat.Advertise', 'registerCat.Column', 'registerCat.ColumnBlog', 'registerCat.Character', 'registerCat.FavoriteThing', 'registerCat.Recommend', 'registerCat.Comment', 'registerCat.CommentImage', 'registerCat.ReactionWordIcon', 'registerCat.ReactionCatIcon', 'registerCat.ReactionHeartIcon', 'registerCat.ReactionSeasonIcon', 'registerCat.ReactionPartyIcon', 'registerCat.ReactionFoodIcon')},
    {'app': 'unregisterCat', 'models' : ('unregisterCat.UnregisterShop', 'unregisterCat.CatApply')},
    {'app': 'other', 'models' : ('other.Ambassador', 'other.Inquiry', 'other.Banner')},
)

# Delete files when corresponding object is deleted
CLEANUP_DELETE_FILES = True

# Delete empty folders along with files
CLEANUP_DELETE_EMPTY_FOLDERS = True
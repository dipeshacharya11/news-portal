
# Django 5.x Compatible Settings
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'ueu^l#vw611-0y&4uyhj94r#8sx4*@24kntbopq6g$y2w6sbk(')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')

# Django 5.x requirement
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #our installed app
    'mainsite.apps.MainsiteConfig',
    'news.apps.NewsConfig',
    'comment.apps.CommentConfig',
    'subscription.apps.SubscriptionConfig',
    'account.apps.AccountConfig',
    'custom_admin.apps.CustomAdminConfig',

    #3rd party
    'taggit',
    'rest_framework',
    'drf_yasg',
    'rest_framework_simplejwt.token_blacklist',

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
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'mainsite.context_processors.custom_context_processor',

            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

# USE_L10N is deprecated in Django 5.x - removed
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Media Folder Settings
MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = '/media/'

# Django 5.x Storage Configuration (replaces STATICFILES_STORAGE)
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Database Configuration (replaces django_heroku for better control)
import dj_database_url

# Use DATABASE_URL environment variable if available, otherwise use SQLite
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}'
    )
}



REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    # "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
}

from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
}

CORS_ORIGIN_WHITELIST = (
'http://localhost:3000',
'https://itech-9b147.web.app',
'https://itech-9b147.firebaseapp.com'
)

# NewsData.io API Configuration
# ===========================================
NEWSDATA_API_KEY = os.environ.get('NEWSDATA_API_KEY', '')
NEWSDATA_BASE_URL = os.environ.get('NEWSDATA_BASE_URL', 'https://newsdata.io/api/1/news')

# API Rate Limits
NEWSDATA_REQUESTS_PER_HOUR = int(os.environ.get('NEWSDATA_REQUESTS_PER_HOUR', '200'))
NEWSDATA_REQUESTS_PER_DAY = int(os.environ.get('NEWSDATA_REQUESTS_PER_DAY', '1000'))

# News Configuration
DEFAULT_NEWS_CATEGORIES = os.environ.get('DEFAULT_NEWS_CATEGORIES', 'top,politics,technology,business,sports,world,health').split(',')
DEFAULT_NEWS_LANGUAGE = os.environ.get('DEFAULT_NEWS_LANGUAGE', 'en')
DEFAULT_NEWS_COUNTRY = os.environ.get('DEFAULT_NEWS_COUNTRY', 'us')

# Cache Settings
NEWS_CACHE_TIMEOUT = int(os.environ.get('NEWS_CACHE_TIMEOUT', '1800'))  # 30 minutes
BREAKING_NEWS_CACHE_TIMEOUT = int(os.environ.get('BREAKING_NEWS_CACHE_TIMEOUT', '300'))  # 5 minutes

# Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'news_portal.log'),
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'news_api': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

"""
Django settings for elearning_system project.

Personalized E-Learning Course Recommendation System
"""

import os

# Detect if running on Render
IS_RENDER = os.getenv('RENDER', False)


# ============================================================
# BASE DIRECTORY
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ============================================================
# SECURITY
# ============================================================

SECRET_KEY = os.getenv(
    'DJANGO_SECRET_KEY',
    'wp5yy9d4=k%6q@lg)gw+@x!1+tke81-e#bpo*k7vm8a-#cs517'
)

# In production (Render), DEBUG is False. Locally it's True.
DEBUG = not IS_RENDER


# ============================================================
# ALLOWED HOSTS
# ============================================================

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'testserver',
    '.onrender.com',  # Covers all Render subdomains
]


# ============================================================
# CSRF
# ============================================================

CSRF_TRUSTED_ORIGINS = [
    'https://*.onrender.com',
]


# ============================================================
# APPLICATIONS
# ============================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'recommender',
]

if IS_RENDER:
    INSTALLED_APPS = ['whitenoise.runserver_nostatic'] + INSTALLED_APPS


# ============================================================
# CUSTOM USER MODEL
# ============================================================

AUTH_USER_MODEL = 'recommender.UserProfile'


# ============================================================
# MIDDLEWARE
# ============================================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Serve static files in production
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ============================================================
# URL CONFIGURATION
# ============================================================

ROOT_URLCONF = 'elearning_system.urls'


# ============================================================
# TEMPLATES
# ============================================================

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


# ============================================================
# WSGI
# ============================================================

WSGI_APPLICATION = 'elearning_system.wsgi.application'


# ============================================================
# DATABASE
# ============================================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# ============================================================
# PASSWORD VALIDATION
# ============================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'UserAttributeSimilarityValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'MinimumLengthValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'CommonPasswordValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'NumericPasswordValidator'
        ),
    },
]


# ============================================================
# INTERNATIONALIZATION
# ============================================================

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# ============================================================
# STATIC FILES
# ============================================================

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# WhiteNoise compressed static files storage for production
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# ============================================================
# DEFAULT PRIMARY KEY
# ============================================================

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
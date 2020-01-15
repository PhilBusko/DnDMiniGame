"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
CFB-SITE SETTINGS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Build paths like this: os.path.join(settings.BASE_DIR, ...) ... must not start with /
#from django.conf import settings


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "app_proj/static/")

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'app_proj/media/')


SECRET_KEY = '1u2v$-x_ot(_q7ace#p9az1a59jquj(3hg@0(llo-kym@jc#$l'

DEBUG = True
#DEBUG = False
ALLOWED_HOSTS = ['*']


# APPLICATION

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'common',
    'dnd4e',
    'webscraper',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'app_proj.urls'

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

WSGI_APPLICATION = 'app_proj.wsgi.application'


# DATABASE

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation

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


# LOGGING
# CRITICAL, ERROR, WARNING, INFO and DEBUG

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    
    'formatters': {
        'simple': {	
            '()': 'common.utility.SimpleFmt'
        },
        'complete': {	
            '()': 'common.utility.CompleteFmt'
        },
    },
    
    'handlers': {
        'console': {
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'console_error': {
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'complete'
        },
        'logfile': {
            'class': 'logging.FileHandler',
            'filename': 'logfile.log',
            'formatter': 'complete'
        }
    },
    
    'loggers': {
        'progress': {
            'handlers': ['console'],
            'level': 'DEBUG',
         },
        'exception': {
            'handlers': ['console_error', 'logfile'],
            'level': 'WARNING',
        }
    }
}


# INTERNATIONALIZATION

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'dnd4e.models.models.context_background', 
            ],
        },
    },
]





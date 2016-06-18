# -*- coding: utf-8 -*-
"""
Test Settings
"""
from __future__ import unicode_literals

import django


APP_NAME = 'ebay_accounts'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
)

if django.VERSION[:2] < (1, 6):
    TEST_RUNNER = 'discover_runner.DiscoverRunner'
    INSTALLED_APPS += (
        'discover_runner',
    )

INSTALLED_APPS += (
    'ebay_accounts',
)
if django.VERSION[:2] < (1, 7):
    INSTALLED_APPS += (
        'south',
    )

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)
if django.VERSION[:2] > (1, 7):
    MIDDLEWARE_CLASSES += (
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    )

MIDDLEWARE_CLASSES += (
    'django.contrib.messages.middleware.MessageMiddleware',
)

if django.VERSION[:2] >= (1, 8):
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [
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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    },
}
SECRET_KEY = '^&*TESTING123^&*'
ROOT_URLCONF = APP_NAME + '.urls'
USE_TZ = True
LOGGING = {
    'version': 1,
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(module)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        }
    },
    'loggers': {
        'ebay_accounts': {
            'handlers': ['console'],
            'level': 'DEBUG',
        }
    }
}
EBAY_SANDBOX_DEVID = ''
EBAY_SANDBOX_APPID = ''
EBAY_SANDBOX_CERTID = ''
EBAY_SANDBOX_RU_NAME = 'TEST_SANDBOX_RU_NAME'
EBAY_PRODUCTION_DEVID = ''
EBAY_PRODUCTION_APPID = ''
EBAY_PRODUCTION_CERTID = ''
EBAY_PRODUCTION_RU_NAME = 'TEST_PRODUCTION_RU_NAME'

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 fileencoding=utf-8

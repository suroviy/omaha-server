# coding: utf8

import os

from django.utils import crypto
from .settings import *

DEBUG = False

ALLOWED_HOSTS = (os.environ.get('HOST_NAME'), '*')
SECRET_KEY = os.environ.get('SECRET_KEY') or crypto.get_random_string(50)

STATICFILES_STORAGE = 'omaha_server.s3utils.StaticS3Storage'
DEFAULT_FILE_STORAGE = 'omaha_server.s3utils.S3Storage'

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
S3_URL = 'http://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME

STATIC_URL = ''.join([S3_URL, 'static/'])
AWS_PRELOAD_METADATA = True
AWS_QUERYSTRING_AUTH = False
AWS_IS_GZIPPED = True


RAVEN_CONFIG = {
    'dsn': os.environ.get('RAVEN_DNS'),
    'name': HOST_NAME,
}

RAVEN_DSN_STACKTRACE = os.environ.get('RAVEN_DSN_STACKTRACE', RAVEN_CONFIG['dsn'])


SPLUNK_HOST = os.environ.get('SPLUNK_HOST')

INSTALLED_APPS = INSTALLED_APPS + (
    'raven.contrib.django.raven_compat',
)

CELERYD_HIJACK_ROOT_LOGGER = False

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': 'INFO',
        'handlers': ['sentry', 'console'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'splunk_format':{
            'format': 'level=%(levelname)s logger=%(name)s timestamp=%(asctime)s module=%(module)s process=%(process)d thread=%(thread)d message=%(message)s\n\r'
        }
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console', 'sentry'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}

if SPLUNK_HOST:
    LOGGING['handlers']['splunk'] = {
        'level': os.environ.get('SPLUNK_LOGGING_LEVEL', 'INFO'),
        'class': 'splunk_handler.SplunkHandler',
        'formatter': 'splunk_format',
        'host': SPLUNK_HOST,
        'port': os.environ.get('SPLUNK_MANAGEMENT_PORT', 8089),
        'username': os.environ.get('SPLUNK_USERNAME', 'admin'),
        'password': os.environ.get('SPLUNK_PASSWORD', 'changeme'),
        'hostname': HOST_NAME or 'Unknown',
        'index': 'main',
        'source': 'omaha',
        'sourcetype': 'omaha-server',
        'verify': False,
    }
    LOGGING['root']['handlers'].append('splunk')

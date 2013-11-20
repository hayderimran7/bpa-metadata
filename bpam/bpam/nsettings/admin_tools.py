from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

INSTALLED_APPS += ('debug_toolbar', )
INTERNAL_IPS = ('127.0.0.1',)

MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware', )

INSTALLED_APPS = (
    'bpam',
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.gis',
    'localflavor',
    'apps.geo',
    'apps.bpaauth',
    'apps.common',
    'apps.melanoma',
    'apps.gbr',
    #'apps.BASE',
    'apps.wheat_cultivars',
    'apps.wheat_pathogens',
    'south',
    'tinymce',
    'bootstrap3',
    'tastypie',
    'debug_toolbar',
)
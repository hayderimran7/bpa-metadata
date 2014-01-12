# Django settings for bpametadata project.

import os
from unipath import Path
from django.core.exceptions import ImproperlyConfigured

BPA_VERSION = '1.0.4'

WEBAPP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROJECT_DIR = Path(__file__).ancestor(1)

MEDIA_ROOT = PROJECT_DIR.child("media")

STATIC_ROOT = os.path.join(WEBAPP_ROOT, 'static')

#STATICFILES_DIRS = (
#    PROJECT_DIR.child("static"),
#)

TEMPLATE_DIRS = (
    PROJECT_DIR.child('bpam.templates'),
)

DEBUG = True

TEMPLATE_DEBUG = DEBUG

ADMINS = (
# ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dev_bpam',
        'USER': 'bpam',
        'PASSWORD': 'bpam',
        'HOST': '',
        'PORT': '',
    }
}


AUTH_USER_MODEL = 'bpaauth.BPAUser'

SUIT_CONFIG = {
    'ADMIN_NAME': 'Bioplatforms Australia Metadata',
    'MENU': (
        {'app': 'common', 'label': 'Common', },
        {'app': 'melanoma', 'label': 'Melanoma', },
        {'app': 'gbr', 'label': 'Great Barrier Reef', },
        {'app': 'wheat_pathogens', 'label': 'Wheat Pathogens', },
        {'app': 'wheat_cultivars', 'label': 'Wheat Cultivars', },
        {'app': 'base', 'label': 'BASE', },
        '-',
        {'app': 'bpaauth', 'label': 'Authorization', 'icon': 'icon-lock', 'models': ('bpaauth.BPAUser', 'auth.group')},
    )
}



# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Australia/Perth'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
# STATIC_URL = '{0}/static/'.format(os.environ.get("SCRIPT_NAME", ""))
STATIC_URL = '/bpa-metadata/static/'

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '2(3)7aip&90=vw@(qwfzvi@zyw8ll+ekq0_mp4rfd-7hn14mmk'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.static',
)

ROOT_URLCONF = 'bpam.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'bpam.wsgi.application'

INSTALLED_APPS = (
    'bpam',
    'suit',
    'crispy_forms',
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
    'apps.BASE',
    'apps.wheat_pathogens',
    'apps.wheat_cultivars',
    'apps.melanoma',
    'apps.gbr',
    'south',
    'tinymce',
    'bootstrap3',
    'tastypie',
    # 'lettuce.django',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


def get_env_variable(var_name):
    """ Get the environment variable or return exception """
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the %s environment variable" % var_name
        raise ImproperlyConfigured(error_msg)

BPA_BASE_URL = 'https://downloads.bioplatforms.com/data/'

try:
    print "Attempting to import default settings as appsettings.bpam"
    from appsettings.bpam import *
    print "Successfully imported appsettings.bpam"
except ImportError, e:
    print "Failed to import appsettings.bpam"

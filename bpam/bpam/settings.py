# -*- coding: utf-8 -*-
# Django settings for bpa metadata project.

import os
import sys

from unipath import Path
from ccg_django_utils.conf import EnvConfig
from bpam import VERSION


env = EnvConfig()

BPA_VERSION = VERSION
# see ccg_django_utils.webhelpers
BASE_URL_PATH = os.environ.get("SCRIPT_NAME", "")
CCG_INSTALL_ROOT = os.path.dirname(os.path.realpath(__file__))

PROJECT_DIR = Path(__file__).ancestor(1)

CCG_WRITABLE_DIRECTORY = env.get("writable_directory", os.path.join(CCG_INSTALL_ROOT, "scratch"))
PROJECT_NAME = os.path.basename(CCG_INSTALL_ROOT)

TEMPLATE_DIRS = (
    PROJECT_DIR.child('bpam.templates'),
)

# Make this unique, and don't share it with anybody.
# see: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env.get("secret_key", "change-it")

# Default SSL on and forced, turn off if necessary
SSL_ENABLED = env.get("production", False)
SSL_FORCE = env.get("production", False)

# Debug on by default
DEBUG = env.get("debug", True)

TEMPLATE_DEBUG = DEBUG

# Default all email to ADMINS and MANAGERS to root@localhost.
# Puppet redirects this to something appropriate depend on the environment.
# see: https://docs.djangoproject.com/en/1.6/ref/settings/#admins
# see: https://docs.djangoproject.com/en/1.6/ref/settings/#managers
ADMINS = [
    ("alert", env.get("alert_email", "root@localhost"))
]
MANAGERS = ADMINS


if env.get("ENABLE_EMAIL", False):
    print('Enabling Email')
    # email settings for sending email error alerts etc
    # See: https://docs.djangoproject.com/en/1.6/ref/settings/#email-host
    EMAIL_HOST = env.get("email_host", "")
    # See: https://docs.djangoproject.com/en/1.6/ref/settings/#email-port
    EMAIL_PORT = env.get("email_port", 25)

    # See: https://docs.djangoproject.com/en/1.6/ref/settings/#email-host-user
    EMAIL_HOST_USER = env.get("email_host_user", "")
    # See: https://docs.djangoproject.com/en/1.6/ref/settings/#email-host-password
    EMAIL_HOST_PASSWORD = env.get("email_host_password", "")

    # See: https://docs.djangoproject.com/en/1.6/ref/settings/#email-use-tls
    EMAIL_USE_TLS = env.get("email_use_tls", False)

    # see: https://docs.djangoproject.com/en/1.6/ref/settings/#email-subject-prefix
    EMAIL_APP_NAME = "BPA Metadata "
    EMAIL_SUBJECT_PREFIX = env.get("email_subject_prefix", "PROD " if env.get("production", False) else "DEV ")

    # See: https://docs.djangoproject.com/en/1.6/ref/settings/#email-backend
    if EMAIL_HOST:
        EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    elif DEBUG:
        EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    else:
        EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
        EMAIL_FILE_PATH = os.path.join(CCG_WRITABLE_DIRECTORY, "mail")
        if not os.path.exists(EMAIL_FILE_PATH):
            from distutils.dir_util import mkpath

            mkpath(EMAIL_FILE_PATH)

    # See: https://docs.djangoproject.com/en/1.6/ref/settings/#server-email
    SERVER_EMAIL = env.get("server_email", "bpam@ccgapps.com.au")
    RETURN_EMAIL = env.get("return_email", "noreply@ccgapps.com.au")
    # email address to receive datasync client log notifications
    LOGS_TO_EMAIL = env.get("logs_to_email", "log_email@ccgapps.com.au")
    # email address to receive datasync key upload notifications
    KEYS_TO_EMAIL = env.get("keys_to_email", "key_email@ccgapps.com.au")
    # email address to receive registration requests
    REGISTRATION_TO_EMAIL = env.get("registration_to_email", "reg_email@ccgapps.com.au")


# See: https://docs.djangoproject.com/en/1.5/releases/1.5/#allowed-hosts-required-in-production
ALLOWED_HOSTS = env.getlist("allowed_hosts", ["*"])

DATABASES = {
    'default': {
        'ENGINE': env.get_db_engine("dbtype", "pgsql"),
        'NAME': env.get("dbname", "bpam"),
        'USER': env.get("dbuser", "bpam"),
        'PASSWORD': env.get("dbpass", "bpam"),
        'HOST': env.get("dbserver", ""),
        'PORT': env.get("dbport", ""),
    }
}

# http://www.django-rest-framework.org/
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'PAGINATE_BY': 10
}


# Default cookie settings
# see: https://docs.djangoproject.com/en/1.4/ref/settings/#session-cookie-age and following
# see: https://docs.djangoproject.com/en/1.4/ref/settings/#csrf-cookie-name and following
SESSION_COOKIE_AGE = env.get("session_cookie_age", 60 * 60)
SESSION_COOKIE_PATH = '{0}/'.format(BASE_URL_PATH)
SESSION_SAVE_EVERY_REQUEST = env.get("session_save_every_request", True)
SESSION_COOKIE_HTTPONLY = env.get("session_cookie_httponly", True)
SESSION_COOKIE_SECURE = env.get("session_cookie_secure", False)
SESSION_COOKIE_NAME = env.get("session_cookie_name", "bpam_{0}".format(BASE_URL_PATH.replace("/", "")))
SESSION_COOKIE_DOMAIN = env.get("session_cookie_domain", "") or None
CSRF_COOKIE_NAME = env.get("csrf_cookie_name", "csrf_{0}".format(SESSION_COOKIE_NAME))
CSRF_COOKIE_DOMAIN = env.get("csrf_cookie_domain", "") or SESSION_COOKIE_DOMAIN
CSRF_COOKIE_PATH = env.get("csrf_cookie_path", SESSION_COOKIE_PATH)
CSRF_COOKIE_SECURE = env.get("csrf_cookie_secure", False)

# Default date input formats, may be overridden
# see: https://docs.djangoproject.com/en/1.4/ref/settings/#date-input-formats
TIME_ZONE = env.get("time_zone", 'Australia/Perth')
LANGUAGE_CODE = env.get("language_code", 'en-us')
USE_I18N = env.get("use_i18n", True)
USE_L10N = False
DATE_INPUT_FORMATS = ('%Y-%m-%d', '%d/%m/%Y', '%d/%m/%y', '%d %m %Y', '%d %m %y', '%d %b %Y')
DATE_FORMAT = "d-m-Y"
SHORT_DATE_FORMAT = "d/m/Y"

AUTH_USER_MODEL = 'bpaauth.BPAUser'

# used by maps when plotting sample location
LEAFLET_CONFIG = {
    'DEFAULT_CENTER': (-25.27, 133.775),
    'DEFAULT_ZOOM': 4,
    'ATTRIBUTION_PREFIX': '',
    'TILES': 'http://otile1.mqcdn.com/tiles/1.0.0/map/{z}/{x}/{y}.png',
}

SUIT_CONFIG = {
    'SHOW_REQUIRED_ASTERISK': True,
    'ADMIN_NAME': 'Bioplatforms Australia Metadata',
    'MENU': (
        {'app': 'common', 'label': 'Common', },
        {'app': 'melanoma', 'label': 'Melanoma',
         'models': ('melanomasample',
                    'melanomasequencefile',
                    'array',
                    'melanomaprotocol',
                    'melanomarun',
                    'tumorstage')},
        {'app': 'gbr', 'label': 'Great Barrier Reef',
         'models': ('gbrsample',
                    'gbrsequencefile',
                    'collectionsite',
                    'collectionevent',
                    'gbrrun',
                    'gbrprotocol',)},
        '-',
        # Wheat Pathogens Genome
        {'app': 'wheat_pathogens', 'label': 'Wheat Pathogens Genome',
         'models': ('pathogensample',
                    'pathogensequencefile',
                    'pathogenrun',
                    'pathogenprotocol')},
        # Wheat Pathogens Transcript
        {'app': 'wheat_pathogens_transcript', 'label': 'Wheat Pathogens Transcript',
         'models': ('wheatpathogentranscriptsample',
                    'wheatpathogentranscriptsequencefile',
                    'wheatpathogentranscriptrun',
                    'wheatpathogentranscriptprotocol')},
        # Wheat Cultivars
        {'app': 'wheat_cultivars', 'label': 'Wheat Cultivars',
         'models': ('cultivarsample',
                    'cultivarsequencefile',
                    'cultivarrun',
                    'cultivarprotocol')},
        '-',
        # Base
        {'app': 'base_metagenomics', 'label': 'BASE Metagenomics',
         'models': ('metagenomicssample',
                    'metagenomicssequencefile',
                    'metagenomicsrun')},
        {'app': 'base_amplicon', 'label': 'BASE Amplicons',
         'models': ('ampliconsequencingmetadata',
                    'ampliconsequencefile',)
        },
        {'app': 'base_vocabulary', 'label': 'BASE Vocabulary', },
        {'app': 'base_contextual', 'label': 'BASE Contextual', },
        {'app': 'base_otu', 'label': 'BASE OTU', },
        {'app': 'base_454', 'label': 'BASE 454', },
        '-',
        {'app': 'bpaauth', 'label': 'Users', 'icon': 'icon-user', 'models': ('bpaauth.bpauser', 'auth.group')},
        # {'label': 'Users', 'url': 'bpaauth.bpauser', 'icon': 'icon-user'},
    )
}

SITE_ID = 1

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_ROOT = env.get('media_root', PROJECT_DIR.child("media"))
MEDIA_URL = ''

# These may be overridden, but it would be nice to stick to this convention
# see: https://docs.djangoproject.com/en/1.4/ref/settings/#static-url
STATIC_ROOT = env.get('static_root', os.path.join(CCG_INSTALL_ROOT, 'static'))
STATIC_URL = '{0}/static/'.format(BASE_URL_PATH)


# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.,clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.static',
)

ROOT_URLCONF = 'bpam.urls'

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
    # 'django.contrib.gis',
    'localflavor',
    'mptt',
    'apps.bpaauth',
    'apps.common',
    # base suit
    'apps.base',
    'apps.base_metagenomics',
    'apps.base_vocabulary',
    'apps.base_contextual',
    'apps.base_amplicon',
    'apps.base_otu',
    'apps.base_454',
    # wheat suit
    'apps.wheat_pathogens',
    'apps.wheat_pathogens_transcript',
    'apps.wheat_cultivars',
    'apps.melanoma',
    'apps.gbr',
    'tinymce',
    'bootstrap3',
    'rest_framework',
    'explorer',
    'leaflet',
)

# Log directory created and enforced by puppet
CCG_LOG_DIRECTORY = env.get('log_directory', os.path.join(CCG_INSTALL_ROOT, "log"))
try:
    if not os.path.exists(CCG_LOG_DIRECTORY):
        os.mkdir(CCG_LOG_DIRECTORY)
except:
    pass
os.path.exists(CCG_LOG_DIRECTORY), "No log directory, please create one: %s" % CCG_LOG_DIRECTORY

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
        'logfile': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(CCG_LOG_DIRECTORY, "ingest-logfile"),
            'maxBytes': 50000,
            'backupCount': 2,
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'rainbow': {
            'level': 'DEBUG',
            'class': 'rainbow_logging_handler.RainbowLoggingHandler',
            'stream': sys.stderr}
    },
    'loggers': {
        # noisy backed, set to DEBUG if something seems wrong
        'django.db.backends': {
            'handlers': ['rainbow'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        '': {
            'handlers': ['rainbow']
        }
    }
}

if env.get("DEBUG_TOOLBAR", False):
    INSTALLED_APPS += ('debug_toolbar', )
    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware', )
    INTERNAL_IPS = ('127.0.0.1', '172.16.2.189',)  # explicitly set this for your environment

# downloads URL
BPA_BASE_URL = 'https://downloads.bioplatforms.com/'
DEFAULT_PAGINATION = 50

# This honours the X-Forwarded-Host header set by our nginx frontend when
# constructing redirect URLS.
# see: https://docs.djangoproject.com/en/1.4/ref/settings/#use-x-forwarded-host
USE_X_FORWARDED_HOST = env.get("use_x_forwarded_host", True)

if env.get("memcache", ""):
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': env.getlist("memcache", []),
            'KEY_PREFIX': env.get("key_prefix", "bpam"),
            #'KEYSPACE': "%s-prod" % PROJECT_NAME,
        }
    }

    SESSION_ENGINE = "django.contrib.sessions.backends.cache"
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
            'LOCATION': 'bpam_cache',
            'TIMEOUT': 3600,
            'MAX_ENTRIES': 600
        }
    }

    SESSION_ENGINE = 'django.contrib.sessions.backends.file'
    SESSION_FILE_PATH = CCG_WRITABLE_DIRECTORY

CHMOD_USER = env.get("repo_user", "apache")
CHMOD_GROUP = env.get("repo_group", "apache")

REPO_FILES_ROOT = env.get("repo_files_root", os.path.join(CCG_WRITABLE_DIRECTORY, 'files'))
QUOTE_FILES_ROOT = env.get("quote_files_root", os.path.join(CCG_WRITABLE_DIRECTORY, 'quotes'))



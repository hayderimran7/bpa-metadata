# -*- coding: utf-8 -*-/MAIL
# Django settings for bpa metadata project.

import os

from ccg_django_utils.conf import EnvConfig

env = EnvConfig()

VERSION = env.get("bpa_version", os.environ.get("GIT_TAG", "UNKNOWN_VERSION"))
BPA_VERSION = VERSION

SCRIPT_NAME = env.get("script_name", os.environ.get("HTTP_SCRIPT_NAME", ""))
FORCE_SCRIPT_NAME = env.get("force_script_name", "") or SCRIPT_NAME or None

WEBAPP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# a directory that will be writable by the webserver, for storing various files...
WRITABLE_DIRECTORY = env.get("writable_directory", "/tmp")

TEMPLATE_DIRS = (
    os.path.join(WEBAPP_ROOT, 'bpam', 'templates'),
)

SECRET_KEY = env.get("secret_key", "change-it")

# Default SSL on and forced, turn off if necessary
PRODUCTION = env.get("production", False)
SSL_ENABLED = PRODUCTION
SSL_FORCE = PRODUCTION

DEBUG = env.get("debug", not PRODUCTION)
TEMPLATE_DEBUG = DEBUG

# django-secure
SECURE_SSL_REDIRECT = env.get("secure_ssl_redirect", PRODUCTION)
SECURE_FRAME_DENY = env.get("secure_frame_deny", PRODUCTION)
SECURE_CONTENT_TYPE_NOSNIFF = env.get("secure_content_type_nosniff", PRODUCTION)
SECURE_BROWSER_XSS_FILTER = env.get("secure_browser_xss_filter", PRODUCTION)
SECURE_HSTS_SECONDS = env.get("secure_hsts_seconds", 10)
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.get("secure_hsts_include_subdomains", PRODUCTION)

ADMINS = [
    ("alert", env.get("alert_email", "root@localhost"))
]
MANAGERS = ADMINS

# mailgun email
DEFAULT_FROM_EMAIL = env.get('DJANGO_DEFAULT_FROM_EMAIL', 'No Reply <no-reply@mg.ccgapps.com.au>')
# default to mailgun, but if the API key is not set, fall back to console
EMAIL_BACKEND = env.get('DJANGO_EMAIL_BACKEND', 'django_mailgun.MailgunBackend')
MAILGUN_ACCESS_KEY = env.get('DJANGO_MAILGUN_API_KEY', '')
MAILGUN_SERVER_NAME = env.get('DJANGO_MAILGUN_SERVER_NAME', '')
EMAIL_SUBJECT_PREFIX = env.get("DJANGO_EMAIL_SUBJECT_PREFIX", '[BPA Metadata] ')
SERVER_EMAIL = env.get('DJANGO_SERVER_EMAIL', DEFAULT_FROM_EMAIL)

# list of emails to send BASE access requests to
BASE_REQUEST_LIST = env.getlist('BASE_REQUEST_LIST', ['bpa_base_request@mg.ccgapps.com.au'])

ALLOWED_HOSTS = env.getlist("allowed_hosts", ["*"])

DATABASES = {
    'default': {
        'ENGINE': env.get_db_engine("dbtype", "pgsql"),
        'NAME': env.get("dbname", "webapp"),
        'USER': env.get("dbuser", "webapp"),
        'PASSWORD': env.get("dbpass", "webapp"),
        'HOST': env.get("dbserver", ""),
        'PORT': env.get("dbport", ""),
    }
}

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'PAGINATE_BY': 10
}

SESSION_COOKIE_AGE = env.get("session_cookie_age", 60 * 60)
SESSION_COOKIE_PATH = '{0}/'.format(SCRIPT_NAME)
SESSION_SAVE_EVERY_REQUEST = env.get("session_save_every_request", True)
SESSION_COOKIE_HTTPONLY = SESSION_COOKIE_HTTPONLY = env.get("session_cookie_httponly", True)
SESSION_COOKIE_SECURE = env.get("session_cookie_secure", PRODUCTION)
SESSION_COOKIE_NAME = env.get("session_cookie_name", "ccg_{0}".format(SCRIPT_NAME.replace("/", "")))
SESSION_COOKIE_DOMAIN = env.get("session_cookie_domain", "") or None
CSRF_COOKIE_NAME = env.get("csrf_cookie_name", "csrf_{0}".format(SESSION_COOKIE_NAME))
CSRF_COOKIE_DOMAIN = env.get("csrf_cookie_domain", "") or SESSION_COOKIE_DOMAIN
CSRF_COOKIE_PATH = env.get("csrf_cookie_path", SESSION_COOKIE_PATH)
CSRF_COOKIE_SECURE = env.get("csrf_cookie_secure", PRODUCTION)

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
    'TILES': [
        ('MapQuest Open Aerial',
         'http://otile1.mqcdn.com/tiles/1.0.0/map/{z}/{x}/{y}.png',
         {'attribution': 'Portions Courtesy NASA/JPL-Caltech and U.S. Depart. of Agriculture, Farm Service Agency'},
         ),
        ('ESRI',
         'http://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
         {'attribution': '&copy; i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'},
         ),
        ('OSM B&W',
         'http://{s}.www.toolserver.org/tiles/bw-mapnik/{z}/{x}/{y}.png',
         {'attribution': '&copy; <a href="http://openstreetmap.org">OpenStreetMap</a> Contributers'},
         ),
        ('Thunderforest',
         'http://{s}.tile.thunderforest.com/landscape/{z}/{x}/{y}.png',
         {'attribution': '&copy; <a href="http://openstreetmap.org">OpenStreetMap</a> Contributers'},
         ),
    ],
    'MINIMAP': True,
    'RESET_VIEW': False
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
        # GBR
        {'app': 'gbr', 'label': 'Great Barrier Reef',
         'models': ('gbrsample',
                    'gbrsequencefile',
                    'collectionsite',
                    'collectionevent',
                    'gbrrun',
                    'gbrprotocol',)},
        '-',
        # barcode
        {'app': 'barcode', 'label': 'Barcode',
         'models': ('sheet',)},
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
                    'ampliconsequencefile', )},
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
MEDIA_ROOT = env.get('media_root', os.path.join(WEBAPP_ROOT, 'static', 'media'))
MEDIA_URL = ''

# These may be overridden, but it would be nice to stick to this convention
STATIC_ROOT = env.get('static_root', os.path.join(WEBAPP_ROOT, 'static'))
STATIC_URL = '{0}/static/'.format(SCRIPT_NAME)


# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'admin_tools.template_loaders.Loader',
)

MIDDLEWARE_CLASSES = (
    'djangosecure.middleware.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    # 'django.middleware.doc.XViewMiddleware',
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
    'apps.gbr_amplicon',
    'apps.barcode',
    'tinymce',
    'bootstrap3',
    'django_bootstrap_breadcrumbs',
    'rest_framework',
    'explorer',
    'leaflet',
    'djangosecure',
)


# #
# # LOGGING
# #
LOG_DIRECTORY = env.get('log_directory', os.path.join(WEBAPP_ROOT, "log"))
try:
    if not os.path.exists(LOG_DIRECTORY):
        os.mkdir(LOG_DIRECTORY)
except:
    pass
os.path.exists(LOG_DIRECTORY), "No log directory, please create one: %s" % LOG_DIRECTORY

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': 'bpam [%(levelname)s:%(asctime)s:%(filename)s:%(lineno)s:%(funcName)s] %(message)s'
        },
        'db': {
            'format': 'bpam [%(duration)s:%(sql)s:%(params)s] %(message)s'
        },
        'simple': {
            'format': 'bpam %(levelname)s %(message)s'
        },
    },
    'filters': {
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'errorfile': {
            'level': 'ERROR',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(LOG_DIRECTORY, 'error.log'),
            'when': 'midnight',
            'formatter': 'verbose'
        },
        'registryfile': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(LOG_DIRECTORY, 'registry.log'),
            'when': 'midnight',
            'formatter': 'verbose'
        },
        'db_logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(LOG_DIRECTORY, 'registry_db.log'),
            'when': 'midnight',
            'formatter': 'db'
        },
         'access_logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(LOG_DIRECTORY, 'access.log'),
            'when': 'midnight',
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': [],
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'verbose',
            'include_html': True
        }
    },
    'root': {
        'handlers': ['console', 'errorfile', 'mail_admins'],
        'level': 'ERROR',
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': False,
            'level': 'INFO',
        },
        'registry_log': {
            'handlers': ['registryfile', 'console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        # The following logger used by django useraudit
        'django.security': {
            'handlers': ['access_logfile', 'console'],
            'level': 'DEBUG',
            'propagate': False,
        }
    }
}


if env.get("DEBUG_TOOLBAR", False):
    INSTALLED_APPS += ('debug_toolbar', )
    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware', )
    INTERNAL_IPS = ('127.0.0.1', '172.16.2.189',)  # explicitly set this for your environment

# downloads URL
DEFAULT_PAGINATION = 50

# This honours the X-Forwarded-Host header set by our nginx frontend when
# constructing redirect URLS.
USE_X_FORWARDED_HOST = env.get("use_x_forwarded_host", True)

if env.get("memcache", ""):
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': env.getlist("memcache", []),
            'KEY_PREFIX': env.get("key_prefix", "bpam"),
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
    SESSION_FILE_PATH = WRITABLE_DIRECTORY

CHMOD_USER = env.get("repo_user", "apache")
CHMOD_GROUP = env.get("repo_group", "apache")

# this is here to placate the new system check framework, its also set in testsettings,
# where it belongs
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# ingest all
DOWNLOADS_CHECKER_USER = env.get('downloads_checker_user', 'downloads_checker')
DOWNLOADS_CHECKER_PASS = env.get('downloads_checker_pass', 'ch3ck3r')
DOWNLOADS_CHECKER_SLEEP = env.get('downloads_checker_sleep', 0.0)

CRISPY_TEMPLATE_PACK = 'bootstrap3'



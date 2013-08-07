from .base import *

######################################################################
# need to remove these once settings file locations are sorted out
PROJECT_DIR = Path(__file__).ancestor(2)
MEDIA_ROOT = PROJECT_DIR.child("media")
STATIC_ROOT = PROJECT_DIR.child("static")
STATICFILES_DIRS = ()
TEMPLATE_DIRS = (PROJECT_DIR.child("templates"),)
######################################################################

# This path depends on centos/bpa-metadata.ccg (the apache config
# file). This should perhaps be configured in puppet_data.
STATIC_URL = '/bpa-metadata/static/'


CCG_INSTALL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CCG_LOG_DIRECTORY = os.path.join(CCG_INSTALL_ROOT, "log")


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': 'bpam [%(name)s:%(levelname)s:%(asctime)s:%(filename)s:%(lineno)s:%(funcName)s] %(message)s'
        },
        'db': {
            'format': 'bpam [%(name)s:%(duration)s:%(sql)s:%(params)s] %(message)s'
        },
    },
    'handlers': {
        'file':{
            'level':'DEBUG',
            'class':'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(CCG_LOG_DIRECTORY, 'bpam.log'),
            'when':'midnight',
            'formatter': 'verbose'
        },
        'db_logfile':{
            'level':'DEBUG',
            'class':'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(CCG_LOG_DIRECTORY, 'db.log'),
            'when':'midnight',
            'formatter': 'db'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django': {
            'handlers':['file'],
            'propagate': True,
            'level':'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['db_logfile', 'mail_admins'],
            'level': 'CRITICAL',
            'propagate': False,
        },
        'bpam': {
            'handlers': ['file'],
            'propagate': True,
            'level': 'DEBUG',
        },
    }
}


# work around django security for now
ALLOWED_HOSTS = ["*"]

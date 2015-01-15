from settings import *

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-#

# Default debug mode is off, turn on for trouble-shooting
# DEBUG = False

# Default SSL on and forced, turn off if necessary
# SSL_ENABLED = True
# SSL_FORCE = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-#

TEST_RUNNER = "django.test.runner.DiscoverRunner"

DEBUG = True
TEMPLATE_DEBUG = DEBUG

if 'debug_toolbar' not in INSTALLED_APPS:
    INSTALLED_APPS += ('debug_toolbar',)
INTERNAL_IPS = ('127.0.0.1',)

MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware', )

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    },
}
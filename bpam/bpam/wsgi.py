"""
WSGI config for bpametadata project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os
import os.path
import sys

# snippet to enable the virtualenv if installed as rpm
activate_this=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bin', 'activate_this.py')
if os.path.exists(activate_this):
    exec(compile(open(activate_this).read(), activate_this, 'exec'), dict(__file__=activate_this))
del activate_this

SITE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(SITE_ROOT)

# Allow appsettings to be imported
sys.path.insert(0, "/etc/ccgapps")

# setup the settings module for the WSGI app
os.environ['DJANGO_SETTINGS_MODULE'] = 'defaultsettings.bpam'
os.environ['PROJECT_DIRECTORY'] = SITE_ROOT
os.environ['WEBAPP_ROOT'] = SITE_ROOT
os.environ['PYTHON_EGG_CACHE'] = '/tmp/.python-eggs'

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
_application = get_wsgi_application()

def application(environ, start_response):
    # Before entering the django app, transfer the SCRIPT_NAME http
    # header into an environment variable so settings can pick it up.
    mount_point = environ.get("HTTP_SCRIPT_NAME", environ.get("SCRIPT_NAME", None))
    if mount_point:
        os.environ["SCRIPT_NAME"] = mount_point
    return _application(environ, start_response)

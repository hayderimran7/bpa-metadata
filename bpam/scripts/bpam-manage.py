#!/usr/bin/env python
import os
import sys
import pwd

USER = "apache"

try:
    (uid, gid, gecos, homedir) = pwd.getpwnam(USER)[2:6]
    os.setgid(gid)
    os.setuid(uid)
    os.environ["HOME"] = homedir
except OSError as e:
    sys.stderr.write("warning: Couldn't switch to the %s user: %s\n" % (USER, e))

if __name__ == "__main__":
    webapp_name = "bpa-metadata"
    os.environ.setdefault('CCG_WEBAPPS_PREFIX', '/usr/local/webapps')
    webapp_root = os.path.join(os.environ['CCG_WEBAPPS_PREFIX'], webapp_name)

    # Allow appsettings to be imported
    sys.path.insert(0, "/etc/ccgapps")

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'defaultsettings.bpam')
    os.environ.setdefault('PROJECT_DIRECTORY', webapp_root)
    os.environ.setdefault('WEBAPP_ROOT', webapp_root)
    os.environ.setdefault('PYTHON_EGG_CACHE', '/tmp/.python-eggs')

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

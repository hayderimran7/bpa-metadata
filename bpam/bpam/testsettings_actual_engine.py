# this settings runs the tests against the real db engine

from testsettings import *  # nopep8

DATABASES = {
    'default': {
        'ENGINE': env.get_db_engine("dbtype", "pgsql"),
        'NAME': 'test-bpam',
        'USER': 'bpam',
        'PASSWORD': 'test-bpam',
        'HOST': '',
        'PORT': '',
    }
}

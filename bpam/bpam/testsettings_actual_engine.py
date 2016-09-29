# this settings runs the tests against the real db engine

from testsettings import *  # noqa

DATABASES = {
    'default': {
        'ENGINE': env.get_db_engine("dbtype", "pgsql"),  # noqa
        'NAME': 'test-bpam',
        'USER': 'bpam',
        'PASSWORD': 'test-bpam',
        'HOST': '',
        'PORT': '',
    }
}

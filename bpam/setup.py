import os.path

from setuptools import setup, find_packages


def get_data_files():
    """
    Dictionary of data files
    """
    current_dir = os.getcwd()
    data_files = {}
    for package in packages:
        data_files[package] = []
        os.chdir(os.path.join(package))
        for data_dir in ('templates', 'static', 'migrations', 'fixtures', 'features', 'templatetags', 'management'):
            data_files[package].extend(
                [os.path.join(subdir, f) for (subdir, dirs, files) in os.walk(data_dir) for f in files])
        os.chdir(current_dir)
    return data_files

INSTALL_ONLY_DEPENDENCIES = 'INSTALL_ONLY_DEPENDENCIES' in os.environ

if 'INSTALL_ONLY_DEPENDENCIES' in os.environ:
    packages = []
    package_data = {}
    package_scripts = []
else:
    packages = [p.replace(".", "/") for p in sorted(find_packages())]
    package_scripts = ["manage.py"]
    package_data = get_data_files()

install_requires = [
    'Django==1.7.6',
    'Django-suit',
    'django-crispy-forms',
    'python-memcached>=1.53,<2.0',
    'Unipath>=1.0,<2.0',
    'boto>=2.15.0',
    'python-dateutil==1.5',  # 2.0 for Python >= 3
    'django-admin-tools>=0.5.1',
    'django-extensions==1.3.11',  # 1.3.11 doesn't hide errors
    'django-localflavor>=1.0',
    'django-tinymce>=1.5.2',
    'django-localflavor',
    'feedparser>=5.1.3',
    'pytz>=2013.7',
    'sqlparse>=0.1.9,<1.0',
    'django-bootstrap3>=3.0',
    'django_bootstrap_breadcrumbs>=0.7.1',
    'django-tastypie==0.10.0',
    'xlrd>=0.9.2',
    'xlwt>=0.7.5',
    'requests>=2.4.0',
    'django_compressor>=1.3',
    'mimeparse>=0.1.3,<1.0',
    'rainbow_logging_handler',
    'django-sql-explorer==0.6',
    'django-mptt>=0.5.5',
    'ccg-extras',
    'django-leaflet',
    'pycontracts',
    'ccg-django-utils',
    'django-debug-toolbar',
    'beautifulsoup4',
    'djangorestframework==3.1.0',
    'markdown',
    'django-filter',
    'lettuce_webdriver',
    # https://bitbucket.org/gutworth/six/issue/51/
    'six>=1.9.0',
    'psycopg2==2.5.5',
    # docker
    'uwsgi==2.0.8',
    'uwsgitop',
    'pyinotify==0.9.4',
    'Werkzeug',
    'psycopg2==2.5.4',
    'model-mommy',
    'django-secure',
    'django-queryset-csv'
]

dev_requires = [
    'psycopg2>=2.5.0,<2.6.0',
    'flake8',
    'Werkzeug',
    'coverage',
    'django-discover-runner',
    'model-mommy',
    'tendo',
    'docutils',
    'pygments',
    'docopt',
    'jinja2',
]

tests_require = [
    'django-nose>=1.2',
    'nose>=1.2.1',
    'dingus',
]

downloads_requires = [
    'Jinja2>=2.7.1',
]

# TODO clean up this mess
dependency_links = [
    'https://bitbucket.org/ccgmurdoch/django-userlog/downloads/django_userlog-0.1.tar.gz',
    'https://bitbucket.org/ccgmurdoch/ccg-django-utils/downloads/ccg-django-utils-0.2.1.tar.gz',
    'https://bitbucket.org/ccgmurdoch/ccg-django-extras/downloads/ccg-extras-0.1.9.tar.gz',
    'https://bitbucket.org/izi/django-admin-tools/downloads/django-admin-tools-0.5.1.tar.gz#md5=132e62fa1d5a0d933c4c13324249381c'
    'https://argparse.googlecode.com/files/argparse-1.2.1.tar.gz',
    'https://alastairs-place.net/projects/netifaces/netifaces-0.8.tar.gz',
]

setup(
    name='bpam',
    version='1.4.2',
    description="BPA Metadata Management",
    author='Centre for Comparative Genomics',
    author_email='web@ccg.murdoch.edu.au',
    packages=packages,
    package_data=package_data,
    include_package_data=True,
    install_requires=install_requires,
    dependency_links=dependency_links,
    extras_require={
        'tests': tests_require,
        'dev': dev_requires,
        'downloads': downloads_requires
    },
    zip_safe=False,
    scripts=package_scripts,
)

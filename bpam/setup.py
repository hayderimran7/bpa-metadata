import os.path
from pprint import pprint

from setuptools import setup, find_packages

packages = [p.replace(".", "/") for p in sorted(find_packages())]


def get_version():
    """
    The VERSION file in project root sets the version
    """
    project_dir = os.path.join(os.path.dirname(__file__), '../')
    with open(os.path.join(project_dir, 'VERSION'), 'r') as version_file:
        return version_file.readline().strip()


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

setup(
    name='bpam',
    version=get_version(),
    description="BPA Metadata Management",
    author='Centre for Comparative Genomics',
    author_email='web@ccg.murdoch.edu.au',
    license="gpl3",
    packages=packages,
    package_data=get_data_files(),
    include_package_data=True,
    install_requires=[
        'Django==1.5.4',
        'Unipath==1.0',
        'South==0.8.2',
        'pygraphviz==1.2',
        'django-extensions==1.2.5',
        'django-admin-tools==0.5.1',
        'feedparser==5.1.3',
        'django-localflavor==1.0',
        'django-tinymce==1.5.1',
        'django-tastypie==0.10.0',
        'django-bootstrap3==0.0.7',
        'mimeparse==0.1.3',
        'requests==1.2.3',
        'ccg-extras==0.1.6',
        'python-memcached==1.48',
        'docutils==0.11',
        'xlrd==0.9.2',
        'dateutils==0.6.6'
    ],
    dependency_links=[
        "http://bitbucket.org/izi/django-admin-tools/downloads/django-admin-tools-0.5.1.tar.gz",
        "https://bitbucket.org/ccgmurdoch/ccg-django-extras/downloads/ccg-extras-0.1.6.tar.gz",
    ],
    zip_safe=False,
)

import setuptools
from setuptools import setup, find_packages
import os.path
import re
from pip.req import parse_requirements

setup(
    name='bpam',
    version='1.0',
    description="BPA Metadata Management",
    author='Centre for Comparative Genomics',
    author_email='web@ccg.murdoch.edu.au',
    license="gpl3",
    packages=find_packages(),
    package_data={
        "bpametadata": [ "templates/admin/base_site.html" ],
        },
    install_requires=[
        "Django==1.5.2",
        "unipath==1.0",
        "South==0.8.2",
        "pygraphviz==1.2",
        "django-extensions==1.2.0",
        "django-admin-tools==0.5.1",
        "feedparser==5.1.3",
        "django-localflavor==1.0",
        "django-tinymce==1.5.1",
        "django-qbe==0.2.0",
        "django-tastypie==0.10.0",
        "django-bootstrap3==0.0.6",
        "mimeparse==0.1.3",
        ],
    dependency_links = [
        "http://repo.ccgapps.com.au",
        "http://bitbucket.org/izi/django-admin-tools/downloads/django-admin-tools-0.5.1.tar.gz"
    ],
    zip_safe=False,
    )

import setuptools
from setuptools import setup, find_packages
import os.path

current_dir = os.getcwd()

packages = [p.replace(".", "/") for p in sorted(find_packages())]

data_files = {}
for package in packages:
    data_files[package] = []
    os.chdir(os.path.join(package))
    for data_dir in ('templates', 'static', 'migrations', 'fixtures', 'features', 'templatetags', 'management'):
        data_files[package].extend([os.path.join(subdir,f) for (subdir, dirs, files) in os.walk(data_dir) for f in files])
    os.chdir(current_dir)

setup(
    name='bpam',
    version='1.0',
    description="BPA Metadata Management",
    author='Centre for Comparative Genomics',
    author_email='web@ccg.murdoch.edu.au',
    license="gpl3",
    packages=packages,
    package_data=data_files,
    install_requires=[
        "Django==1.5.4",
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
        "requests==1.2.3",
        "tendo==0.2.4",
        ],
    dependency_links = [
        "http://repo.ccgapps.com.au",
        "http://bitbucket.org/izi/django-admin-tools/downloads/django-admin-tools-0.5.1.tar.gz"
    ],
    zip_safe=False,
)

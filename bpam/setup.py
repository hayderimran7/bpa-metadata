import setuptools
from setuptools import setup, find_packages
import os.path
import re
from pip.req import parse_requirements

def list_requirements(name):
    return [str(ir.req) for ir in
            parse_requirements(os.path.join("..", "requirements", name))]

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
    install_requires=list_requirements("dev.txt"),
    )

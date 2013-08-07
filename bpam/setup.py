import setuptools
from setuptools import setup
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
    packages=[
        'bpam',
        'bpam.settings',
        'apps.bpaauth',
        'apps.common',
        'apps.common.management',
        'apps.common.management.commands',
        'apps.coral',
        'apps.melanoma',
        'apps.base_soil_agricultural',
        'apps.base_soil_environmental',
        'apps.wheat_cultivars',
        'apps.wheat_fungal_pathogens',
        'scripts',
        ],
    package_data={
        "bpametadata": [ "templates/admin/base_site.html" ],
        },
    install_requires=[str(ir.req) for ir in parse_requirements('../requirements/dev.txt')],
    )

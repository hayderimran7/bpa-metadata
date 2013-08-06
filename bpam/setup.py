import setuptools
from setuptools import setup
import os.path
import re

def list_requirements(name, _visited=None):
    "Lists the modules in a pip requirements.txt file"
    reqs = []
    filename = os.path.join(os.path.dirname(__file__), "..", "requirements", name)

    if _visited is None: _visited = set()
    _visited.add(name)

    with open(filename) as f:
        for line in f:
            line = line.strip()
            if line and line[0] != "#":
                include = re.match(r"^-r\s+([\w.]+)$", line, re.I)
                if include:
                    if include.group(1) not in _visited:
                        reqs.extend(list_requirements(include.group(1)))
                else:
                    reqs.append(line)
    return reqs

setup(
    name='bpam',
    version='1.0',
    description="BPA Metadata Management",
    author='Centre for Comparative Genomics',
    author_email='web@ccg.murdoch.edu.au',
    license="gpl3",
    packages=[
        'bpametadata',
        'bpametadata.settings',
        'bpaauth',
        'common',
        'common.management',
        'common.management.commands',
        'coral',
        'melanoma',
        'scripts',
        'bpam',
        ],
    package_data={
        "bpametadata": [ "templates/admin/base_site.html" ],
        },
    install_requires=list_requirements("dev.txt"),
    )

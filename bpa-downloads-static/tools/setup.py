from setuptools import setup
from pip.req import parse_requirements

requirements = [str(ir.req) for ir in parse_requirements('./requirements.txt')]

setup(
    name='bpalink',
    version='0.0.1',
    author='Centre for Comparative Genomics',
    author_email='web@ccg.murdoch.edu.au',
    description='Builds Melanoma Link tree',
    url='https://bitbucket.org/ccgmurdoch/linktreefactory',
    py_modules=['bpalink'],
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: MIT License',
    ],
    install_requires=requirements,
)

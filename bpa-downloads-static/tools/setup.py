from setuptools import setup
# from pip.req import parse_requirements
# requirements = [str(ir.req) for ir in parse_requirements('./requirements.txt')]

requirements = (
    'Unipath>=1.0',
    'docopt>=0.6.1',
    'tendo>=0.2.3',
    'xlrd>=0.9.2',
    'Jinja2>=2.7.1',
    'xlrd>=0.9.2',
    'python-keystoneclient',
    'python-swiftclient',
)

setup(
    name='bpalink',
    version='0.0.1',
    author='Centre for Comparative Genomics',
    author_email='web@ccg.murdoch.edu.au',
    description='Builds BPA Link tree',
    url='https://bitbucket.org/ccgmurdoch/linktreefactory',
    py_modules=['bpalink'],
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: MIT License',
    ],
    install_requires=requirements,
)

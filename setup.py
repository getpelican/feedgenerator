#! /usr/bin/python

# Using setuptools rather than distutils to get the `develop` command
from setuptools import setup


NAME = 'feedgenerator'
PACKAGES = ['feedgenerator', 'feedgenerator.django',
    'feedgenerator.django.utils']
DESCRIPTION = 'Standalone version of django.utils.feedgenerator, compatible with Py3k'
LONG_DESCRIPTION = open('README.rst').read()

URL = "https://github.com/dmdm/feedgenerator-py3k.git"

CLASSIFIERS = ['Development Status :: 3 - Alpha',
               'Environment :: Web Environment',
               'Intended Audience :: Developers',
               'License :: OSI Approved :: BSD License',
               'Operating System :: OS Independent',
               'Programming Language :: Python',
               'Programming Language :: Python :: 2.7',
               'Programming Language :: Python :: 3.2',
               'Topic :: Internet :: WWW/HTTP',
               'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
               'Topic :: Software Development :: Libraries :: Python Modules',
]

AUTHOR = 'Django Software Foundation'
AUTHOR_EMAIL = 'foundation@djangoproject.com'
MAINTAINER = 'Dirk Makowski'
MAINTAINER_EMAIL = 'dm@parenchym.com'
KEYWORDS = "feed atom rss".split(' ')
VERSION = '1.5.dev'

TEST_SUITE = 'tests'

REQUIRES = ['pytz', 'six']

setup(
    name=NAME,
    version=VERSION,
    packages=PACKAGES,
    test_suite=TEST_SUITE,
    install_requires=REQUIRES,
    # metadata for upload to PyPI
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    maintainer=MAINTAINER,
    maintainer_email=MAINTAINER_EMAIL,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    keywords=KEYWORDS,
    url=URL,
    classifiers=CLASSIFIERS,
)

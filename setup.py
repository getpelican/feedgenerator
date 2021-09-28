#!/usr/bin/env python


# Using setuptools rather than distutils to get the `develop` command
from setuptools import setup


NAME = 'feedgenerator'
PACKAGES = ['feedgenerator', 'feedgenerator.django',
            'feedgenerator.django.utils']
DESCRIPTION = 'Standalone version of django.utils.feedgenerator'
LONG_DESCRIPTION = open('README.rst', encoding='UTF-8').read()

URL = "https://github.com/getpelican/feedgenerator"

CLASSIFIERS = ['Development Status :: 5 - Production/Stable',
               'Environment :: Web Environment',
               'Framework :: Pelican',
               'Intended Audience :: Developers',
               'License :: OSI Approved :: BSD License',
               'Operating System :: OS Independent',
               'Programming Language :: Python',
               'Programming Language :: Python :: 3.6',
               'Programming Language :: Python :: 3.7',
               'Programming Language :: Python :: 3.8',
               'Programming Language :: Python :: 3.9',
               'Topic :: Internet :: WWW/HTTP',
               'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
               'Topic :: Software Development :: Libraries :: Python Modules',
               ]

AUTHOR = 'Django Software Foundation'
AUTHOR_EMAIL = 'foundation@djangoproject.com'
MAINTAINER = 'Pelican Dev Team'
MAINTAINER_EMAIL = 'authors@getpelican.com'
KEYWORDS = "feed atom rss".split(' ')
VERSION = '2.0.0'

TEST_SUITE = 'tests_feedgenerator'

REQUIRES = ['pytz >= 0a']

setup(
    name=NAME,
    version=VERSION,
    packages=PACKAGES,
    test_suite=TEST_SUITE,
    install_requires=REQUIRES,
    python_requires='>=3.6',
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
    zip_safe=False,
)

#! /usr/bin/python
from setuptools import setup


NAME = 'feedgenerator'
MODULES = ['feedgenerator']
DESCRIPTION = 'Standalone version of django.utils.feedgenerator'

URL = "http://hg.lolnet.org/feedgenerator/"

CLASSIFIERS = ['Development Status :: 5 - Production/Stable',
               'Environment :: Web Environment',
               'Intended Audience :: Developers',
               'License :: OSI Approved :: BSD License',
               'Operating System :: OS Independent',
               'Programming Language :: Python',
               'Topic :: Internet :: WWW/HTTP',
               'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
               'Topic :: Software Development :: Libraries :: Python Modules',
]

AUTHOR = 'Django Software Foundation'
AUTHOR_EMAIL = 'foundation@djangoproject.com'
MAINTAINER = 'Alexis Metaireau'
MAINTAINER_EMAIL= 'alexis@notmyidea.org'
KEYWORDS = "feed atom rss".split(' ')
VERSION = '1.2.1'

setup(
    name=NAME,
    version=VERSION,
    py_modules=MODULES,
    
    # metadata for upload to PyPI
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    maintainer=MAINTAINER,
    maintainer_email=MAINTAINER_EMAIL,
    description=DESCRIPTION,
    keywords=KEYWORDS,
    url=URL,
    classifiers=CLASSIFIERS,
)

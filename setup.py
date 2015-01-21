#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import kladr_api

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = kladr_api.__version__

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='django-kladr-api',
    version=version,
    description="""Some django stuff for kladr-api.ru (Russian address database Cloud API)""",
    long_description=readme + '\n\n' + history,
    author='Oleg Rybkin aka Fish',
    author_email='okfish@yandex.ru',
    url='https://github.com/okfish/django-kladr-api',
    packages=[
        'kladr_api',
    ],
    include_package_data=True,
    install_requires=[
    ],
    license="BSD",
    zip_safe=False,
    keywords='django-kladr-api',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
)

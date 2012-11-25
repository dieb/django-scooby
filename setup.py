#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import scooby

packages = ['scooby']
requires = []

setup(name='django-scooby',
      version=scooby.__version__,
      description='Minimalistic Django application for sending email notifications',
      long_description=open('README.rst').read() + '\n\n' + open('HISTORY.rst').read(),
      author=u'André Dieb Martins',
      author_email='andre.dieb@gmail.com',
      url='https://github.com/dieb/django-scooby/',
      packages=packages,
      package_data={'': ['LICENSE', 'NOTICE'], 'scooby': []},
      package_dir={'scooby': 'scooby'},
      include_package_data=True,
      license=open('LICENSE').read(),
      zip_safe=False,
      install_requires = [
        'Django>=1.3.1',
      ],
      classifiers = ['Development Status :: 2 - Pre-Alpha',
                     'Environment :: Web Environment',
                     'Framework :: Django',
                     'Intended Audience :: Developers',
                     'License :: OSI Approved :: ISC License (ISCL)',
                     'Operating System :: OS Independent',
                     'Programming Language :: Python',
                     'Topic :: Utilities'],
      )
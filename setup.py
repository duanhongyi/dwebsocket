#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
readme_file = os.path.join(here, 'README.rst')
changes_file = os.path.join(here, 'CHANGES.rst')

long_description = '\n\n'.join((
    file(readme_file).read(),
    file(changes_file).read(),
))


setup(
    name = u'dwebsocket',
    version = u'0.2.4',
    url = u'http://github.com/duanhongyi/dwebsocket',
    license = u'BSD',
    description = u'Websocket support for django.',
    long_description = long_description,
    author = "duanhongyi",
    author_email = u'duanhongyi@github.com',
    packages = ['dwebsocket'],
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'
    ],
    zip_safe = True,
    install_requires = ['setuptools'],
)

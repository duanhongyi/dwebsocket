#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup


long_description = '\n\n'.join((
    file('README.rst').read(),
    file('CHANGES.rst').read(),
))


setup(
    name = u'dwebsocket',
    version = u'0.2.1',
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

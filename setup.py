#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2016 t-kenji.
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.
#

import os
from setuptools import setup

setup(
    name = 'TracBootstrapTheme',
    version = '0.4',
    description = 'Bootstrap theme for Trac and ThemeEnginePlugin powered on Honoka.',
    url = 'https://github.com/t-kenji/trac-bootstrap-theme',
    keywords = 'trac plugin theme',
    classifiers = ['Framework :: Trac'],

    author = 't-kenji',
    author_email = 'protect.2501@gmail.com',
    license = 'BSD',  # the same as Trac
    maintainer='t-kenji',
    maintainer_email='protect.2501@gmail.com',

    packages = ['bstheme'],
    package_data = {
        'bstheme': [
            'templates/*.html',
            'htdocs/css/*.css',
            'htdocs/fonts/*.*',
            'htdocs/js/*.js',
            'htdocs/*.png',
            'htdocs/*.gif',
        ]},
    install_requires = ['TracThemeEngine'],
    entry_points = {
        'trac.plugins': [
            'bstheme.theme = bstheme.theme',
        ]
    },
)

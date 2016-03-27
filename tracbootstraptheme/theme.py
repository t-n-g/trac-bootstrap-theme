# -*- coding: utf-8 -*-
#
# Copyright (C) 2016 t-kenji.
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.
#

from pkg_resources import parse_version, resource_filename

from trac import __version__ as trac_version
from trac.core import Component, TracError, implements
from trac.web.api import IRequestFilter
from trac.web.chrome import Chrome, ITemplateStreamFilter, ITemplateProvider, \
                            add_script, add_stylesheet

from genshi.filters.transform import Transformer
from themeengine.api import IThemeProvider


__all__ = ['TracBootstrapTheme']


_stylesheets = (
    'tracbootstraptheme/css/bootstrap.min.css',
    'tracbootstraptheme/css/font-awesome.min.css',
    'tracbootstraptheme/css/trac-bootstrap.css',
    )

_javascripts = (
    'tracbootstraptheme/js/bootstrap.min.js',
    )

class TracBootstrapTheme(Component):

    implements(IRequestFilter,
               ITemplateStreamFilter,
               ITemplateProvider,
               IThemeProvider)

    css = True
    htdocs = True

    _bootstrap_theme = None

    def pre_process_request(self, req, handler):
        return handler

    def post_process_request(self, req, template, data, content_type):
        if template:
            theme = self._get_bootstrap_theme()
            if theme:
                for path in theme['stylesheets']:
                    add_stylesheet(req, path)
                for path in theme['javascripts']:
                    add_script(req, path)
                req.chrome['theme'] = 'bootstrap_theme.html'
        return template, data, content_type

    def filter_stream(self, req, method, filename, stream, data):
        def repl_link(name, event):
            attrs = event[1][1]
            if attrs.get(name):
                if attrs.get(name).endswith("common/css/trac.css"):
                    return attrs.get(name).replace("common/css/trac.css", 'tracbootstraptheme/css/trac.css')
            return attrs.get(name)

        stream = stream | Transformer('//head/link').attr('href', repl_link)
        return stream

    def get_htdocs_dirs(self):
        return [('tracbootstraptheme', resource_filename(__name__, 'htdocs'))]

    def get_templates_dirs(self):
        return [resource_filename(__name__, 'templates')]

    def get_theme_names(self):
        yield 'bootstrap_honoka'

    def get_template_overrides(self, name):
        yield ('wiki_page_path.html', 'bootstrap_wiki_page_path.html', None)
        #yield ('wiki_view.html', 'bootstrap_wiki_view.html', None)

    def get_theme_info(self, name):
        if not name.startswith('bootstrap_'):
            raise TracError('Internal Error')
        return {
            'description': 'Bootstrap theme powered by Honoka.',
            'screenshot': 'htdocs/screenshot.png',
        }

    def _get_bootstrap_theme(self):
        theme = self._bootstrap_theme
        if theme is None:
            name = self.config.get('theme', 'theme', '')
            if name and name.startswith('bootstrap_'):
                theme = {'name': name,
                         'stylesheets': list(self._get_stylesheets()),
                         'javascripts': list(self._get_javascripts())}
            else:
                theme = {}
            self._bootstrap_theme = theme
        return theme

    def _get_stylesheets(self):
        for path in _stylesheets:
            yield path

    def _get_javascripts(self):
        for path in _javascripts:
            yield path

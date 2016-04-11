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
    'tracbootstraptheme/css/trac.css',
    'tracbootstraptheme/css/bootstrap.min.css',
    'tracbootstraptheme/css/font-awesome.min.css',
    'tracbootstraptheme/css/trac-bootstrap.css',
    )

_javascripts = (
    'tracbootstraptheme/js/bootstrap.min.js',
    'tracbootstraptheme/js/trac-bootstrap.js',
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
        links = req.chrome.get('links')
        if links and 'stylesheet' in links:
          for i, link in enumerate(links['stylesheet']):
            if link.get('href', '').endswith('common/css/trac.css'):
              del links['stylesheet'][i]
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
                if attrs.get(name).endswith("common/css/report.css"):
                    return attrs.get(name).replace("common/css/report.css", 'tracbootstraptheme/css/report.css')
                if attrs.get(name).endswith("common/css/ticket.css"):
                    return attrs.get(name).replace("common/css/ticket.css", 'tracbootstraptheme/css/ticket.css')
                if attrs.get(name).endswith("common/css/timeline.css"):
                    return attrs.get(name).replace("common/css/timeline.css", 'tracbootstraptheme/css/timeline.css')
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
        yield ('admin_basics.html', 'bootstrap_admin_basics.html', None)
        yield ('admin_components.html', 'bootstrap_admin_components.html', None)
        yield ('admin_enums.html', 'bootstrap_admin_enums.html', None)
        yield ('admin_logging.html', 'bootstrap_admin_logging.html', None)
        yield ('admin_milestones.html', 'bootstrap_admin_milestones.html', None)
        yield ('admin_perms.html', 'bootstrap_admin_perms.html', None)
        yield ('admin_plugins.html', 'bootstrap_admin_plugins.html', None)
        yield ('admin_versions.html', 'bootstrap_admin_versions.html', None)
        yield ('attachment.html', 'bootstrap_attachment.html', None)
        yield ('history_view.html', 'bootstrap_history_view.html', None)
        yield ('login.html', 'bootstrap_login.html', None)
        yield ('milestone_delete.html', 'bootstrap_milestone_delete.html', None)
        yield ('milestone_edit.html', 'bootstrap_milestone_edit.html', None)
        yield ('milestone_view.html', 'bootstrap_milestone_view.html', None)
        yield ('prefs_advanced.html', 'bootstrap_prefs_advanced.html', None)
        yield ('prefs_general.html', 'bootstrap_prefs_general.html', None)
        yield ('prefs_keybindings.html', 'bootstrap_prefs_keybindings.html', None)
        yield ('prefs_localization.html', 'bootstrap_prefs_localization.html', None)
        yield ('prefs_notification.html', 'bootstrap_prefs_notification.html', None)
        yield ('prefs_pygments.html', 'bootstrap_prefs_pygments.html', None)
        yield ('prefs_userinterface.html', 'bootstrap_prefs_userinterface.html', None)
        yield ('query.html', 'bootstrap_query.html', None)
        yield ('roadmap.html', 'bootstrap_roadmap.html', None)
        yield ('report_delete.html', 'bootstrap_report_delete.html', None)
        yield ('report_edit.html', 'bootstrap_report_edit.html', None)
        yield ('report_list.html', 'bootstrap_report_list.html', None)
        yield ('report_view.html', 'bootstrap_report_view.html', None)
        yield ('ticket.html', 'bootstrap_ticket.html', None)
        yield ('ticket_preview.html', 'bootstrap_ticket_preview.html', None)
        yield ('timeline.html', 'bootstrap_timeline.html', None)
        yield ('wiki_delete.html', 'bootstrap_wiki_delete.html', None)
        yield ('wiki_diff.html', 'bootstrap_wiki_diff.html', None)
        yield ('wiki_edit.html', 'bootstrap_wiki_edit.html', None)
        yield ('wiki_edit_comment.html', 'bootstrap_wiki_edit_comment.html', None)
        yield ('wiki_edit_form.html', 'bootstrap_wiki_edit_form.html', None)
        yield ('wiki_rename.html', 'bootstrap_wiki_rename.html', None)
        yield ('wiki_view.html', 'bootstrap_wiki_view.html', None)

    def get_theme_info(self, name):
        if not name.startswith('bootstrap_'):
            raise TracError('Internal Error')
        return {
            'description': 'Bootstrap theme powered by Honoka.',
            'screenshot': 'htdocs/screenshot.png',
            'disable_trac_css' : True,
        }

    def _get_bootstrap_theme(self):
        theme = self._bootstrap_theme
        if theme is None:
            name = self.config.get('theme', 'theme', '')
            if name and name.startswith('bootstrap_'):
                theme = {'name': name,
                         'stylesheets': list(self._get_stylesheets()),
                         'javascripts': list(self._get_javascripts()),
                }
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

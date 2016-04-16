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
    'bstheme/css/trac.css',
    'bstheme/css/bootstrap.min.css',
    'bstheme/css/font-awesome.min.css',
    'bstheme/css/trac-bootstrap.css',
    )

_javascripts = (
    'bstheme/js/bootstrap.min.js',
    'bstheme/js/trac-bootstrap.js',
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
                req.chrome['theme'] = 'bs_theme.html'
        return template, data, content_type

    def filter_stream(self, req, method, filename, stream, data):
        def repl_link(name, event):
            attrs = event[1][1]
            if attrs.get(name):
                if attrs.get(name).endswith("common/css/report.css"):
                    return attrs.get(name).replace("common/css/report.css", 'bstheme/css/report.css')
                if attrs.get(name).endswith("common/css/ticket.css"):
                    return attrs.get(name).replace("common/css/ticket.css", 'bstheme/css/ticket.css')
                if attrs.get(name).endswith("common/css/timeline.css"):
                    return attrs.get(name).replace("common/css/timeline.css", 'bstheme/css/timeline.css')
                return attrs.get(name)

        stream = stream | Transformer('//head/link').attr('href', repl_link)
        return stream

    def get_htdocs_dirs(self):
        return [('bstheme', resource_filename(__name__, 'htdocs'))]

    def get_templates_dirs(self):
        return [resource_filename(__name__, 'templates')]

    def get_theme_names(self):
        yield 'bootstrap_honoka'

    def get_template_overrides(self, name):
        yield ('admin_basics.html', 'bs_admin_basics.html', None)
        yield ('admin_components.html', 'bs_admin_components.html', None)
        yield ('admin_enums.html', 'bs_admin_enums.html', None)
        yield ('admin_logging.html', 'bs_admin_logging.html', None)
        yield ('admin_milestones.html', 'bs_admin_milestones.html', None)
        yield ('admin_perms.html', 'bs_admin_perms.html', None)
        yield ('admin_plugins.html', 'bs_admin_plugins.html', None)
        yield ('admin_versions.html', 'bs_admin_versions.html', None)
        yield ('attachment.html', 'bs_attachment.html', None)
        yield ('history_view.html', 'bs_history_view.html', None)
        yield ('login.html', 'bs_login.html', None)
        yield ('milestone_delete.html', 'bs_milestone_delete.html', None)
        yield ('milestone_edit.html', 'bs_milestone_edit.html', None)
        yield ('milestone_view.html', 'bs_milestone_view.html', None)
        yield ('prefs_advanced.html', 'bs_prefs_advanced.html', None)
        yield ('prefs_general.html', 'bs_nprefs_general.html', None)
        yield ('prefs_keybindings.html', 'bs_prefs_keybindings.html', None)
        yield ('prefs_localization.html', 'bs_prefs_localization.html', None)
        yield ('prefs_notification.html', 'bs_prefs_notification.html', None)
        yield ('prefs_pygments.html', 'bs_prefs_pygments.html', None)
        yield ('prefs_userinterface.html', 'bs_prefs_userinterface.html', None)
        yield ('query.html', 'bs_query.html', None)
        yield ('roadmap.html', 'bs_roadmap.html', None)
        yield ('report_delete.html', 'bs_report_delete.html', None)
        yield ('report_edit.html', 'bs_report_edit.html', None)
        yield ('report_list.html', 'bs_report_list.html', None)
        yield ('report_view.html', 'bs_report_view.html', None)
        yield ('ticket.html', 'bs_ticket.html', None)
        yield ('ticket_preview.html', 'bs_ticket_preview.html', None)
        yield ('timeline.html', 'bs_timeline.html', None)
        yield ('wiki_delete.html', 'bs_wiki_delete.html', None)
        yield ('wiki_diff.html', 'bs_wiki_diff.html', None)
        yield ('wiki_edit.html', 'bs_wiki_edit.html', None)
        yield ('wiki_edit_comment.html', 'bs_wiki_edit_comment.html', None)
        yield ('wiki_edit_form.html', 'bs_wiki_edit_form.html', None)
        yield ('wiki_rename.html', 'bs_wiki_rename.html', None)
        yield ('wiki_view.html', 'bs_wiki_view.html', None)

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

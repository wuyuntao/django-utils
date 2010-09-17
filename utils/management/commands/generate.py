# -*- coding: utf-8 -*-

import os
import re
import shlex
import shutil
from subprocess import Popen, PIPE
from optparse import make_option

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Import css and js frameworks'

    CSS_FRAMEWORKS = ['blueprint', 'emastic3']
    JS_FRAMEWORKS = ['jquery', 'jqueryui']
    HTML_FRAMEWORKS = ['html', 'html5']

    BIN_PATH = '%s/bin' % os.path.dirname(__file__)
    TEMPLATE_PATH = '%s/templates' % os.path.dirname(__file__)

    option_list = BaseCommand.option_list + (
        make_option('--css', '-c', action='store', default='',
            help='Import CSS frameworks like %s' % (', '.join(CSS_FRAMEWORKS),)),

        make_option('--css-path', '-C', action='store', default='css',
            help='Path to store stylesheets'),

        make_option('--js', '-j', action='store', default='',
            help='Import javascript frameworks like %s' % (', '.join(JS_FRAMEWORKS),)),

        make_option('--js-path', '-J', action='store', default='js',
            help='Path to store javascripts'),

        make_option('--html', '-H', action='store', default='',
            help='Import HTML templates like %s' % (', '.join(HTML_FRAMEWORKS),)),
    )

    def handle(self, *args, **options):
        for css in set(options['css'].split(',')):
            if not css: continue

            css_path = '%s/%s' % (settings.MEDIA_ROOT, options['css_path'])
            self._makedirs(css_path)
            if css in ('blueprint', 'emastic3'):
                cmd = shlex.split("%s/%s %s" % (self.BIN_PATH, css, css_path))
                Popen(cmd, stdout=PIPE)
            else:
                print "We do not support %s yet" % css

        for js in set(options['js'].split(',')):
            if not js: continue

            js_path = '%s/%s/%s' % (settings.MEDIA_ROOT, options['js_path'], js)
            self._makedirs(js_path)
            if js in ('jquery', 'jqueryui'):
                cmd = shlex.split("%s/%s %s" % (self.BIN_PATH, js, js_path))
                Popen(cmd, stdout=PIPE)
            else:
                print "We do not support %s yet" % js

        for html in set(options['html'].split(',')):
            if not html: continue

            if len(settings.TEMPLATE_DIRS) > 0:
                html_path = settings.TEMPLATE_DIRS[0]
            else:
                html_path = '%s/templates' % settings.ROOT_PATH

            self._makedirs(html_path)
            if html == 'html':
                shutil.copy('%s/base.html' % self.TEMPLATE_PATH, html_path)

            elif html == 'html5':
                shutil.copy('%s/base5.html' % self.TEMPLATE_PATH, html_path)

            else:
                print "We do not support %s yet" % js

    def _makedirs(self, path):
        try:
            os.makedirs(path)
        except OSError, e:
            # Ignore file exists error
            if str(e).find('File exists') > 0:
                pass
            else:
                raise OSError, e

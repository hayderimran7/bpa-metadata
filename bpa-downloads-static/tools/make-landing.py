#!/usr/bin/env python
# coding: utf-8

"""
ake-landing.py creates the bpa downloads

Usage:
  bpalink.py [options] WEB_ROOT

Options:
  -v, --verbose    Verbose mode.
"""

__version__ = '0.0.1'

import sys
import os
import datetime
import distutils.core
import logging

from jinja2 import FileSystemLoader
from jinja2.environment import Environment

from docopt import docopt
from unipath import Path


logging.basicConfig(level=logging.DEBUG)


def make_landing_page(args):
    """
    Make the bpa-downloads web site landing page.
    """

    def copy_statics():
        # copy statics
        root_source = Path(Path(os.path.abspath(__file__)).ancestor(2), "webroot/")
        logging.info('Copying statics from {0} to {1}'.format(root_source, args['WEB_ROOT']))
        distutils.dir_util.copy_tree(root_source, args['WEB_ROOT'])

    def make_index():
        # make index.html fom template
        env = Environment()
        env.loader = FileSystemLoader('templates/')
        template = env.get_template('landing_page.html')

        output_filename = os.path.join(args['WEB_ROOT'], 'index.html')
        tmpf = output_filename + '.tmp'
        with open(tmpf, 'w') as fd:
            template_data = {'now': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            fd.write(template.render(template_data))
        # backup old index
        os.rename(output_filename, output_filename + '.old')
        os.rename(tmpf, output_filename)

    copy_statics()
    make_index()


if __name__ == '__main__':
    def sanity_check():
        def test_path(path):
            if not Path(path).exists():
                sys.exit("The folder {0} does not exist. Quitting".format(path))

        # does the source folder exist ?
        test_path(args['WEB_ROOT'])

    args = docopt(__doc__, version=__version__)
    if args['--verbose']:
        logging.info(args)
    sanity_check()
    make_landing_page(args)
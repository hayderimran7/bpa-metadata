#!/usr/bin/env python
# coding: utf-8
import sys
import os
from docopt import docopt

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '../../bpam/libs/'))  # FIXME
from logger_utils import get_logger

__version__ = "1.0.0"
logger = get_logger(__file__)

"""
{0} builds the downloads link tree for the BASE Amplicon project data

Usage:
  {0} [options] ( landing_page | melanoma | gbr | wheat7a | wheat_cultivars | wheat_pathogens | base ) SUBARCHIVE_ROOT

Options:
  -v, --verbose                       Verbose mode.
  -s, --swiftbase=SWIFTURI            Base URI for files in swift [default: http://swift.bioplatforms.com/v1/AUTH_b154c0aff02345fba80bd118a54177ea]
  -a, --apacheredirects=APACHEREDIRS  Output file for Apache redirects
  -l, --linktree=LINKTREE_ROOT        Base path for link tree
  -o, --htmlbase=HTMLBASE             Output path for HTML
  -b, --linkbase=PUBLICURI            Base URI for files on public interface,  [default: http://downloads.bioplatforms.com/]
"""


if __name__ == '__main__':

    args = docopt(__doc__, version=__version__.format(__file__))
    if args['--verbose']:
        logger.info(args)

#!/usr/bin/env python2.7
"""
This tool takes a Django json class definition template and a csv dataset and makes a Django
fixture. It expects a directory with a template.txt and data.csv file.

Usage:
    makefixture.py [options] TAXONDIRECTORY

Options:
    -v --verbose  Explain what makefixture is doing as it is doing it.
    -t --template=NAME  Specify the template file name [default: template.txt].
    -l --list=NAME  Specify the source data file name [default: data.csv].
"""

import logging
from tendo import colorer

from docopt import docopt
import csv
from pprint import pprint
from unipath import Path

__version__ = "0.1"
logging.basicConfig(level=logging.INFO)


def get_template(args):
    template_file = Path(args['TAXONDIRECTORY'], args['--template'])
    with open(template_file, 'r') as tfile:
        template = tfile.read()
        logging.info(template)
        return template.strip()


def get_csv_reader(args):
    data_file = Path(args['TAXONDIRECTORY'], args['--list'])
    return csv.DictReader(open(data_file, 'r'), delimiter=';', restkey='the_rest')


def get_fixture_list(args):
    """
    make a list of fixture objects
    """
    fixturelist = []
    template = get_template(args)
    for d in get_csv_reader(args):
        wc = template
        for k, v in d.items():
            wc = wc.replace('${%s}' % k, v)
        fixturelist.append(wc)

    return fixturelist


def print_fixtures(fixturelist):
    """
    Print the list of fixtures
    """
    print("[")
    for i, e in enumerate(fixturelist):
        e = e.replace('${pkey}', str(i + 1))
        if (i + 1) < len(fixturelist):
            print(e + ", ")
        else:
            print(e)
    print("]")


def main(args):
    fixturelist = get_fixture_list(args)
    print_fixtures(fixturelist)


if __name__ == "__main__":
    args = docopt(__doc__, version=__version__)
    if args['--verbose']:
        pprint.pprint(args)
        logging.basicConfig(level=logging.DEBUG)

    main(args)


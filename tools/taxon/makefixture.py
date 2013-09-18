#!/usr/bin/env python2.7
"""
This tool takes a Django json class definition template and a csv dataset and makes a Django
fixture. It expects a directory with a template.txt and data.csv file.

Usage:
    makefixture.py [options] TAXONDIRECTORY [FIXTURE]

Options:
    -v --verbose  Explain what makefixture is doing as it is doing it.
    -c --config=NAME  Specify the config module name for this fixture [default: config].
    -l --list=NAME  Specify the source data file name [default: data.csv].
"""

import logging
from tendo import colorer

from docopt import docopt
import csv
from pprint import pprint
from unipath import Path
import json
import importlib
import sys
import codecs

from django.utils.encoding import smart_text

__version__ = "0.1"
logging.basicConfig(level=logging.INFO)


def import_config(args):
    sys.path.append(Path(args['TAXONDIRECTORY']))
    return importlib.import_module(args['--config'])


def get_csv_reader(args):
    data_file = Path(args['TAXONDIRECTORY'], args['--list'])
    return csv.DictReader(open(data_file, 'r'), delimiter=';', restkey='the_rest')


def get_fixture_list(args):
    """
    make a list of fixture objects
    """
    fixturelist = []
    config = import_config(args)

    for i, d in enumerate(get_csv_reader(args)):
        fixture = {"model": config.model_class, "fields": {}, "pk": i + 1}
        for k, v in d.items():
            fixture["fields"][k] = smart_text(v)
        fixturelist.append(fixture)

    return fixturelist


def print_fixtures(args, fixturelist):
    """
    Print the list of fixtures
    """

    fixture_name = args['FIXTURE']
    if fixture_name:
        with codecs.open(args['FIXTURE'], "w",  encoding='utf-8') as f:
            json.dump(fixturelist, f, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))
    else:
        print(json.dumps(fixturelist, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': ')))


def main(args):
    fixturelist = get_fixture_list(args)
    print_fixtures(args, fixturelist)


if __name__ == "__main__":
    args = docopt(__doc__, version=__version__)
    if args['--verbose']:
        pprint.pprint(args)
        logging.basicConfig(level=logging.DEBUG)

    main(args)


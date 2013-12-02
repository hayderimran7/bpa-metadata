#!/usr/bin/env python
# coding: utf-8

"""
wh.py builds download link trees with file names provided.

Usage:
  isolate_indexer.py [options] SUBARCHIVE_ROOT

Options:
  -v, --verbose                       Verbose mode.
  -s, --swiftbase=SWIFTURI            Base URI for files in swift [default: http://swift.bioplatforms.com/v1/AUTH_b154c0aff02345fba80bd118a54177ea]
  -a, --apacheredirects=APACHEREDIRS  Output file for Apache redirects
  -l, --linktree=LINKTREE_ROOT        Base path for link tree
  -o, --htmlbase=HTMLBASE             Output path for HTML
  -b, --linkbase=PUBLICURI            Base URI for files on public interface,  [default: http://downloads.bioplatforms.com/]
"""

import sys
import re
import urlparse
import os
import json
import datetime
from collections import namedtuple
import logging
from operator import itemgetter

from docopt import docopt
from unipath import Path
import unipath
import xlrd
from jinja2 import FileSystemLoader
from jinja2.environment import Environment


logging.basicConfig(level=logging.DEBUG)




def _stringify(s):
    if isinstance(s, str):
        return str(s.decode('utf8'))
    elif isinstance(s, unicode):
        return str(s.encode('utf8'))
    else:
        return str(s)


def stringify(s):
    _s = _stringify(s)
    return _s


def excel_date_to_string(date_mode, s):
    try:
        date_val = float(s)
        tpl = xlrd.xldate_as_tuple(date_val, date_mode)
        return datetime.datetime(*tpl).strftime("%d/%m/%Y")
    except ValueError:
        return s


class ExcelWrapper(object):
    def __init__(self, fname):
        self.workbook = xlrd.open_workbook(fname)

    def get_date_mode(self):
        return self.workbook.datemode

    def sheet_iter(self, sheet_name):
        sheet = [t for t in self.workbook.sheets() if t.name.lower() == sheet_name.lower()][0]
        for row_idx in xrange(sheet.nrows):
            vals = [stringify(t) for t in sheet.row_values(row_idx)]
            yield vals


class IsolateIndexer(object):
    metadata_filename = '../../../data/wheat_pathogens/current'
    metadata_sheet = 'Metadata'
    index_template = 'wheat_pathogens_species.html'

    fieldspec = [
        ('md5', 'MD5 checksum', None),
        ('filename', 'FILE NAMES - supplied by AGRF', lambda p: p.rsplit('/', 1)[-1]),
        ('uid', 'BPA ID', None),
        ('flow_cell_id', 'Run #:Flow Cell ID', None),
        ('pathogen', 'Species', None),
        ('isolate', 'Researcher Sample ID', None),
        ('official_variety_name', 'Official Variety Name', None),
        ('run', 'Run number', lambda s: s.replace('RUN #', '')),
        ('genome_analysis', 'Genome-Analysis', lambda s: s.split('_')[0]),
        ('metadata_file', 'Metadata file', None),
    ]

    def parse_to_named_tuple(self, typname, reader, header):
        """
        parse a CSV file and yield a list of namedtuple instances.
        fieldspec specifies the CSV fields to be read in, and the name
        of the attribute to map them to on the new type
        reader should be past the header - clear to read normal rows.
        the header in which to look up fields must be passed in.

        always adds a 'row' member to the named tuple, which is the row
        number of the entry in the source file (minus header)
        """
        typ = namedtuple(typname, ['row'] + [t[0] for t in self.fieldspec])
        lookup = []
        fns = [t[2] for t in self.fieldspec]
        for _, field_name, _ in self.fieldspec:
            idx = header.index(field_name)
            assert (idx != -1)
            lookup.append(idx)
        for idx, row in enumerate(reader):
            tpl = [idx]
            for fn, i in zip(fns, lookup):
                val = row[i].decode('utf-8').strip()
                if fn is not None:
                    val = fn(val)
                tpl.append(val)
            yield typ(*tpl)

    def parse_metadata(self):
        metadata = []

        wrapper = ExcelWrapper(self.metadata_filename)
        reader = wrapper.sheet_iter(self.metadata_sheet)
        header = [t.strip() for t in next(reader)]
        for tpl in self.parse_to_named_tuple('WheatPathogensMeta', reader, header):
            if tpl.filename == '' or tpl.uid == '':
                continue
            metadata.append(tpl)
        return metadata

    def get_pathogen_isolate_set(self, metadata):
        """
        Get set of pathogen-isolate pairs, ordered by pathogen
        """
        pathogen_isolate = set()
        for e in metadata:
            pi = (e.pathogen, e.isolate, e.uid, e.genome_analysis, e.metadata_file)
            pathogen_isolate.add(pi)
        return pathogen_isolate

    def get_index_template_environment(self, isolate_set):
        objects = []
        for pathogen, isolate, uid, genome_analysis, metadata_file in isolate_set:
            objects.append({
                'pathogen': pathogen,
                'isolate': isolate,
                'bpa_id': uid,
                'genome_analysis': genome_analysis,
                'metadata_file': metadata_file,
            })

        object_list = sorted(objects, key=itemgetter('pathogen'))
        return {'object_list': object_list}

    def make_index(self, template_environment):
        env = Environment()
        env.loader = FileSystemLoader('../templates/')
        index_template = env.get_template(self.index_template)

        with open('isolate_index.html', 'w') as fd:
            fd.write(index_template.render(template_environment))


def run():
    from pprint import pprint
    indexer = IsolateIndexer()
    data = indexer.parse_metadata()
    pathogen_isolate_set = indexer.get_pathogen_isolate_set(data)
    index_template_environment = indexer.get_index_template_environment(pathogen_isolate_set)
    indexer.make_index(index_template_environment)


if __name__ == "__main__":
    run()

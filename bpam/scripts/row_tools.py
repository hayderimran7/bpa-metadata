# coding: utf-8

"""
Tool to manage the import of row-based data.
This data is typically read from Excel workbooks, or CSV files.
"""

import os
import datetime
from collections import namedtuple
import logging
import xlrd

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class ColumnNotFoundException(Exception):
    column_name = 'Not Set'

    def __init__(self, column_name):
        self.column_name = column_name

    def __str__(self):
        return 'Column {0} not found'.format(self.column_name)


def _stringify(s):
    if isinstance(s, str):
        return str(s.decode('utf8'))
    elif isinstance(s, unicode):
        return str(s.encode('utf8'))
    else:
        return str(s)


class ExcelWrapper(object):
    def __init__(self, fname):
        self.workbook = xlrd.open_workbook(fname)

    def get_date_mode(self):
        return self.workbook.datemode

    def date_to_string(self, s):
        try:
            date_val = float(s)
            tpl = xlrd.xldate_as_tuple(date_val, self.workbook.datemode)
            return datetime.datetime(*tpl).strftime("%d/%m/%Y")
        except ValueError:
            return s

    def sheet_iter(self, sheet_name):
        sheet = [t for t in self.workbook.sheets() if t.name.lower() == sheet_name.lower()][0]
        for row_idx in xrange(sheet.nrows):
            vals = [_stringify(t) for t in sheet.row_values(row_idx)]
            yield vals


def parse_to_named_tuple(typname, reader, header, fieldspec):
    """
    parse a CSV file and yield a list of namedtuple instances.
    fieldspec specifies the CSV fields to be read in, and the name
    of the attribute to map them to on the new type
    reader should be past the header - clear to read normal rows.
    the header in which to look up fields must be passed in.

    always adds a 'row' member to the named tuple, which is the row
    number of the entry in the source file (minus header)
    """

    typ = namedtuple(typname, ['row'] + [t[0] for t in fieldspec])
    lookup = []
    functions = [t[2] for t in fieldspec]
    for _, field_name, _ in fieldspec:
        idx = header.index(field_name)
        if idx == -1:
            raise ColumnNotFoundException(field_name)

        assert (idx != -1)
        lookup.append(idx)

    for idx, row in enumerate(reader):
        tpl = [idx]
        for fn, i in zip(functions, lookup):
            # if the column is a date, be nice to it
            if
            val = row[i].decode('utf-8').strip()
            if fn is not None:
                val = fn(val)
            tpl.append(val)
        yield typ(*tpl)
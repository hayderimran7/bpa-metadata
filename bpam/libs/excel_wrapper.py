# coding: utf-8

"""
Tool to manage the import of row-based data.
This data is typically read from Excel workbooks.

Pass a filename, a sheet_name, a mapping (fieldspec)
Fieldspec maps spread sheet column names to more manageable names. It provides
functions associated with each column type that must be used to massage the data found in the column.

It returns a iterator providing a list of named tuples.
"""

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
    """
    Parse a excel file and yield a list of namedtuple instances.
    fieldspec specifies the columns  to be read in, and the name
    of the attribute to map them to on the new type

    field_spec: list of (new_name, column_name, callable) tuples
    file_name: workbook name
    sheet_name: sheet in workbook
    header_length: first number of lines to ignore
    column_name_row_index: row in which colum names are found, typically 0
    """

    def __init__(self, field_spec, file_name, sheet_name, header_length, column_name_row_index=0):
        self.sheet_name = sheet_name
        self.header_length = header_length
        self.column_name_row_index = column_name_row_index
        self.field_spec = field_spec

        self.workbook = xlrd.open_workbook(file_name)
        self.sheet = self.workbook.sheet_by_name(self.sheet_name)

    def get_date_mode(self):
        assert (self.workbook is not None)
        return self.workbook.datemode

    def date_to_string(self, s):
        try:
            date_val = float(s)
            tpl = xlrd.xldate_as_tuple(date_val, self.workbook.datemode)
            return datetime.datetime(*tpl).strftime("%d/%m/%Y")
        except ValueError:
            return s

    def set_column_positions(self):
        """
        find the column position
        """
        column_positions = []

        for _, field_name, _ in self.field_spec:
            idx = self.sheet.row_values(self.column_name_row_index).index(field_name)
            if idx == -1:
                raise ColumnNotFoundException(field_name)
            assert (idx != -1)
            column_positions.append(idx)

        return column_positions

    def _get_rows(self):
        """
        Yields sequence of cells
        """
        for row_idx in xrange(self.sheet.nrows)[self.header_length - 1:]:
            yield self.sheet.row(row_idx)

    def parse_to_named_tuple(self, typname='DataRow'):
        """
        always adds a 'row' member to the named tuple, which is the row
        number of the entry in the source file (minus header(s))
        """
        # row is added so we know where in the spreadsheet this came from
        typ = namedtuple(typname, ['row'] + [t[0] for t in self.field_spec])
        functions = [t[2] for t in self.field_spec]
        column_positions = self.set_column_positions()

        for idx, row in enumerate(self._get_rows()):
            tpl = [idx]
            for fn, i in zip(functions, column_positions):
                # if the column type is a date, try to handle it as such
                if row[i].ctype == xlrd.XL_CELL_DATE:
                    val = datetime(*xlrd.xldate_as_tuple(row[i].value, self.get_date_mode()))
                else:
                    val = row[i].decode('utf-8').strip()
                if fn is not None:
                    val = fn(val)
                tpl.append(val)
            yield typ(*tpl)
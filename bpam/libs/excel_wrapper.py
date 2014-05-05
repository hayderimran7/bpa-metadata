# _*_ coding: utf-8 _*_

"""
Tool to manage the import of rows from Excel workbooks.

Pass a filename, a sheet_name, a mapping (fieldspec)
Fieldspec maps spread sheet column names to more manageable names. It provides
functions associated with each column type that must be used to massage the data found in the column.

It returns a iterator providing named tuples, each tuple contains key/value pairs, the keys
being the fist column of the fieldspec, the value are found in the column specisied in the second fieldspec field
as mangled by the provided method.
"""

import datetime
from collections import namedtuple
import xlrd

import logger_utils

logger = logger_utils.get_logger(__name__)


class ColumnNotFoundException(Exception):
    column_name = 'Not Set'

    def __init__(self, column_name):
        self.column_name = column_name

    def __str__(self):
        return 'Column [{0}] not found'.format(self.column_name)


def _stringify(s):
    if isinstance(s, str):
        return str(s.decode('utf8'))
    elif isinstance(s, unicode):
        return str(s.encode('utf8'))
    else:
        return str(s)


class ExcelWrapper(object):
    """
    Parse a excel file and yields namedtuples.
    fieldspec specifies the columns  to be read in, and the name
    of the attribute to map them to on the new type

    field_spec: list of (new_name, column_name, callable) tuples
    file_name: workbook name
    sheet_name: sheet in workbook
    header_length: first number of lines to ignore
    column_name_row_index: row in which column names are found, typically 0
    """

    def __init__(self, field_spec, file_name, sheet_name, header_length, column_name_row_index=0):
        self.sheet_name = sheet_name
        self.header_length = header_length
        self.column_name_row_index = column_name_row_index
        self.field_spec = field_spec

        self.workbook = xlrd.open_workbook(file_name)
        self.sheet = self.workbook.sheet_by_name(self.sheet_name)

        self.field_names = self._set_field_names()
        self.name_to_column_map = self.set_name_to_column_map()
        self.name_to_func_map = self.set_name_fo_func_map()

    def _set_field_names(self):
        """
        sets field name list
        """
        names = []
        for attribute, _, _ in self.field_spec:
            if attribute in names:
                logger.error('Attribute {0} is listed more than once in the field specification'.format(attribute))
            names.append(attribute)
        return names

    def set_name_to_column_map(self):
        """
        maps the named field to the actual column in the spreadsheet
        """
        cmap = {}
        for attribute, column_name, _ in self.field_spec:
            try:
                col_index = self.sheet.row_values(self.column_name_row_index).index(column_name)
            except ValueError:
                logger.error('column name {0} not found'.format(column_name))
                raise ColumnNotFoundException(column_name)

            cmap[attribute] = col_index
        return cmap

    def set_name_fo_func_map(self):
        """
        Map the spec fields to their corresponding functions
        """
        function_map = {}
        for attribute, _, func in self.field_spec:
            function_map[attribute] = func
        return function_map

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

    def _get_rows(self):
        """
        Yields sequence of cells
        """
        for row_idx in xrange(self.header_length, self.sheet.nrows):
            yield self.sheet.row(row_idx)

    def get_all(self, typname='DataRow'):
        """
        Returns all rows for the sheet as named tuples.
        """
        # row is added so we know where in the spreadsheet this came from
        typ = namedtuple(typname, ['row'] + [n for n in self.field_names])

        for idx, row in enumerate(self._get_rows()):
            tpl = [idx]
            for name in self.field_names:
                i = self.name_to_column_map[name]
                func = self.name_to_func_map[name]
                ctype = row[i].ctype
                val = row[i].value
                if ctype == xlrd.XL_CELL_DATE:
                    try:
                        val = datetime.datetime(*xlrd.xldate_as_tuple(val, self.get_date_mode()))
                    except ValueError, e:
                        logger.error("Error '{0}' column:{1}".format(e, i))
                        val = val  # keep the original value
                        print val
                if ctype == xlrd.XL_CELL_TEXT:
                    val = val.strip()

                if func is not None:
                    val = func(val)
                tpl.append(val)
            yield typ(*tpl)
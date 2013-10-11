#! /usr/bin/env python
# coding: utf-8

__author__ = 'ccg'

import xlrd

wb = xlrd.open_workbook('Melanoma_study_metadata.xlsx')
metadata_sheet = wb.sheet_by_name('Melanoma_study_metadata')
for row in range(metadata_sheet.nrows):
    for col in range(metadata_sheet.ncols):
        print metadata_sheet.cell(row, col).value


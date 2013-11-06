"""
Creates a report on missing sequence files
"""

import logging
import xlwt

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)

from apps.common.models import *
from apps.melanoma.models import MelanomaSequenceFile


def make_report(missing):
    '''
    Make a missing file report
    '''

    book = xlwt.Workbook()
    sheet = book.add_sheet('Missing Melanoma Sequence Files')
    sheet.write(0, 0, 'BPA ID')
    sheet.write(0, 1, 'File Name')

    for i, f in enumerate(missing):
        sheet.write(i + 1, 0, f.sample.bpa_id.bpa_id)
        sheet.write(i + 1, 1, f.filename)

    book.save('missing_melanoma.xlsx')


def run():
    # melanoma
    missing = [f for f in MelanomaSequenceFile.objects.all() if not f.link_ok()]
    make_report(missing)
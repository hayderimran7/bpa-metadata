"""
Creates a report on missing sequence files
"""

import logging
import xlwt

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)

from apps.melanoma.models import MelanomaSequenceFile

MISSING_REPORT_NAME = 'missing_melanoma.xlsx'


def make_report(missing):
    logger.info('{0} missing Melanoma Sequence files'.format(len(missing)))
    book = xlwt.Workbook()
    sheet = book.add_sheet('Missing Melanoma Sequence Files')
    sheet.write(0, 0, 'BPA ID')
    sheet.write(0, 1, 'File Name')

    for i, f in enumerate(missing):
        sheet.write(i + 1, 0, f.sample.bpa_id.bpa_id)
        sheet.write(i + 1, 1, f.filename)

    book.save(MISSING_REPORT_NAME)
    logger.info('Wrote report {0}'.format(MISSING_REPORT_NAME))


def run():
    # melanoma
    missing = [f for f in MelanomaSequenceFile.objects.all() if not f.link_ok()]
    make_report(missing)
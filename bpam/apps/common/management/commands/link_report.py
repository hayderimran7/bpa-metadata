"""
Creates a report on missing sequence files
"""

import xlwt
from django.core.management.base import BaseCommand
from libs.logger_utils import get_logger
from apps.melanoma.models import MelanomaSequenceFile

logger = get_logger(__name__)


MISSING_REPORT_NAME = 'missing_melanoma.xlsx'


def make_report(not_ok):
    logger.info('{0} Melanoma Sequence files with issues'.format(len(not_ok)))
    book = xlwt.Workbook()
    sheet = book.add_sheet('Melanoma Files with issues')
    sheet.write(0, 0, 'BPA ID')
    sheet.write(0, 1, 'File Name')
    sheet.write(0, 2, 'Issue')

    for i, f in enumerate(not_ok):
        sheet.write(i + 1, 0, f.sample.bpa_id.bpa_id)
        sheet.write(i + 1, 1, f.filename)
        sheet.write(i + 1, 2, f.ingest_issue)

    book.save(MISSING_REPORT_NAME)
    logger.info('Wrote report {0}'.format(MISSING_REPORT_NAME))


class Command(BaseCommand):
    help = 'Link Report, Melanoma Only'

    def handle(self, *args, **options):
        # melanoma
        not_ok = [f for f in MelanomaSequenceFile.objects.all() if not f.link_ok()]
        make_report(not_ok)

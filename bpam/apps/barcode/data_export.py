# -*- coding: utf-8 -*-

import djqscsv
from cStringIO import StringIO
from .models import Sheet

# plate
def get_sheets(response):
    qs = Sheet.objects.values()
    return djqscsv.render_to_csv_response(qs)


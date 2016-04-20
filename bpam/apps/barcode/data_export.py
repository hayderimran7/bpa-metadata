# -*- coding: utf-8 -*-

import djqscsv
from .models import Sheet


# plate
def get_sheets(response):
    qs = Sheet.objects.values()
    return djqscsv.render_to_csv_response(qs)

# -*- coding: utf-8 -*-

from import_export import fields
import ingest


class DateField(fields.Field):
    """
    This field automatically parses a number of known date formats and returns
    the standard python date
    """

    def __init__(self, *args, **kwargs):
        super(DateField, self).__init__(*args, **kwargs)

    def clean(self, data):
        try:
            val = data[self.column_name]
            return ingest.get_date(val)
        except ValueError:
            return None


class BPAIDField(fields.Field):
    def __init__(self, *args, **kwargs):
        super(BPAIDField, self).__init__(*args, **kwargs)

    def clean(self, data):
        return ingest.get_bpa_id(data[self.column_name])

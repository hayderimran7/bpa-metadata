# -*- coding: utf-8 -*-

from import_export import fields
from libs.ingest_utils import get_date  # noqa
from apps.common.models import BPAUniqueID, BPAProject


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
            return get_date(val)
        except ValueError:
            return None


def get_bpa_id(bpaid):
    """get BPA ID"""

    if bpaid is None:
        return None

    bpaid = bpaid.replace("/", ".")
    project, _ = BPAProject.objects.get_or_create(key="SEPSIS")
    bpa_id, _ = BPAUniqueID.objects.get_or_create(bpa_id=bpaid, project=project)
    return bpa_id


class BPAIDField(fields.Field):
    def __init__(self, *args, **kwargs):
        super(BPAIDField, self).__init__(*args, **kwargs)

    def clean(self, data):
        return get_bpa_id(data[self.column_name])

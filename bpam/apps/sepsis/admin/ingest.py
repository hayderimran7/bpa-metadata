# -*- coding: utf-8 -*-

from libs.ingest_utils import get_date, get_bpa_id  # noqa

from ..models import Host


def get_sex(sex):
    """take a ques at sex"""
    sex = sex.lower().strip()
    if sex.find("male") != -1:
        return "M"
    if sex.find("female") != -1:
        return "F"
    return None


def get_host(row):
    """Make a host """
    # this code here... ¯\_(ツ)_/¯
    id = int(row.get("BPA ID", 0))  #
    description = row.get("Host_description", "")
    location = row.get("Host_location (state, country)", "")
    sex = get_sex(row.get("Host_sex (F/M)", ""))
    age = get_date(row.get("Host_age", None))
    dob = get_date(row.get("Host_DOB (DD/MM/YY)", None))
    disease_outcome = row.get("Host_disease_outcome", None)

    host, _ = Host.objects.get_or_create(id=id,
                                         description=description,
                                         location=location,
                                         sex=sex,
                                         age=age,
                                         dob=dob,
                                         disease_outcome=disease_outcome, )

    return host
# -*- coding: utf-8 -*-

from dateutil.parser import parse as date_parser
from apps.common.models import BPAUniqueID, BPAProject
from apps.common.admin import SequenceFileAdmin

from ..models import Host


def get_date(date):
    """Tries to make a python date"""
    try:
        return date_parser(date)
    except ValueError:
        return None


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


def get_bpa_id(bpaid):
    """get BPA ID"""

    if bpaid is None:
        return None

    bpaid = bpaid.replace("/", ".")
    project, _ = BPAProject.objects.get_or_create(key="SEPSIS")
    bpa_id, _ = BPAUniqueID.objects.get_or_create(bpa_id=bpaid,
                                                  project=project)
    return bpa_id

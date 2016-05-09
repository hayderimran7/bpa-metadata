# -*- coding: utf-8 -*-

import time
import sys
from pprint import pprint

import django
from django.core.management.base import BaseCommand
import requests
from apps.common.models import URLVerification
from apps.melanoma.models import MelanomaSequenceFile
from apps.gbr.models import GBRSequenceFile
from apps.wheat_cultivars.models import CultivarSequenceFile
from apps.wheat_pathogens.models import PathogenSequenceFile
from apps.wheat_pathogens_transcript.models import WheatPathogenTranscriptSequenceFile
from apps.base_metagenomics.models import MetagenomicsSequenceFile
from apps.base_amplicon.models import AmpliconSequenceFile
from libs.logger_utils import get_logger
from django.conf import settings
from datetime import datetime

import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

logger = get_logger(__name__)

SLEEP_TIME = settings.DOWNLOADS_CHECKER_SLEEP  # time to rest between checks


def process_object(sleep_time, session, model, attr_name, url_fn):
    problems = []
    for obj in model.objects.all():
        if getattr(obj, attr_name) is None:
            uv = URLVerification()
            uv.status_ok = False
            uv.checked_at = datetime.now()
            uv.save()
            setattr(obj, attr_name, uv)
        verifier = getattr(obj, attr_name)
        verifier.checked_url = url_fn(obj)
        sys.stderr.write("HEAD {}: ".format(verifier.checked_url))
        sys.stderr.flush()
        r = session.head(verifier.checked_url, verify=False)
        # direct access, or a redirect to the backend. redirects are precise, so
        # we can be sure we'll find the backing file if they exist
        if r.status_code == 200 or r.status_code == 302:
            verifier.status_ok = True
        else:
            verifier.status_ok = False
            verifier.status_note = "Status %d: %s" % (r.status_code, r.text)
            problems.append(obj.filename)
        obj.save()
        sys.stderr.write("%d -> %s\n" % (r.status_code, verifier.status_ok))
        sys.stderr.flush()
        verifier.save()
        time.sleep(sleep_time)

    if problems:
        pprint(problems)
    else:
        print("There were no problems")


def check_gbr(sleep_time):
    logger.info('Checking GBR')
    session = requests.Session()
    session.auth = (settings.DOWNLOADS_CHECKER_USER, settings.DOWNLOADS_CHECKER_PASS)

    try:
        process_object(sleep_time, session, GBRSequenceFile, 'url_verification', lambda obj: obj.get_url())
    except django.db.utils.ProgrammingError as e:
        logger.error(e)


def check_wheat_cultivars(sleep_time):
    logger.info('Checking Wheat Cultivars')
    session = requests.Session()
    try:
        process_object(sleep_time, session, CultivarSequenceFile, 'url_verification', lambda obj: obj.get_url())
    except django.db.utils.ProgrammingError as e:
        logger.error(e)


def check_wheat_pathogens(sleep_time):
    logger.info('Checking Wheat Pathogens')
    session = requests.Session()
    try:
        process_object(sleep_time, session, PathogenSequenceFile, 'url_verification', lambda obj: obj.get_url())
    except django.db.utils.ProgrammingError as e:
        logger.error(e)


def check_wheat_pathogens_transcript(sleep_time):
    logger.info('Checking Wheat Pathogens Transcript')
    session = requests.Session()
    try:
        process_object(sleep_time, session, WheatPathogenTranscriptSequenceFile, 'url_verification', lambda obj: obj.get_url())
    except django.db.utils.ProgrammingError as e:
        logger.error(e)


def check_melanoma(sleep_time):
    logger.info('Checking Melanoma')
    session = requests.Session()
    session.auth = (settings.DOWNLOADS_CHECKER_USER, settings.DOWNLOADS_CHECKER_PASS)
    try:
        process_object(sleep_time, session, MelanomaSequenceFile, 'url_verification', lambda obj: obj.get_url())
    except django.db.utils.ProgrammingError as e:
        logger.error(e)


def check_base_metagenomcis(sleep_time):
    logger.info('Checking BASE Metagenomics')
    session = requests.Session()
    session.auth = (settings.DOWNLOADS_CHECKER_USER, settings.DOWNLOADS_CHECKER_PASS)

    try:
        process_object(sleep_time, session, MetagenomicsSequenceFile, 'url_verification', lambda obj: obj.get_url())
    except django.db.utils.ProgrammingError as e:
        logger.error(e)


def check_base_amplicons(sleep_time):
    logger.info('Checking BASE Amplicons')
    session = requests.Session()
    session.auth = (settings.DOWNLOADS_CHECKER_USER, settings.DOWNLOADS_CHECKER_PASS)

    try:
        process_object(sleep_time, session, AmpliconSequenceFile, 'url_verification', lambda obj: obj.get_url())
    except django.db.utils.ProgrammingError as e:
        logger.error(e)


class Command(BaseCommand):
    help = 'URL Validator'

    def handle(self, *args, **options):

        check_melanoma(SLEEP_TIME)
        check_gbr(SLEEP_TIME)
        check_wheat_cultivars(SLEEP_TIME)
        check_wheat_pathogens(SLEEP_TIME)
        check_wheat_pathogens_transcript(SLEEP_TIME)
        check_base_metagenomcis(SLEEP_TIME)
        check_base_amplicons(SLEEP_TIME)

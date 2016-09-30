# -*- coding: utf-8 -*-

import time
import sys
import requests
import django
from pprint import pprint
from apps.common.models import URLVerification
from datetime import datetime
from django.conf import settings
from django.core.management.base import BaseCommand
from libs.logger_utils import get_logger

from ...models import GenomicsPacBioFile, GenomicsMiseqFile, TranscriptomicsHiseqFile
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


def check(sleep_time):
    logger.info('Checking Sepsis Files')
    session = requests.Session()
    session.auth = (settings.DOWNLOADS_CHECKER_USER, settings.DOWNLOADS_CHECKER_PASS)

    try:
        process_object(sleep_time, session, TranscriptomicsHiseqFile, 'url_verification', lambda obj: obj.get_url())
        process_object(sleep_time, session, GenomicsPacBioFile, 'url_verification', lambda obj: obj.get_url())
        process_object(sleep_time, session, GenomicsMiseqFile, 'url_verification', lambda obj: obj.get_url())
    except django.db.utils.ProgrammingError as e:
        logger.error(e)


class Command(BaseCommand):
    help = 'URL Validator'

    def handle(self, *args, **options):
        check(SLEEP_TIME)

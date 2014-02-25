import time
import sys
from pprint import pprint
import requests

from apps.common.models import URLVerification
from apps.melanoma.models import MelanomaSequenceFile
from apps.gbr.models import GBRSequenceFile
from apps.wheat_cultivars.models import CultivarSequenceFile
from apps.wheat_pathogens.models import PathogenSequenceFile


SLEEP_TIME = 0.0  # time to rest between checks
MELANOMA_PASS = 'm3lan0ma'  # Melanoma http access password

from libs.logger_utils import get_logger


logger = get_logger(__name__)


def process_object(sleep_time, session, model, attr_name, url_fn):
    problems = []
    for obj in model.objects.all():
        if getattr(obj, attr_name) is None:
            uv = URLVerification()
            uv.status_ok = False
            uv.save()
            setattr(obj, attr_name, uv)
        verifier = getattr(obj, attr_name)
        verifier.checked_url = url_fn(obj)
        sys.stderr.write("HEAD %s: " % (verifier.checked_url))
        sys.stderr.flush()
        r = session.head(verifier.checked_url)
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

    pprint(problems)


def check_gbr(sleep_time):
    logger.info('Checking GBR')
    session = requests.Session()
    process_object(sleep_time, session, GBRSequenceFile, 'url_verification', lambda obj: obj.get_url())


def check_wheat_cultivars(sleep_time):
    logger.info('Checking Wheat Cultivars')
    session = requests.Session()
    process_object(sleep_time, session, CultivarSequenceFile, 'url_verification', lambda obj: obj.get_url())


def check_wheat_pathogens(sleep_time):
    logger.info('Checking Wheat Pathogens')
    session = requests.Session()
    process_object(sleep_time, session, PathogenSequenceFile, 'url_verification', lambda obj: obj.get_url())


def check_melanoma(sleep_time):
    logger.info('Checking Melanoma')
    session = requests.Session()
    session.auth = ('bpa', MELANOMA_PASS)
    process_object(sleep_time, session, MelanomaSequenceFile, 'url_verification', lambda obj: obj.get_url())


def run(sleep_time=SLEEP_TIME):
    """
    Pass parameters like below:
    vpython-bpam manage.py runscript url_checker --script-args 0.1
    """
    try:
        sleep_time = float(sleep_time)
    except ValueError:
        sys.stderr.write("sleep_time parameter must be a float.\n")
        sys.stderr.write("Continuing with default value: %f\n" % SLEEP_TIME)
        sleep_time = SLEEP_TIME

    check_melanoma(sleep_time)
    check_gbr(sleep_time)
    check_wheat_cultivars(sleep_time)
    check_wheat_pathogens(sleep_time)



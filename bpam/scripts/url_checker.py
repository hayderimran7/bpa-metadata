from apps.common.models import URLVerification
from apps.melanoma.models import MelanomaSequenceFile
from django.db import transaction
import requests, time, sys

def process_object(session, model, attr_name, url_fn):
    for obj in model.objects.all():
        if getattr(obj, attr_name) is None:
            uv = URLVerification()
            uv.save()
            setattr(obj, attr_name, uv)
        verifier = getattr(obj, attr_name)
        verifier.checked_url = url_fn(obj)
        sys.stderr.write("HEAD %s: " % (verifier.checked_url))
        sys.stderr.flush()
        r = session.head(verifier.checked_url)
        sys.stderr.write("%d\n" % (r.status_code))
        sys.stderr.flush()
        if r.status_code == 200:
            verifier.status_ok = True
        else:
            verifier.status_ok = False
            verifier.status_note = "Status %d: %s" % (r.status_code, r.text)
        obj.save()
        verifier.save()
        time.sleep(0.2) # five requests per second seems fair -- otherwise iVEC killfiles us for a bit

def check_melanoma():
    session = requests.Session()
    session.auth = ('rodney', 'slipslopslap')
    process_object(session, MelanomaSequenceFile, 'url_verification', lambda obj: obj.get_url())

def run():
    check_melanoma()

from apps.common.models import URLVerification
from apps.melanoma.models import MelanomaSequenceFile
from django.db import transaction
import requests

def process_object(model, attr_name, url_fn):
    with transaction.commit_on_success():
        worklist = []
        for obj in model.objects.all():
            if getattr(obj, attr_name) is None:
                setattr(obj, attr_name, URLVerification())
            verifier = getattr(obj, attr_name)
            verifier.url = url_fn(obj)

def run():
    process_object(MelanomaSequenceFile, 'url_verification', lambda obj: obj.get_url())

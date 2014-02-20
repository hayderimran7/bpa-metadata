from datetime import date

from apps.common.models import BPAUniqueID, BPAProject
from logger_utils import get_logger

BPA_ID = "102.100.100"
INGEST_NOTE = "Ingested from GoogleDocs on {0}".format(date.today())

logger = get_logger('BPA ID Utils')


def add_bpa_id(idx, project_name, note=INGEST_NOTE):
    """
    Add a BPA ID
    """

    lbl = BPAUniqueID(bpa_id=idx)
    lbl.project = BPAProject.objects.get(name=project_name)
    lbl.note = note
    lbl.save()
    logger.info("Added BPA Unique ID: " + str(lbl))


def add_id_set(id_set, project_name):
    """
    Add the id's in the given set
    """
    for bpa_id in id_set:
        add_bpa_id(bpa_id, project_name)


def ingest_bpa_ids(data, project_name):
    """
    The BPA ID's are unique
    """

    id_set = set()
    for e in data:
        if isinstance(e, dict):
            bpa_id = e['bpa_id'].strip()
        elif isinstance(e, tuple):
            bpa_id = e.bpa_id.strip()
        if is_good_bpa_id(bpa_id):
            id_set.add(bpa_id)

    add_id_set(id_set, project_name)


def get_bpa_id(bpa_id, project_name, note=INGEST_NOTE):
    """
    Get a BPA ID, if it does not exist, make it
    """

    try:
        bid = BPAUniqueID.objects.get(bpa_id=bpa_id)
    except BPAUniqueID.DoesNotExist:
        logger.info("BPA ID {0} does not exit, adding it".format(bpa_id))
        bid = BPAUniqueID(bpa_id=bpa_id)
        bid.project = BPAProject.objects.get(name=project_name)
        bid.note = note
        bid.save()

    return bid


def is_good_bpa_id(bpa_id):
    """
    Determines if id is a good BPA ID
    """
    bpa_id = bpa_id.strip()
    # empties
    if bpa_id == '':
        return False

    # no BPA prefix
    if bpa_id.find(BPA_ID) == -1:
        return False

    # this function has failed to find a reason why this can't be a BPA ID....
    return True

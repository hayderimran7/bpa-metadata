from datetime import date

from apps.common.models import BPAUniqueID, BPAProject
import logger_utils

BPA_ID = "102.100.100"
INGEST_NOTE = "Ingested from GoogleDocs on {0}".format(date.today())

logger = logger_utils.get_logger('BPA ID Utils')


def ingest_bpa_ids(data, project_key, project_name):
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

    add_id_set(id_set, project_key, project_name)


def get_bpa_id(bpa_idx, project_key, project_name, note=INGEST_NOTE):
    """
    Get a BPA ID, if it does not exist, make it
    It also creates the necessary project.
    """

    if not is_good_bpa_id(bpa_idx):
        logger.warning('Given ID string failed good ID test')
        return None

    project, _ = BPAProject.objects.get_or_create(key=project_key, name=project_name)
    bpa_id, created = BPAUniqueID.objects.get_or_create(bpa_id=bpa_idx, project=project)
    if created:
        logger.info("New BPA ID {0}".format(bpa_idx))
        bpa_id.note = note
        bpa_id.save()

    return bpa_id


def add_id_set(id_set, project_key, project_name):
    """
    Add the id's in the given set
    """
    for bpa_id in id_set:
        get_bpa_id(bpa_id, project_key, project_name)


def is_good_bpa_id(bpa_id):
    """
    Determines if id is a good BPA ID
    """
    bpa_id = bpa_id.strip()
    # empties
    if bpa_id == '':
        logger.warning('Empty string for ID')
        return False

    # no BPA prefix
    if bpa_id.find(BPA_ID) == -1:
        logger.warning('No {0} identifying the string as a BPA ID'.format(BPA_ID))
        return False

    # this function has failed to find a reason why this can't be a BPA ID....
    return True

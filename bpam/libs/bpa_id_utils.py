from datetime import date

from apps.common.models import BPAUniqueID, BPAProject
import logger_utils


BPA_ID = "102.100.100"
INGEST_NOTE = "Ingested from GoogleDocs on {0}".format(date.today())

logger = logger_utils.get_logger(__name__)


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
        if BPAIdValidator(bpa_id).is_valid():
            id_set.add(bpa_id)

    add_id_set(id_set, project_key, project_name)


def get_project(key, name):
    project, created = BPAProject.objects.get_or_create(key=key)
    if created:
        project.name = name
        project.save()
    return project


def get_bpa_id(bpa_idx, project_key, project_name, note=INGEST_NOTE):
    """
    Get a BPA ID, if it does not exist, make it
    It also creates the necessary project.
    :rtype : bpa_id
    """
    validator = BPAIdValidator(bpa_idx)
    if not validator.is_valid():
        return None, validator.valid_report()

    project = get_project(project_key, project_name)
    bpa_id, created = BPAUniqueID.objects.get_or_create(bpa_id=bpa_idx,
                                                        defaults={
                                                            'project': project,
                                                            'note': note
                                                        })
    if created:
        logger.debug("New BPA ID {0}".format(bpa_idx))
    return bpa_id, "OK"


def add_id_set(id_set, project_key, project_name):
    """
    Add the id's in the given set
    """
    for bpa_id in id_set:
        get_bpa_id(bpa_id, project_key, project_name)


class BPAIdValidator(object):
    """
    Given a BPA ID string, check validitty.
    """

    def __init__(self, bpa_id):
        self.bpa_id = bpa_id.strip()
        self.valid_report = None
        self.valid = None

    def get_id(self):
        """
        Return validated ID
        """
        return self.bpa_id

    def is_valid(self):
        if self.valid is None:
            self.is_valid_bpa_id()
        return self.valid

    def is_valid_bpa_id(self):
        """
        Determines if id is a valid BPA ID
        """

        if self.bpa_id is None:
            self.valid_report = 'BPA ID is None'
            self.valid = False

        # empties
        if self.bpa_id == '':
            self.valid_report = 'BPA ID is empty string'
            self.valid = False

        # no BPA prefix
        if self.bpa_id.find(BPA_ID) == -1:
            self.valid_report = 'No "{0}" identifying the string as a BPA ID'.format(BPA_ID)
            self.valid = False

        # this function has failed to find a reason why this can't be a BPA ID....
        self.valid = True

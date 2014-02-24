import csv

import unipath

from libs import ingest_utils, user_helper, logger_utils
from apps.bpaauth.models import BPAUser


logger = logger_utils.get_logger('IngestUsers')

DATA_DIR = unipath.Path(unipath.Path(__file__).ancestor(3), "data/users/")
USERS_FILE = unipath.Path(DATA_DIR, 'current')


def get_data(users_file):
    with open(users_file, 'rb') as contacts:
        fieldnames = ['Project', 'First name', 'Last name', 'Organisation', 'Email', 'Interest', 'Lab']
        reader = csv.DictReader(contacts, fieldnames=fieldnames, restkey='therest')
        return ingest_utils.strip_all(reader)


def filter_contacts(contact):
    """
    If for some reason the contact line is unsuitable, filter it out.
    """
    username = user_helper.make_username(contact)
    if not username:
        return True

    if contact['Project'].strip() == 'Project':
        return True

    return False


def ingest_contacts(users_file):
    """
    Contacts associated with BPA pojects
    """

    for contact in get_data(users_file):
        if filter_contacts(contact):
            continue

        # if the user already exists, she probably is part of several projects so add her to those groups
        username = user_helper.make_username(contact)
        try:
            existing_user = BPAUser.objects.get(username=username)
            group = user_helper.get_group(contact['Project'])
            existing_user.groups.add(group)
            existing_user.save()
        except BPAUser.DoesNotExist:
            user_helper.make_new_user(username, contact)


def run(users_file=USERS_FILE):
    """
    Pass parameters like below:
    vpython-bpam manage.py runscript ingest_users --script-args bpa-users.csv
    """
    ingest_contacts(users_file)


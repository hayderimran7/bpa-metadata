# -*- coding: utf-8 -*-

import csv

from django.core.management.base import BaseCommand, CommandError
from libs import ingest_utils, user_helper, logger_utils
from libs.fetch_data import Fetcher, get_password
from apps.bpaauth.models import BPAUser
from unipath import Path

logger = logger_utils.get_logger(__name__)

METADATA_URL = 'https://downloads-qcif.bioplatforms.com/bpa/bpa_support/users/'  # the folder
BPA_USERS_FILE = 'bpa_users.csv'  # the file
DATA_DIR = Path(ingest_utils.METADATA_ROOT, 'users/')


def get_data(users_file):
    with open(users_file, 'rb') as contacts:
        fieldnames = ['Project', 'First name', 'Last name', 'Organisation', 'Email', 'Interest', 'Lab']
        reader = csv.DictReader(contacts, fieldnames=fieldnames, restkey='therest')
        return ingest_utils.strip_all(reader)


def filter_contacts(contact):
    """ If for some reason the contact line is unsuitable, filter it out. """
    
    username = user_helper.make_username(contact)
    if not username:
        return True

    if contact['Project'].strip() == 'Project':
        return True

    return False


def ingest_contacts(users_file):
    """ Contacts associated with BPA projects """

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


class Command(BaseCommand):
    help = 'Ingest Users'

    def handle(self, *args, **options):
        password = get_password('users')
        fetcher = Fetcher(DATA_DIR, METADATA_URL, auth=('base', password))
        fetcher.fetch(BPA_USERS_FILE)
        ingest_contacts(DATA_DIR + BPA_USERS_FILE)

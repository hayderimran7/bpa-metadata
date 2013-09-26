import pprint
import csv
from datetime import date
import os.path

from apps.bpaauth.models import BPAUser
from apps.common.models import *
from apps.melanoma.models import *
from .utils import *

from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
USERS_FILE = os.path.join(DATA_DIR, 'bpa-users.csv')


def ingest_contacts():
    """
    Contacts associated with BPA pojects
    """

    def get_group(name):
        def get_group_name(raw_group):
            if raw_group != "":
                return raw_group.strip().split()[0]
            else:
                return "Ungrouped"

        nname = get_group_name(name.strip())
        try:
            group = Group.objects.get(name=nname)
        except Group.DoesNotExist:
            print("Group {0} does not exit, adding it".format(nname))
            group = Group(name=nname)
            group.save()

        return group

    def get_data():
        with open(USERS_FILE, 'rb') as contacts:
            fieldnames = ['Project', 'First name', 'Last name', 'Organisation', 'Email', 'Interest', 'Lab']
            reader = csv.DictReader(contacts, fieldnames=fieldnames, restkey='therest')
            return strip_all(reader)

    contacts = get_data()

    def make_username(e):
        """
        Create a username, or none. For this dataset if I can't make a user,
        I ignore this line from the file.
        """
        try:
            name = e['First name'][0] + e['Last name']
            return name
        except IndexError:
            return None

    for contact in contacts:
        pprint.pprint(contact)
        username = make_username(contact)
        if not username:
            continue

        User = get_user_model()
        user = User()
        user.username = username
        user.email = contact['Email']
        user.first_name = contact['First name']
        user.last_name = contact['Last name']
        user.is_staff = False
        user.project = contact['Project']
        user.organisation = contact['Organisation']
        user.interest = contact['Interest']
        user.lab = contact['Lab']

        user.save()
        group = get_group(contact['Project'])
        user.groups.add(group)
        user.save()


def run():
    ingest_contacts()


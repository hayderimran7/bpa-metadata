import pprint
import csv
from datetime import date
import unipath

from apps.bpaauth.models import BPAUser
from apps.common.models import *
from apps.melanoma.models import *
from .utils import *

from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

DATA_DIR = unipath.Path(unipath.Path(__file__).ancestor(3), "data/users/")
USERS_FILE = unipath.Path(DATA_DIR, 'bpa-users.csv')


def format_group_name(name):
    """
    A standard format for the group name
    """
    name = name.strip().replace('_', ' ').title()
    return name


def get_group(name):
    name = format_group_name(name)
    try:
        group = Group.objects.get(name=name)
    except Group.DoesNotExist:
        print("Group {0} does not exit, adding it".format(name))
        group = Group(name=name)
        group.save()

    return group


def get_data():
    with open(USERS_FILE, 'rb') as contacts:
        fieldnames = ['Project', 'First name', 'Last name', 'Organisation', 'Email', 'Interest', 'Lab']
        reader = csv.DictReader(contacts, fieldnames=fieldnames, restkey='therest')
        return strip_all(reader)


def make_username(entry):
    """
    Create a username, or none. For this dataset if I can't make a user,
    I ignore this line from the file.
    """
    try:
        name = entry['First name'][0].lower() + entry['Last name'].lower().replace(' ', '')
        return name
    except IndexError:
        return None


def make_new_user(username, contact):
    user_class = get_user_model()
    user = user_class()
    user.username = username
    user.email = contact['Email']
    user.first_name = contact['First name']
    user.last_name = contact['Last name']
    user.is_staff = False
    user.project = format_group_name(contact['Project'])
    user.organisation = contact['Organisation']
    user.interest = contact['Interest']
    user.lab = contact['Lab']
    user.save()
    group = get_group(contact['Project'])
    user.groups.add(group)
    user.save()


def filter_contacts(contact):
    """
    If for some reason the contact line is unsuitable, filter it out.
    """
    username = make_username(contact)
    if not username:
        return True

    if contact['Project'].strip() == 'Project':
        return True

    return False


def ingest_contacts():
    """
    Contacts associated with BPA pojects
    """

    for contact in get_data():
        if filter_contacts(contact):
            continue

        # if the user already exists, she probably is part of several projects so add her to those groups
        username = make_username(contact)
        try:
            existing_user = BPAUser.objects.get(username=username)
            group = get_group(contact['Project'])
            existing_user.groups.add(group)
            existing_user.save()
        except BPAUser.DoesNotExist:
            make_new_user(username, contact)


def run():
    ingest_contacts()


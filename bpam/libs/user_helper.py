"""
This module provides some user management tools
"""

from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

import logger_utils


logger = logger_utils.get_logger(__name__)


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
        logger.info("Group {0} does not exit, adding it".format(name))
        group = Group(name=name)
        group.save()

    return group


def get_unpacked_user_labels(name):
    """
    Unpack name into user object fields
    """
    try:
        first_name, last_name = name.strip().split()
    except ValueError:
        logger.warning("%s cannot be split", name)
        last_name = name
        first_name = ''

    if len(first_name) > 0:
        username = first_name[0].lower() + last_name.lower()
    else:
        username = last_name.lower()

    return username, first_name, last_name


def get_user(name, email, group_names):
    """
    Get user by email
    """

    if name.strip() == '':
        return None

    username, first_name, last_name = get_unpacked_user_labels(name)
    email = email.strip()

    user_class = get_user_model()
    try:
        user = user_class.objects.get(username=username)
    except user_class.DoesNotExist:
        user = user_class()
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.save()

        for groupn in group_names:
            user.groups.add(get_group(groupn))
            user.save()

    return user


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
    """
    contact is a dictionary providing the necessary values.
    """
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


def get_user_by_email(email):
    """
    See if we can find a contact for this sample based on the email address in the spreadsheet.
    """
    try:
        return get_user_model().objects.get(email=email)
    except get_user_model().DoesNotExist:
        logger.warning('No user found with email: {0}'.format(email))
        return None


def get_user_by_full_name(name):
    """
    See if we can find a contact for this sample based on the user name
    """
    username, first_name, last_name = get_unpacked_user_labels(name)
    try:
        return get_user_model().objects.get(username=username)
    except get_user_model().DoesNotExist:
        logger.warning('No user found with name: {0}'.format(name))
        return None

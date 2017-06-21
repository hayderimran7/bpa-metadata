#!/usr/bin/env python

from django.core.management.base import BaseCommand
from apps.common import models as common


def fix_project_codes():
    sepsis = common.BPAProject.objects.get(name='SEPSIS')
    for obj in common.BPAUniqueID.objects.filter(project__name='Sepsis'):
        obj.project = sepsis
        obj.save()
    old_project = common.BPAProject.objects.get(name='Sepsis')
    old_project.delete()


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        fix_project_codes()

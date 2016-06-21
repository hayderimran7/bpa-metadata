# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from ...models import Metagenomic

class Command(BaseCommand):
    help = 'Deletes all Marine Microbe Metagenomic Sequence Entries'

    def handle(self, *args, **options):
        count, _ = Metagenomic.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(
            'Successfully deleted {} Marine Microbe Metagenomic Entries'.format(count))
            )

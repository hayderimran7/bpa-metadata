# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from ...models import Amplicon


class Command(BaseCommand):
    help = 'Deletes all Marine Microbes Amplicons'

    def handle(self, *args, **options):
        count, _ = Amplicon.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted {} Marine Microbe  Amplicons'.format(count)))

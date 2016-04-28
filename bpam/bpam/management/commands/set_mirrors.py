from django.core.management.base import BaseCommand
from apps.common.models import BPAMirror


class Command(BaseCommand):
    help = "Configure BPA mirrors"

    def handle(self, dataset=[], **options):
        print("Setting the mirrors")
        BPAMirror.objects.all().delete()
        sites = [
            {
                'name': 'CCG',
                'base_url': 'https://downloads.bioplatforms.com'
            },
        ]
        [BPAMirror.objects.get_or_create(order=i, **t) for i, t in enumerate(sites)]
        print("Primary mirror is `%s'." % (repr(BPAMirror.primary())))

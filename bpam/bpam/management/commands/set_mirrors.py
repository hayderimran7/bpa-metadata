from django.core.management.base import BaseCommand
from apps.common.models import BPAMirror


class Command(BaseCommand):
    help = "Configure BPA mirrors"

    def handle(self, dataset=[], **options):
        print("Setting the mirrors")
        BPAMirror.objects.all().delete()
        sites = [
            {
                'name': 'QCIF',
                'base_url': 'https://downloads-qcif.bioplatforms.com/bpa/'
            },
            {
                'name': 'MU',
                'base_url': 'https://downloads-mu.bioplatforms.com/bpa/'
            },
        ]
        [BPAMirror.objects.get_or_create(order=i, **t) for i, t in enumerate(sites)]
        print("Primary mirror is `%s'." % (repr(BPAMirror.primary())))

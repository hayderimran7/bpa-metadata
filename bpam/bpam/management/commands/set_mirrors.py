from django.core.management.base import BaseCommand
from apps.common.models import BPAMirror

SITES = [
    {
        'name': 'QCIF',
        'base_url': 'https://downloads-qcif.bioplatforms.com/bpa/'
    },
]


class Command(BaseCommand):
    help = "Configure BPA mirrors"

    def handle(self, dataset=[], **options):
        print("Setting the mirrors")
        BPAMirror.objects.all().delete()
        [BPAMirror.objects.get_or_create(order=i, **t) for i, t in enumerate(SITES)]
        print("Primary mirror is `%s'." % (repr(BPAMirror.primary())))

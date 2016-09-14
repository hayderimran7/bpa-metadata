from django.core.management.base import BaseCommand
from apps.common.models import CKANServer

SITES = [
    {
        'name': 'bpa-aws1',
        'base_url': 'https://data.bioplatforms.com/'
    },
]


class Command(BaseCommand):
    help = "Configure CKAN servers"

    def handle(self, dataset=[], **options):
        CKANServer.objects.all().delete()
        [CKANServer.objects.get_or_create(order=i, **t) for i, t in enumerate(SITES)]
        print("Primary server is `%s'." % (repr(CKANServer.primary())))

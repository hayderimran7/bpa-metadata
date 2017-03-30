from django.core.management.base import BaseCommand
from django.conf import settings
from apps.common.models import CKANServer


class Command(BaseCommand):
    help = "Configure CKAN servers"

    def handle(self, dataset=[], **options):
        CKANServer.objects.all().delete()
        for i, ckan in enumerate(getattr(settings, 'CKAN_SERVERS', ())):
            CKANServer.objects.create(
                name=ckan.get('name'),
                base_url=ckan.get('base_url'),
                api_key=ckan.get('api_key'),
                order=i)
        self.stdout.write("Primary server is `%s'." % (repr(CKANServer.primary())))

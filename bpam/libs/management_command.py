# -*- coding: utf-8 -*-
import sys
from django.core.management.base import BaseCommand
from libs.logger_utils import get_logger

from apps.common.models import BPAMirror

logger = get_logger(__name__)


class BPACommand(BaseCommand):
    """ BPACommand knows about the mirrors"""

    def log_warn(self, message):
        self.stdout.write(self.style.WARNING(message))

    def log_info(self, message):
        self.stdout.write(message)

    def log_error(self, message):
        self.stdout.write(self.style.ERROR(message))

    def get_base_url(self, options):
        mirror_base_url = BPAMirror.primary().base_url
        if options['mirror']:
            try:
                mirror = BPAMirror.objects.get(name=options['mirror'])
            except BPAMirror.DoesNotExist:
                logger.error('mirror {} specified does not exist'.format(options['mirror']))
                sys.exit()

            mirror_base_url = mirror.base_url
            logger.info('Using mirror {} base url: {}'.format(mirror.name, mirror.base_url))

        return mirror_base_url

    def add_arguments(self, parser):
        mirrors = [str(mirror.name) for mirror in BPAMirror.objects.all()]

        parser.add_argument('--mirror',
                            action='store',
                            dest='mirror',
                            help='Use specified Mirror, pick one from {}'.format(mirrors), )

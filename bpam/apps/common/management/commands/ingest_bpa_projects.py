# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from collections import namedtuple

from apps.common.models import BPAProject
import libs.logger_utils as logger_utils


logger = logger_utils.get_logger(__name__)

Project = namedtuple('Project', 'key name description note')
projects = (
    Project('BASE', 'BASE', 'BASE, Agricultural and Environmental Soil', ''),
    Project('MARINE_MICROBES', 'Marine Microbes', 'Marine Microbes', ''),
    Project('SEPSIS', 'Sepsis', 'Sepsis', ''),
    Project('BARCODE', 'Barcode', 'Organism Barcoding', ''),
    Project('GBR', 'GBR', 'Great Barrier Reef', 'Coral'),
    Project('MELANOMA', 'Melanoma', 'Melanoma', 'Human Melanomas'),
    Project('WHEAT_7A', 'Wheat 7A', 'Wheat Chromosome 7A', ''),
    Project('WHEAT_CULTIVAR', 'Wheat Cultivars', 'Wheat Cultivars', ''),
    Project('WHEAT_PATHOGEN', 'Wheat Pathogens', 'Wheat Pathogens', ''),
)

def truncate():
    from django.db import connection

    cursor = connection.cursor()
    cursor.execute('TRUNCATE TABLE "{0}" CASCADE'.format(BPAProject._meta.db_table))

def set_bpa_projects():
    """ Create BPA Projects """

    truncate()
    for project in projects:
        BPAProject.objects.get_or_create(key=project.key,
                                         name=project.name,
                                         description=project.description,
                                         note=project.note)
        logger.info('BPA Project {0} Added'.format(project.name))


class Command(BaseCommand):
    help = 'BPA Projects'

    def handle(self, *args, **options):
        logger.info('BPA Projects')
        set_bpa_projects()

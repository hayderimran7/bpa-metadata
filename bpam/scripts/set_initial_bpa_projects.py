from collections import namedtuple
import logging
from apps.common.models import BPAProject

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('SetProjects')

Project = namedtuple('Project', 'key name description note')
projects = (
    Project('BASE', 'BASE', 'BASE, Agricultural and Environmental Soil', ''),
    Project('GBR', 'GBR', 'Great Barrier Reef', 'Coral'),
    Project('MELANOMA', 'Melanoma', 'Melanoma', 'Human Melanomas'),
    Project('WHEAT_7A', 'Wheat 7A', 'Wheat Chromosome 7A', ''),
    Project('WHEAT_CULTIVAR', 'Wheat Cultivars', 'Wheat Cultivars', ''),
    Project('WHEAT_PATHOGEN', 'Wheat Pathogens', 'Wheat Pathogens', ''),
)


def set_bpa_projects():
    """
    Set BPA Projects if not set already. This is for new DB's
    """

    for project in projects:
        try:
            BPAProject.objects.get(key=project.key)
        except BPAProject.DoesNotExist:
            proj = BPAProject(key=project.key,
                              name=project.name,
                              description=project.description,
                              note=project.note
                              )
            proj.save()
            logger.info('Added project {0}'.format(proj.name))


def run():
    logger.info('BPA Projects')
    set_bpa_projects()


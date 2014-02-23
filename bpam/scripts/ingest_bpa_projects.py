from collections import namedtuple

from apps.common.models import BPAProject
import libs.logger_utils as logger_utils


logger = logger_utils.get_logger('Add Projects')

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
        BPAProject.objects.get_or_create(key=project.key,
                                         name=project.name,
                                         description=project.description,
                                         note=project.note)
        logger.info('BPA Project {0} Added'.format(project.name))


def run():
    logger.info('BPA Projects')
    set_bpa_projects()


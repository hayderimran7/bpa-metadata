from libs.logger_utils import get_logger
from apps.base_vocabulary.contextual_controlled_vocabularies import LandUseVocabulary
from apps.base_vocabulary.models import LandUse

logger = get_logger(__name__)

import pprint

def run():
    def add(section, parent=None):
        if isinstance(section, tuple):
            for sect in section:
                parent = add(sect, parent)

        if isinstance(section, str):
            logger.warning(section)
            return LandUse.objects.create(order=0, description=section, parent=parent)

    for entry in LandUseVocabulary:
        add(entry)





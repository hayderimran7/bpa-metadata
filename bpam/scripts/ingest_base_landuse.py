# -*- coding: utf-8 -*-

from libs.logger_utils import get_logger
from apps.base_vocabulary.contextual_controlled_vocabularies import LandUseVocabulary
from apps.base_vocabulary.models import LandUse

# import logging
# logging.basicConfig(level=logging.INFO)
logger = get_logger(__name__)


def run():
    for u1 in LandUseVocabulary:
        parent_name_u1 = u1[0]
        logger.info('Adding %s', parent_name_u1)
        parent_u1, created = LandUse.objects.get_or_create(order=0, description=parent_name_u1)
        for u2 in u1[1:]:
            parent_name_u2 = u2[0]
            logger.info('Adding %s', parent_name_u2)
            parent_u2, created = LandUse.objects.get_or_create(order=0, description=parent_name_u2, parent=parent_u1)
            for u3 in u2[1]:
                logger.info('Adding %s', u3)
                LandUse.objects.get_or_create(order=0, description=u3, parent=parent_u2)

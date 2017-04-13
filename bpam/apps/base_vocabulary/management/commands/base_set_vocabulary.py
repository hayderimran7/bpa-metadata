# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from libs.logger_utils import get_logger
from apps.base_vocabulary.contextual_controlled_vocabularies import (
    AustralianSoilClassificationVocabulary,
    DrainageClassificationVocabulary,
    BroadVegetationTypeVocabulary,
    EcologicalZoneVocabulary,
    FAOSoilClassificationVocabulary,
    HorizonClassificationVocabulary,
    LandUseVocabulary,
    ProfilePositionVocabulary,
    SoilColourVocabulary,
    TillageClassificationVocabulary)
from apps.base_vocabulary.models import (
    AustralianSoilClassification,
    BroadVegetationType,
    DrainageClassification,
    FAOSoilClassification,
    GeneralEcologicalZone,
    HorizonClassification,
    LandUse,
    ProfilePosition,
    SoilColour,
    SoilTexture,
    TillageType)


# import logging
# logging.basicConfig(level=logging.INFO)
logger = get_logger(__name__)


def _texture():
    """Set Soil texture Classification"""
    logger.info(_texture.__doc__)
    for texture, description in SoilColourVocabulary:
        SoilTexture.objects.get_or_create(texture=texture, description=description)


def _drainage():
    """Set Drainage Classification"""
    logger.info(_drainage.__doc__)
    for drainage, description in DrainageClassificationVocabulary:
        DrainageClassification.objects.get_or_create(drainage=drainage, description=description)


def _soilcolour():
    """Set Soil Colour Vocabulary """
    logger.info(_soilcolour.__doc__)
    for colour, code in SoilColourVocabulary:
        SoilColour.objects.get_or_create(colour=colour, code=code)


def _tillage():
    """Set Tillage Classification Vocabulary """
    logger.info(_tillage.__doc__)
    for tillage, description in TillageClassificationVocabulary:
        TillageType.objects.get_or_create(tillage=tillage, description=description)


def _aus_soil():
    """ Australian Soil Classification """
    logger.info(_aus_soil.__doc__)
    for classification, note in AustralianSoilClassificationVocabulary:
        logger.info(classification)
        soil, _ = AustralianSoilClassification.objects.get_or_create(classification=classification)
        soil.note = note
        soil.save()


def _fao_soil():
    """ FAO Soil Classification """
    logger.info(_fao_soil.__doc__)
    for classification, note in FAOSoilClassificationVocabulary:
        logger.info(classification)
        soil, _ = FAOSoilClassification.objects.get_or_create(classification=classification)
        soil.note = note
        soil.save()


def _profileposition():
    """Set Profile Position Vocabulary """

    logger.info(_profileposition.__doc__)
    for position, note in ProfilePositionVocabulary:
        logger.info(position)
        ProfilePosition.objects.get_or_create(position=position)


def _broad_vegetation_type():
    """Set Broadvegetation Type Vocabulary """
    logger.info(_broad_vegetation_type.__doc__)
    for vegetation, note in BroadVegetationTypeVocabulary:
        logger.info(vegetation)
        veg, _ = BroadVegetationType.objects.get_or_create(vegetation=vegetation)
        veg.note = note
        veg.save()


def _ecozone():
    """Set Ecological Zone Vocabulary """
    logger.info(_ecozone.__doc__)
    for description, note in EcologicalZoneVocabulary:
        logger.info(description)
        zone, _ = GeneralEcologicalZone.objects.get_or_create(description=description)
        zone.note = note
        zone.save()


def _horizon():
    """Set Horizon Classification Vocabulary """
    logger.info(_horizon.__doc__)
    for c, description in HorizonClassificationVocabulary:
        logger.info(description)
        HorizonClassification.objects.get_or_create(horizon=c, description=description)


def _landuse():
    """ Land Use vocabulary """
    logger.info(_landuse.__doc__)
    for u1 in LandUseVocabulary:
        parent_name_u1 = u1[0]
        logger.info('Adding %s', parent_name_u1)
        parent_u1, _ = LandUse.objects.get_or_create(order=0, description=parent_name_u1)
        for u2 in u1[1:]:
            parent_name_u2 = u2[0]
            logger.info('Adding %s', parent_name_u2)
            parent_u2, created = LandUse.objects.get_or_create(order=0, description=parent_name_u2, parent=parent_u1)
            for u3 in u2[1]:
                logger.info('Adding %s', u3)
                LandUse.objects.get_or_create(order=0, description=u3, parent=parent_u2)


class Command(BaseCommand):
    help = 'Ingest BASE Land Use'

    def handle(self, *args, **options):
        _landuse()
        _broad_vegetation_type()
        _ecozone()
        _horizon()
        _profileposition()
        _aus_soil()
        _fao_soil()
        _tillage()
        _soilcolour()
        _drainage()
        _texture()

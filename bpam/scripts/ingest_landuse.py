from libs.logger_utils import get_logger
from apps.base_vocabulary.contextual_controlled_vocabularies import LandUseVocabulary
from apps.base_vocabulary.models import LandUse

logger = get_logger(__name__)

def run():
    for u1 in LandUseVocabulary:
        parent_name_u1 = u1[0]
        parent_u1 = LandUse.objects.create(order=0, description=parent_name_u1)
        for u2 in u1[1:]:
            parent_name_u2 = u2[0]
            parent_u2 = LandUse.objects.create(order=0, description=parent_name_u2, parent=parent_u1)
            for u3 in u2[1]:
                LandUse.objects.create(order=0, description=u3, parent=parent_u2)









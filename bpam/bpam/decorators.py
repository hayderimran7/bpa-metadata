from functools import wraps
import logging

from django.conf import settings

from .views import GoToCKANView


logger = logging.getLogger(__name__)


def DEBUG_ONLY_VIEW(view):

    @wraps(view)
    def wrapper(*args, **kwargs):
        if settings.DEBUG:
            return view(*args, **kwargs)
        return GoToCKANView.as_view()(*args, **kwargs)

    return wrapper

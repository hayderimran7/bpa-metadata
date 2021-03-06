from functools import wraps
import logging

from django.conf import settings

from .views import GoToCKANView


logger = logging.getLogger(__name__)


def DEBUG_ONLY_VIEW(view):  # noqa: N802 - I want this decorator to be all uppercase

    @wraps(view)
    def wrapper(*args, **kwargs):
        if settings.DEBUG:
            return view(*args, **kwargs)
        return GoToCKANView.as_view()(*args, **kwargs)

    return wrapper

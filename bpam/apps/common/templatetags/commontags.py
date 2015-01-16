from django import template
from django.conf import settings

register = template.Library()


# settings value
@register.simple_tag
def bpam_version():
    return getattr(settings, 'BPA_VERSION', '')

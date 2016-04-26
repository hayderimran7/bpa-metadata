from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def bpam_version():
    return getattr(settings, 'BPA_VERSION', 'NO-VERSION')

@register.simple_tag
def sample_url(mirror, sample):
    return sample.get_url(mirror)

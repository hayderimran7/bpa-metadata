from django import template
from django.conf import settings
from django.core.urlresolvers import reverse

from ..models import CKANServer

register = template.Library()


@register.simple_tag
def bpam_version():
    return getattr(settings, 'BPA_VERSION', 'NO-VERSION')


@register.simple_tag
def sample_url(mirror, sample):
    return sample.get_url(mirror)


@register.simple_tag
def ckan_server_url():
    return reverse('ckan:index')

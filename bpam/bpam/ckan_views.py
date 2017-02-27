import ckanapi
from collections import Counter
from hashlib import sha1
import logging
import operator
import re

from django.conf import settings
from django.core.cache import caches
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.views.decorators.cache import cache_page
from revproxy.views import ProxyView
from revproxy import utils

from apps.common.models import CKANServer


# For responses larger than this the revproxy will return a streaming response.
# We can't cache streaming responses so we have to increase this value.
utils.MIN_STREAMING_LENGTH = 20 * 1024 * 1024


logger = logging.getLogger(__name__)


class CKANProxyView(ProxyView):
    BLACKLIST = [re.compile(x) for x in (
        r'\.\.',
    )]

    WHITELIST = [re.compile(x) for x in (
        # r'^api/3/action/package_search\?.*wheat-pathogens.*',
        r'^api/3/action/package_search\?',
        r'^api/3/action/package_show\?',
        r'^api/3/action/resource_search\?',
        r'^api/3/action/organization_show\?',
    )]

    @property
    def upstream(cls):
        server = CKANServer.primary()
        return server.base_url

    def get_request_headers(self):
        headers = super(CKANProxyView, self).get_request_headers()
        server = CKANServer.primary()
        headers['Authorization'] = server.api_key
        logger.debug(headers)
        return headers

    def access_control(self, path):
        logger.debug('PATH is %s', path)

        for rule in self.BLACKLIST:
            if rule.match(path):
                raise PermissionDenied()

        for rule in self.WHITELIST:
            if rule.match(path):
                return

        raise PermissionDenied()

    def dispatch(self, request, path):
        path_and_querystring = path
        if request.META.get('QUERY_STRING'):
            path_and_querystring = '%s?%s' % (path, request.META.get('QUERY_STRING'))
        self.access_control(path_and_querystring)

        def f(request, path):
            return super(CKANProxyView, self).dispatch(request, path)

        ckan_timeout = settings.CKAN_CACHE_TIMEOUT

        # TODO maybe better cache selection
        # For example write own cacher that on set checks the size of the response.
        # and chooses the cache to store it in based on it.
        # Then on get it will check both caches...
        # cached = cache_page(ckan_timeout)(f)
        # if 'organization_show' in path:
        #    cached = cache_page(ckan_timeout, cache='big_objects')(f)

        # For now put all CKAN responses into the big_objects cache
        cached = cache_page(ckan_timeout, cache='big_objects')(f)

        return cached(request, path)



@cache_page(settings.CKAN_CACHE_TIMEOUT, cache='big_objects')
def ckan_resources(request, org_name, package_type):
    resources = get_resources(org_name, package_type)
    return JsonResponse({
        'success': True,
        'data': resources,
    })


@cache_page(settings.CKAN_CACHE_TIMEOUT, cache='big_objects')
def ckan_resources_count(request, org_name, package_type):
    package_ids = [p['id'] for p in get_org(org_name)['packages'] if p['type'] == package_type]

    return JsonResponse({
        'success': True,
        'count': len(package_ids),
    })


def ckan_resources_count_by_amplicon(request):
    cnt = Counter(p.get('amplicon') for p in get_org('bpa-marine-microbes')['packages'] if p['type'] == 'mm-genomics-amplicon')

    counts = dict(cnt.most_common())
    counts['all'] = reduce(operator.add, counts.values())

    return JsonResponse({
        'success': True,
        'data': counts,
    })


def get_ckan():
    server = CKANServer.primary()
    return ckanapi.RemoteCKAN(server.base_url, apikey=server.api_key)


def get_org(org_name):
    cache = caches['big_objects']
    ckan = get_ckan()

    key = sha1('ckan_organization_show:${id},include_datasets=True'.format(id=org_name)).hexdigest()
    org = cache.get(key)
    if org is None:
        org = ckan.action.organization_show(id=org_name, include_datasets=True)
        cache.set(key, org)
    return org


def get_resources(org_name, package_type):
    ckan = get_ckan()
    package_ids = [p['id'] for p in get_org(org_name)['packages'] if p['type'] == package_type]

    packages = [ckan.action.package_show(id=pid, include_datasets=True) for pid in package_ids]

    resources = [dict(r.items() + [('package', {k: v for k, v in p.items() if k != 'resources'})])
                 for p in packages
                 for r in p['resources']]

    return resources

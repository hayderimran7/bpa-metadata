import ckanapi
from collections import Counter
from hashlib import sha1
import json
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

    # TODO review, we've opened up too much?
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
        return headers

    def access_control(self, path):
        for rule in self.BLACKLIST:
            if rule.match(path):
                raise PermissionDenied()

        for rule in self.WHITELIST:
            if rule.match(path):
                return

        raise PermissionDenied()

    def dispatch(self, request, path):
        logger.debug('Proxying %s', path)
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


# To review
# I disabled all per-page caching to make it obvious that we cache on the ckan requests,
# namely organizations_show and get_all_resources. All the other views are reusing that data
# so caching per page isn't that important.


#@cache_page(settings.CKAN_CACHE_TIMEOUT, cache='big_objects')
def ckan_packages(request, org_name, package_type=None):
    amplicon = request.GET.get('amplicon')
    org = get_org(org_name)
    if package_type is None:
        packages = org['packages']
    else:
        packages = [p for p in org['packages'] if p['type'] == package_type]

    if amplicon:
        packages = [p for p in packages if p.get('amplicon', '').lower() == amplicon.lower()]

    return JsonResponse({
        'success': True,
        'data': packages,
    })


#@cache_page(settings.CKAN_CACHE_TIMEOUT, cache='big_objects')
def ckan_resources(request, org_name, package_type):
    amplicon = request.GET.get('amplicon')
    resources = [r for r in get_all_resources(org_name) if r['package']['type'] == package_type]
    if amplicon:
        resources = [r for r in resources if r.get('amplicon', '').lower() == amplicon.lower()]

    return JsonResponse({
        'success': True,
        'data': resources,
    })


#@cache_page(settings.CKAN_CACHE_TIMEOUT, cache='big_objects')
def ckan_packages_count(request, org_name):
    org = get_org(org_name)

    return JsonResponse({
        'success': True,
        'data': len(org['packages']),
    })


def mm_project_overview_count(request):
    org = get_org('bpa-marine-microbes')

    cnt = Counter(p['type'] for p in org['packages'])
    amplicons_cnt = Counter(p['amplicon'] for p in org['packages'] if p['type'] == 'mm-genomics-amplicon')

    counts = dict(cnt.most_common())
    counts['amplicons'] = dict(amplicons_cnt.most_common())

    return JsonResponse({
        'success': True,
        'data': counts,
    })


def stemcell_project_overview_count(request):
    org = get_org('bpa-stemcells')

    cnt = Counter(p['type'] for p in org['packages'])
    counts = dict(cnt.most_common())

    return JsonResponse({
        'success': True,
        'data': counts,
    })


#@cache_page(settings.CKAN_CACHE_TIMEOUT, cache='big_objects')
def ckan_resources_count(request, org_name):
    resources = get_all_resources(org_name)
    cnt = Counter(r['package']['type'] for r in resources)
    sample_ids = set(r['package']['id'] for r in resources)

    counts = dict(cnt.most_common())
    counts['samples'] = len(sample_ids)

    return JsonResponse({
        'success': True,
        'data': counts,
    })


#@cache_page(settings.CKAN_CACHE_TIMEOUT, cache='big_objects')
def ckan_resources_count_by_amplicon(request):
    resources = [r for r in get_all_resources('bpa-marine-microbes') if r['package']['type'] == 'mm-genomics-amplicon']

    cnt = Counter(r.get('amplicon') for r in resources)

    counts = dict(cnt.most_common())
    counts['all'] = reduce(operator.add, counts.values())

    return JsonResponse({
        'success': True,
        'data': counts,
    })


# CKAN "services"


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


def get_all_resources(org_name):
    cache = caches['big_objects']
    ckan = get_ckan()

    key = sha1('get_all_resources:${org_name}'.format(org_name=org_name)).hexdigest()
    resources = cache.get(key)
    if resources is not None:
        logger.debug('Cached get_all_resources(%s)', org_name)
        return resources

    org = get_org(org_name)
    package_ids = [p['id'] for p in get_org(org_name)['packages']]

    packages = []
    for pid in package_ids:
        try:
            packages.append(ckan.action.package_show(id=pid, include_datasets=True))
        except ckanapi.errors.CKANAPIError:
            logger.exception('Error trying to show package %s' % pid)

    resources = [dict(r.items() + [('package', {k: v for k, v in p.items() if k != 'resources'})])
                 for p in packages
                 for r in p['resources']]


    cache.set(key, resources)

    return resources


# Currently, unused, but leaving it because we might go back this
def get_resources(org_name, package_type, filter_fn=lambda x: True):
    ckan = get_ckan()
    # package_ids = [p['id'] for p in get_org(org_name)['packages'] if p['type'] == package_type]
    package_ids = [p['id'] for p in get_org(org_name)['packages'] if p['type'] == package_type and filter_fn(p)]

    packages = []
    for pid in package_ids:
        try:
            packages.append(ckan.action.package_show(id=pid, include_datasets=True))
        except ckanapi.errors.CKANAPIError:
            logger.exception('Error trying to show package %s' % pid)

    resources = [dict(r.items() + [('package', {k: v for k, v in p.items() if k != 'resources'})])
                 for p in packages
                 for r in p['resources']]

    return resources

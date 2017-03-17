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


logger = logging.getLogger(__name__)


# See datatables.net serverSide documentation for details
COLUMN_PATTERN = re.compile(r'^columns\[(\d+)\]\[(data|name|searchable|orderable)\]$')
ORDERING_PATTERN = re.compile(r'^order\[(\d+)\]\[(dir|column)\]$')
SEARCH_PATTERN = re.compile(r'^search\[(value|regex)\]$')


# TODO Review
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

    draw = _int_get_param(request, 'draw')
    start = _int_get_param(request, 'start')
    length = _int_get_param(request, 'length')

    column_definitions = _extract_column_definitions(request)
    ordering = _extract_ordering(request)
    search_params = _extract_search_params(request)

    package_filter = _make_search_filters(search_params, column_definitions)
    filtered_packages = packages if package_filter is None else filter(package_filter, packages)
    filtered_packages_count = len(filtered_packages)

    for order in reversed(ordering):
        key_fn, should_reverse = _make_sort_params(order, column_definitions)
        if key_fn is not None:
            filtered_packages = sorted(filtered_packages, key=key_fn, reverse=should_reverse)

    if start is not None and length is not None:
        filtered_packages = filtered_packages[int(start):int(start)+int(length)]

    return JsonSuccess({
        'draw': draw,
        'data': filtered_packages,
        'recordsTotal': len(packages),
        'recordsFiltered': filtered_packages_count,
     })


#@cache_page(settings.CKAN_CACHE_TIMEOUT, cache='big_objects')
def ckan_resources(request, org_name, package_type):
    amplicon = request.GET.get('amplicon')
    logger.debug(list(set(r['package']['type'] for r in get_all_resources(org_name))))
    resources = [r for r in get_all_resources(org_name) if r['package']['type'] == package_type]
    if amplicon:
        resources = [r for r in resources if r.get('amplicon', '').lower() == amplicon.lower()]

    draw = _int_get_param(request, 'draw')
    start = _int_get_param(request, 'start')
    length = _int_get_param(request, 'length')

    total_records = len(resources)

    # TODO apply filter (search)
    filtered_records = len(resources)

    column_definitions = _extract_column_definitions(request)
    ordering = _extract_ordering(request)

    for order in reversed(ordering):
        key_fn, should_reverse = _make_sort_params(order, column_definitions)
        if key_fn is not None:
            resources = sorted(resources, key=key_fn, reverse=should_reverse)

    if start is not None and length is not None:
        resources = resources[int(start):int(start)+int(length)]

    logger.debug('resources is now %s', len(resources))

    return JsonSuccess({
        'draw': draw,
        'data': resources,
        'recordsTotal': total_records,
        'recordsFiltered': filtered_records,
    })


def ckan_package_show(request, package_id):
    ckan = get_ckan()

    package = ckan.call_action('package_show', {'id': package_id})

    return JsonSuccess.data(package)



def ckan_packages_count(request, org_name=None):
    ckan = get_ckan()

    packages_count = ckan.call_action('package_search', {'facet.field': ['organization'], 'include_private': True, 'rows': 0})
    path = ['facets', 'organization']
    if org_name is not None:
        path.append(org_name)

    return JsonSuccess.data(get_in(packages_count, path))


def mm_project_overview_count(request):
    org = get_org('bpa-marine-microbes')

    cnt = Counter(p['type'] for p in org['packages'])
    amplicons_cnt = Counter(p['amplicon'] for p in org['packages'] if p['type'] == 'mm-genomics-amplicon')

    counts = dict(cnt.most_common())
    counts['amplicons'] = dict(amplicons_cnt.most_common())

    return JsonSuccess.data(counts)


def stemcell_project_overview_count(request):
    org = get_org('bpa-stemcells')

    cnt = Counter(p['type'] for p in org['packages'])
    counts = dict(cnt.most_common())

    return JsonSuccess.data(counts)


#@cache_page(settings.CKAN_CACHE_TIMEOUT, cache='big_objects')
def ckan_resources_count(request, org_name):
#    TODO should switch to the new API
#    ckan = get_ckan()

#    response = ckan.action.resource_search(query='resource_type:%s' % org_name, limit=0)
#    data = response.get('count')

    resources = get_all_resources(org_name)
    cnt = Counter(r['package']['type'] for r in resources)
    sample_ids = set(r['package']['id'] for r in resources)

    counts = dict(cnt.most_common())
    counts['samples'] = len(sample_ids)

    return JsonSuccess.data(counts)


#@cache_page(settings.CKAN_CACHE_TIMEOUT, cache='big_objects')
def OLD_ckan_resources_count(request, org_name):
    resources = get_all_resources(org_name)
    cnt = Counter(r['package']['type'] for r in resources)
    sample_ids = set(r['package']['id'] for r in resources)

    counts = dict(cnt.most_common())
    counts['samples'] = len(sample_ids)

    return JsonSuccess.data(counts)


#@cache_page(settings.CKAN_CACHE_TIMEOUT, cache='big_objects')
def ckan_resources_count_by_amplicon(request):
    resources = [r for r in get_all_resources('bpa-marine-microbes') if r['package']['type'] == 'mm-genomics-amplicon']

    cnt = Counter(r.get('amplicon') for r in resources)

    counts = dict(cnt.most_common())
    counts['all'] = reduce(operator.add, counts.values())

    return JsonSuccess.data(counts)


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


# Implementation


def _int_get_param(request, param_name):
    param = request.GET.get(param_name)
    try:
        return int(param) if param is not None else None
    except ValueError:
        return None

def _extract_column_definitions(request):
    columns = []
    for k in request.GET:
        match = COLUMN_PATTERN.match(k)
        if match is not None:
            index = int(match.groups()[0])
            attr = match.groups()[1]
            for i in range(index - len(columns) + 1):
                columns.append({})
            columns[index][attr] = request.GET.get(k)
    return columns


def _extract_ordering(request):
    ordering = []
    for k in request.GET:
        match = ORDERING_PATTERN.match(k)
        if match is not None:
            index = int(match.groups()[0])
            attr = match.groups()[1]
            for i in range(index - len(ordering) + 1):
                ordering.append({})
            value = request.GET.get(k)
            if attr == 'column':
                value = int(value)
            ordering[index][attr] = value
    return ordering


def _extract_search_params(request):
    # Note: search[regex] not supported. I don't think it is needed.
    return {SEARCH_PATTERN.match(k).groups()[0]: v for k, v in request.GET.items() if SEARCH_PATTERN.match(k)}


def _make_search_filters(search_params, col_defs):
    searched_words = search_params.get('value', '').strip().split()
    if len(searched_words) == 0:
        return None
    searchable_columns = [c.get('data') for c in col_defs if c.get('searchable') == 'true']
    icontains = lambda term, text: term.lower() in text.lower()

    def each_word_exists_in_at_least_one_column(package):
        return all(any(icontains(w, package.get(c, '')) for c in searchable_columns) for w in searched_words)

    return each_word_exists_in_at_least_one_column


def _make_sort_params(order, column_definitions):
    if order['column'] >= len(column_definitions):
        return None, None
    column = column_definitions[order['column']]
    def getter(d):
        return get_in(d, column.get('data', '').split('.'))

    return getter, order['dir'] == 'desc'


def get_in(root_dict, keys):
    return reduce(lambda d, key: d.get(key) if d is not None else None, keys, root_dict)


class JsonSuccess(JsonResponse):
    def __init__(self, data, *args, **kwargs):
        resp = data
        if isinstance(data, dict):
            resp = data.copy()
            resp['success'] = True

        super(JsonSuccess, self).__init__(resp, *args, **kwargs)

    @classmethod
    def data(cls, data):
        return JsonSuccess({'data': data})


# Disabled the proxy (in urls.py) for now, leaving the code for a while in case we will need it


# For responses larger than this the revproxy will return a streaming response.
# We can't cache streaming responses so we have to increase this value.
utils.MIN_STREAMING_LENGTH = 20 * 1024 * 1024


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

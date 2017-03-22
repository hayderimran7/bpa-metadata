import ckanapi
from collections import Counter, OrderedDict
from functools import wraps
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


# Could grab these with a facet.pivot Solr query, but it is unsupported in the CKAN API :-(
CKAN_RESOURCE_TYPES = {
        'bpa-marine-microbes':
            ('mm-metagenomics', 'mm-metatranscriptome', 'mm-genomics-amplicon'),
        'bpa-wheat-pathogens-genomes':
            ('wheat-pathogens',),
        'bpa-stemcells':
            ('stemcells-transcriptomics', 'stemcells-smallrna', 'stemcells-singlecellrnaseq'),
}


def exceptions_to_json_err(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        try:
            return view(*args, **kwargs)
        except Exception as e:
            logger.exception('Error while running view %s', view.__name__)
            return JsonError.from_exception(e)

    return wrapped_view


@exceptions_to_json_err
def package_list(request, org_name, resource_type=None):
    amplicon = request.GET.get('amplicon')

    if resource_type is None:
        packages = ckan_get_packages_by_organisation(org_name)
    else:
        packages = ckan_get_packages_by_resource_type(resource_type)

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


@exceptions_to_json_err
def resource_list(request, org_name, resource_type):
    amplicon = request.GET.get('amplicon')
    resources = ckan_get_resources(resource_type)

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

    return JsonSuccess({
        'draw': draw,
        'data': resources,
        'recordsTotal': total_records,
        'recordsFiltered': filtered_records,
    })


@exceptions_to_json_err
def package_detail(request, package_id):
    ckan = get_ckan()
    package = ckan.call_action('package_show', {'id': package_id})

    return JsonSuccess.data(package)


# Used by landing page to display how many samples we have in each project
@exceptions_to_json_err
def packages_count_by_organisation(request, org_name=None):
    return JsonSuccess.data(ckan_packages_count_by_organisation(org_name))


# Used by each projects page to display how may samples and files (of different types) we have
@exceptions_to_json_err
def org_packages_and_resources_count(request, org_name):
    counts = {k: ckan_get_resources_count(k) for k in CKAN_RESOURCE_TYPES.get(org_name, {})}
    sample_counts = ckan_packages_count_by_organisation(org_name)

    counts['samples'] = sample_counts

    return JsonSuccess.data(counts)


# We use this view currently only to get the amplicons for Marine Microbes.
# Displays the number of files by amplicon types ie. 16S, A16S, 18S
@exceptions_to_json_err
def amplicon_resources_count(request):
    counts = ckan_amplicon_resources_count()

    return JsonSuccess.data(counts)


@exceptions_to_json_err
def mm_project_overview_count(request):
    all_package_counts = ckan_packages_count_by_resource_type()
    counts = {k: v for k, v in all_package_counts.items() if k in CKAN_RESOURCE_TYPES['bpa-marine-microbes']}

    amplicon_counts = ckan_amplicon_packages_count('mm-genomics-amplicon')
    counts['amplicons'] = amplicon_counts


    return JsonSuccess.data(counts)


@exceptions_to_json_err
def stemcell_project_overview_count(request):
    all_package_counts = ckan_packages_count_by_resource_type()
    counts = {k: v for k, v in all_package_counts.items() if k in CKAN_RESOURCE_TYPES['bpa-stemcells']}

    return JsonSuccess.data(counts)


# CKAN "services"


def get_ckan():
    server = CKANServer.primary()
    return ckanapi.RemoteCKAN(server.base_url, apikey=server.api_key)


def ckan_get_amplicon_resources_count(resource_type, amplicon_type):
    ckan = get_ckan()

    args = OrderedDict((
        ('query', ['resource_type:%s' % resource_type, 'amplicon:%s' % amplicon_type]),
        ('include_private', True),
        ('limit', 0),
    ))
    result = ckan.call_action('resource_search', args)

    return result['count']


def ckan_get_resources_count(resource_type):
    ckan = get_ckan()

    args = OrderedDict((
        ('query', 'resource_type:%s' % resource_type),
        ('include_private', True),
        ('limit', 0),
    ))
    result = ckan.call_action('resource_search', args)

    return result['count']

    packages = ckan_get_packages_by_resource_type(resource_type)
    resources = [dict(r.items() + [('package', {k: v for k, v in p.items() if k != 'resources'})])
                 for p in packages
                 for r in p['resources']]

    return resources


def ckan_get_resources(resource_type):
    # Fetching all resources by getting all packages then turn the resources inside-out
    # ie. putting the resources at top-level and nest their package inside them
    # Another strategy would be to fetch only the needed resources and then fetch the associated packages
    # with show_package (it will result in 1 request per resource, but it might be faster overall)

    packages = ckan_get_packages_by_resource_type(resource_type)
    resources = [dict(r.items() + [('package', {k: v for k, v in p.items() if k != 'resources'})])
                 for p in packages
                 for r in p['resources']]

    return resources


def ckan_packages_count_by_organisation(org_name=None):
    ckan = get_ckan()

    args = OrderedDict((
        ('facet.field', ['organization']),
        ('include_private', True),
        ('rows', 0),
    ))
    result = ckan.call_action('package_search', args)

    path = ['facets', 'organization']
    if org_name is not None:
        path.append(org_name)

    return get_in(result, path)


def ckan_packages_count_by_resource_type():
    ckan = get_ckan()

    args = OrderedDict((
        ('facet.field', ['type']),
        ('include_private', True),
        ('rows', 0),
    ))
    result = ckan.call_action('package_search', args)

    return get_in(result, ['facets', 'type'])


def ckan_amplicon_packages_count(resource_type):
    ckan = get_ckan()

    args = OrderedDict((
        ('q', 'type:%s' % resource_type),
        ('facet.field', ['amplicon']),
        ('include_private', True),
        ('rows', 0),
    ))
    result = ckan.call_action('package_search', args)

    return get_in(result, ['facets', 'amplicon'])


def ckan_amplicon_resources_count():
    # This implementation would be better, but unfortunately the resource search always
    # uses contains instead of exact matching, so when looking for "16S" amplicons we
    # also get the "A16S" amplicons back.
    # Leaving the code here because we might use it later on.
    #
    # AMPLICON_TYPES = ('16S', '18S', 'A16S')
    #
    # counts = {at: ckan_get_amplicon_resources_count('mm-genomics-amplicon', at)
    #           for at in AMPLICON_TYPES}

    resources = ckan_get_resources('mm-genomics-amplicon')

    cnt = Counter(r['amplicon'] for r in resources)

    counts = dict(cnt.most_common())
    counts['all'] = sum(counts.values())

    return counts


# Cached CKAN services
# Some of the other CKAN services above rely on these


def ckan_get_packages_by_organisation(org_name):
    cache = caches['big_objects']
    ckan = get_ckan()

    args = OrderedDict((
        ('q', 'organization:%s' % org_name),
        ('include_private', True),
        ('rows', 10000),
    ))

    args_str = ','.join('%s=%s' % i for i in args.items())
    key = sha1('ckan_package_search(%s)' % args_str).hexdigest()

    packages = cache.get(key)
    if packages is None:
        result = ckan.call_action('package_search', args)
        packages = result['results']
        cache.set(key, packages)

    return packages


def ckan_get_packages_by_resource_type(resource_type):
    cache = caches['big_objects']
    ckan = get_ckan()

    args = OrderedDict((
        ('q', 'type:%s' % resource_type),
        ('include_private', True),
        ('rows', 10000),
    ))

    args_str = ','.join('%s=%s' % i for i in args.items())
    key = sha1('ckan_package_search(%s)' % args_str).hexdigest()

    packages = cache.get(key)
    if packages is None:
        result = ckan.call_action('package_search', args)
        packages = result['results']
        cache.set(key, packages)

    return packages


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


class JsonError(JsonResponse):
    def __init__(self, data, *args, **kwargs):
        resp = data
        if isinstance(data, dict):
            resp = data.copy()
            resp['success'] = False

        super(JsonError, self).__init__(resp, *args, **kwargs)

    @classmethod
    def from_exception(cls, exc):
        return JsonError({'msg': repr(exc)})



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

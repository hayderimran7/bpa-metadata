from django.conf.urls import patterns, url
from django.conf import settings
from django.views.decorators.cache import cache_page
from ckan_views import CKANProxyView, ckan_resources, ckan_resources_count, ckan_resources_count_by_amplicon


urlpatterns = patterns(
    '',
    # url(r'^proxy(?P<path>.*)$', cache_page(settings.CKAN_CACHE_TIMEOUT)(CKANProxyView.as_view()), name='proxy'),
    url(r'^proxy/(?P<path>.*)$', CKANProxyView.as_view(), name='proxy'),
    url(r'^resources/(?P<org_name>[\w-]+)/(?P<package_type>[\w-]+)/?$', ckan_resources, name='resources'),
    url(r'^resources_count/(?P<org_name>[\w-]+)/(?P<package_type>[\w-]+)/?$', ckan_resources_count, name='resources_count'),
    url(r'^resources_count_by_amplicon/?$', ckan_resources_count_by_amplicon, name='resources_count_by_amplicon'),
)

from django.conf.urls import patterns, url
from django.conf import settings
from django.views.decorators.cache import cache_page

import ckan_views as views


urlpatterns = patterns(
    '',
    # url(r'^proxy(?P<path>.*)$', cache_page(settings.CKAN_CACHE_TIMEOUT)(CKANProxyView.as_view()), name='proxy'),
    url(r'^proxy/(?P<path>.*)$', views.CKANProxyView.as_view(), name='proxy'),
    url(r'^packages/(?P<org_name>[\w-]+)/?$', views.ckan_packages, name='packages'),
    url(r'^packages_count/(?P<org_name>[\w-]+)/?$', views.ckan_packages_count, name='packages_count'),
    url(r'^resources/(?P<org_name>[\w-]+)/(?P<package_type>[\w-]+)/?$', views.ckan_resources, name='resources'),
    url(r'^resources_count/(?P<org_name>[\w-]+)/?$', views.ckan_resources_count, name='resources_count'),
    url(r'^resources_count_by_amplicon/?$', views.ckan_resources_count_by_amplicon, name='resources_count_by_amplicon'),
)

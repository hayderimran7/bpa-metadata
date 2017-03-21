from django.conf.urls import patterns, url
from django.conf import settings
from django.views.decorators.cache import cache_page
from django.views.defaults import page_not_found

import ckan_views as views


urlpatterns = patterns(
    '',
    url(r'^$', page_not_found, name='index'),

    # Disabled the proxy for now, leaving the code for a while in case we will need it
    # url(r'^proxy/(?P<path>.*)$', views.CKANProxyView.as_view(), name='proxy'),

    url(r'^packages/(?P<org_name>[\w-]+)/?$', views.ckan_packages, name='packages'),
    url(r'^packages/(?P<org_name>[\w-]+)/(?P<package_type>[\w-]+)/?$', views.ckan_packages, name='packages'),
    url(r'^package_show/(?P<package_id>.+)/?$', views.ckan_package_show, name='package_show'),
    url(r'^packages_count/?$', views.ckan_packages_count, name='packages_count'),
    url(r'^packages_count/(?P<org_name>[\w-]+)/?$', views.ckan_packages_count, name='packages_count'),

    url(r'^resources/(?P<org_name>[\w-]+)/(?P<package_type>[\w-]+)/?$', views.ckan_resources, name='resources'),

    url(r'^resources_count/(?P<org_name>[\w-]+)/?$', views.ckan_resources_count, name='resources_count'),
    url(r'^resources_count_by_amplicon/?$', views.ckan_resources_count_by_amplicon, name='resources_count_by_amplicon'),

    url(r'^mm_project_overview_count/?$', views.mm_project_overview_count, name='mm_project_overview_count'),
    url(r'^stemcell_project_overview_count/?$', views.stemcell_project_overview_count, name='stemcell_project_overview_count'),
)

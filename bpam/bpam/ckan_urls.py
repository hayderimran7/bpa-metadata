from django.conf.urls import patterns, url
from django.views.defaults import page_not_found

import ckan_views as views


urlpatterns = patterns(
    '',
    url(r'^$', page_not_found, name='index'),

    # Disabled the proxy for now, leaving the code for a while in case we will need it
    # url(r'^proxy/(?P<path>.*)$', views.CKANProxyView.as_view(), name='proxy'),

    url(r'^package_list/(?P<org_name>[\w-]+)/?$', views.package_list, name='package_list'),
    url(r'^package_list/(?P<org_name>[\w-]+)/(?P<resource_type>[\w-]+)/?$', views.package_list, name='package_list'),
    url(r'^package_list/(?P<org_name>[\w-]+)/(?P<resource_type>[\w-]+)/(?P<status>(embargoed|public))/?$', views.package_list, name='package_list'),

    url(r'^package_list/(?P<org_name>[\w-]+)/(?P<resource_type>[\w-]+)/(?P<status>(sample_processing|bpa_archive_ingest|bpa_qc))/?$', views.models_package_list, name='models_package_list'),
    url(r'^sepsis_contextual_data/?$', views.sepsis_contextual_list, name='sepsis_contextual_list'),

    url(r'^package_detail/(?P<project>[\w-]+)/(?P<resource_type>[^/]+)/(?P<status>[\w-]+)/(?P<package_id>.+)/?$', views.package_detail, name='package_detail'),
    url(r'^package_detail/(?P<package_id>.+)/?$', views.package_detail, name='package_detail'),

    url(r'^resource_list/(?P<org_name>[\w-]+)/(?P<resource_type>[\w-]+)/?$', views.resource_list, name='resource_list'),

    url(r'^packages_count/?$', views.packages_count_by_organisation, name='packages_count'),
    url(r'^packages_count/(?P<org_name>[\w-]+)/?$', views.packages_count_by_organisation, name='packages_count'),

    url(r'^org_packages_and_resources_count/(?P<org_name>[\w-]+)/?$', views.org_packages_and_resources_count, name='org_packages_and_resources_count'),

    url(r'^amplicon_resources_count/?$', views.amplicon_resources_count, name='amplicon_resources_count'),

    url(r'^mm_project_overview_count/?$', views.mm_project_overview_count, name='mm_project_overview_count'),
    url(r'^stemcell_project_overview_count/?$', views.stemcell_project_overview_count, name='stemcell_project_overview_count'),
    url(r'^sepsis_project_overview_count/?$', views.sepsis_project_overview_count, name='sepsis_project_overview_count'),
)

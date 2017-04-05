# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.views.generic import TemplateView

from bpam.decorators import DEBUG_ONLY_VIEW

import views


urlpatterns = [
    url(r'^$', DEBUG_ONLY_VIEW(views.MMView.as_view()), name='index'),

    url(r'^samples/?$', views.SampleListView.as_view(), name='samples'),
    url(r'^sample/(?P<package_id>[^\/]+)/?$', views.SampleDetailView.as_view(), name='sample'),
    url(r'^sample/(?P<resource_type>[^/]+)/(?P<status>[\w-]+)/(?P<package_id>[^\/]+)/?$', views.SampleDetailView.as_view(), name='sample'),
    url(r'^metagenomic_sequence_files/?$', views.MetagenomicFileListView.as_view(), name='metagenomic_sequence_files'),

    url(r'^amplicons$', views.AmpliconIndexView.as_view(), name='amplicon_index'),
    url(r'^amplicons/all/?$', views.AmpliconListView.as_view(), name='amplicons_all'),
    url(r'^amplicons/16S/?$', views.Amplicon16SListView.as_view(), name='amplicons_16S'),
    url(r'^amplicons/18S/?$', views.Amplicon18SListView.as_view(), name='amplicons_18S'),
    url(r'^amplicons/A16S/?$', views.AmpliconA16SListView.as_view(), name='amplicons_A16S'),
    url(r'^amplicon/(?P<pk>.*)/?$', views.AmpliconDetailView.as_view(), name='amplicon_detail'),

    url(r'^overview/?$',
        TemplateView.as_view(template_name='marine_microbes/project_overview.html'),
        name='overview'),
]

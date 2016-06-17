# -*- coding: utf-8 -*-

from django.conf.urls import url
import views

urlpatterns = [
    url(regex=r'^$', view=views.MMView.as_view(), name='index'),
    url(regex=r'^contacts$', view=views.ContactsView.as_view(),
        name='contacts'),
    url(regex=r'^samples', view=views.SampleListView.as_view(),
        name='samples'),
    url(regex=r'^sample/(?P<pk>.*)/$',
        view=views.SampleDetailView.as_view(),
        name='sample'),
    url(regex=r'^metagenomic_sequence_files',
        view=views.MetagenomicFileListView.as_view(),
        name='metagenomic_sequence_files'),
    url(regex=r'^consortium$', view=views.ConsortiumView.as_view(),
        name='consortium'),
]

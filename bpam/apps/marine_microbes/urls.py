# -*- coding: utf-8 -*-

from django.conf.urls import url
import views
import tracker_views

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
    url(regex=r'^amplicons$', view=views.AmpliconIndexView.as_view(),
        name='amplicon_index'),
    url(regex=r'^amplicons/all/$$',
        view=views.AmpliconListView.as_view(),
        name='amplicons_all'),
    url(regex=r'^amplicons/16S/$',
        view=views.Amplicon16SListView.as_view(),
        name='amplicons_16S'),
    url(regex=r'^amplicons/18S/$',
        view=views.Amplicon18SListView.as_view(),
        name='amplicons_18S'),
    url(regex=r'^amplicons/A16S/$',
        view=views.AmpliconA16SListView.as_view(),
        name='amplicons_A16S'),
    url(regex=r'^amplicon/(?P<pk>.*)/$',
        view=views.AmpliconDetailView.as_view(),
        name='amplicon_detail'),
    url(regex=r'^sites/(?P<pk>\d+)/$',
        view=views.CollectionSiteDetailView.as_view(),
        name='collectionsitedetail'),
    url(regex=r'^sites', view=views.CollectionSiteListView.as_view(),
        name='collectionsites'),
    url(regex=r'^methods$',
        view=views.MethodsView.as_view(),
        name='methods'),

    # BEGIN----- Tracker URLs ----------

    url(regex=r'^overview/$',
        view=tracker_views.TrackOverview.as_view(),
        name='overview'),

    url(regex=r'^overview/data/$',
        view=tracker_views.TrackOverviewConstraints.as_view(),
        name='overview_constraints'),

    url(regex=r'^overview/(?P<constraint>.*)/(?P<status>.*)/$',
        view=tracker_views.TrackDetails.as_view(),
        name='overview_detail'),

    # END------- Tracker URLs ----------
]

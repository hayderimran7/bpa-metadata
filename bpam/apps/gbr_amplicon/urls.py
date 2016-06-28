from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
                       url(regex=r'^$', view=views.IndexView.as_view(),
                           name='index'),
                       url(regex=r'^amplicons$',
                           view=views.AmpliconListView.as_view(),
                           name='amplicons'),
                       url(regex=r'^amplicons/16S/$',
                           view=views.Amplicon16SListView.as_view(),
                           name='amplicons_16S'),
                       url(regex=r'^amplicons/18S/$',
                           view=views.Amplicon18SListView.as_view(),
                           name='amplicons_18S'),
                       url(regex=r'^amplicons/ITS/$',
                           view=views.AmpliconITSListView.as_view(),
                           name='amplicons_ITS'),
                       url(regex=r'^amplicons/A16S/$',
                           view=views.AmpliconA16SListView.as_view(),
                           name='amplicons_A16S'),
                       url(regex=r'^amplicon/(?P<pk>.*)/$',
                           view=views.AmpliconDetailView.as_view(),
                           name='amplicon'), )

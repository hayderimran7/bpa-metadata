from django.conf.urls import patterns, url

from . import views
import data_export

urlpatterns = patterns(
    '',
    url(
        regex=r'^$',
        view=views.GBRView.as_view(),
        name='index'),
    url(
        regex=r'^collections',
        view=views.CollectionEventListView.as_view(),
        name='collections'),
    url(
        regex=r'^collection/?.*/$',
        view=views.CollectionView.as_view(),
        name='collection'),
    url(
        regex=r'^samples/csv',
        view=data_export.get_samples,
        name='samples_csv'),
    url(
        regex=r'^samples',
        view=views.SampleListView.as_view(),
        name='samples'),
    url(
        regex=r'^sites',
        view=views.CollectionSiteListView.as_view(),
        name='sites'),
    url(
        regex=r'^site/(?P<pk>.*)/$',
        view=views.CollectionSiteDetailView.as_view(),
        name='site'),
    url(
        regex=r'^sample/(?P<pk>.*)/$',
        view=views.SampleDetailView.as_view(),
        name='sample'),
    url(
        regex=r'^sequencefiles/csv',
        view=data_export.get_sequencefiles,
        name='sequencefiles_csv'),
    url(
        regex=r'^sequencefiles',
        view=views.SequenceFileListView.as_view(),
        name='sequencefiles'),
    url(
        regex=r'^contacts$',
        view=views.ContactsView.as_view(),
        name='contacts'),
)

from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    '',
    url(
        regex=r'^$',
        view=views.GBRView.as_view(),
        name='index'),
    url(
        regex=r'^collections',
        view=views.CollectionListView.as_view(),
        name='collections'),
    url(
        regex=r'^collection/?.*/$',
        view=views.CollectionView.as_view(),
        name='collection'),
    url(
        regex=r'^samples',
        view=views.SampleListView.as_view(),
        name='samples'),
    url(
        regex=r'^sample/(?P<pk>.*)/$',
        view=views.SampleDetailView.as_view(),
        name='sample'),
    url(
        regex=r'^sequencefiles',
        view=views.SequenceFileListView.as_view(),
        name='sequencefiles'),
)
